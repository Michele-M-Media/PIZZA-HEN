/* Injected into SceShellUI via elfldr_exec (see cr_hotkey_hook.c).
 * Hooks GamePad.GetData. */

#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/syscall.h>
#include <time.h>

#include <ps5/kernel.h>
#include <ps5/klog.h>

#include "cr_detour.h"
#include "cr_hotkey_signal.h"

#define SYS_DL_GET_LIST   0x217
#define SYS_DL_GET_INFO_2 0x2cd

#define MODULE_INFO_NAME_LENGTH 128
#define MODULE_INFO_SANDBOXED_PATH_LENGTH 1024
#define MODULE_INFO_MAX_SECTIONS 4
#define FINGERPRINT_LENGTH 20
#define MODULE_HANDLE_MAX 256

typedef struct {
  uint64_t vaddr;
  uint32_t size;
  uint32_t prot;
} module_section_t;

/* matches SYS_dl_get_info_2's output layout; only filename/handle are used */
typedef struct {
  char filename[MODULE_INFO_NAME_LENGTH];
  uint64_t handle;
  uint8_t unknown0[32];
  uint64_t init;
  uint64_t fini;
  uint64_t eh_frame_hdr;
  uint64_t eh_frame_hdr_sz;
  uint64_t eh_frame;
  uint64_t eh_frame_sz;
  module_section_t sections[MODULE_INFO_MAX_SECTIONS];
  uint8_t unknown7[1176];
  uint8_t fingerprint[FINGERPRINT_LENGTH];
  uint32_t unknown8;
  char libname[MODULE_INFO_NAME_LENGTH];
  uint32_t unknown9;
  char sandboxed_path[MODULE_INFO_SANDBOXED_PATH_LENGTH];
  uint64_t sdk_version;
} module_info_t;

static int
find_module_handle(const char *module_name) {
  pid_t pid = getpid();
  size_t num_handles = 0;

  syscall(SYS_DL_GET_LIST, pid, NULL, 0, &num_handles);
  if (!num_handles) {
    klog_puts("hotkey_hook: no modules found in SceShellUI\n");
    return 0;
  }

  /* Fixed-size stack buffer instead of malloc/free - a heap-decommit
   * assertion in SceShellUI's own allocator (seen on 4.03) fired right around this pair. */
  uintptr_t handles[MODULE_HANDLE_MAX];
  if (num_handles > MODULE_HANDLE_MAX) {
    num_handles = MODULE_HANDLE_MAX;
  }
  syscall(SYS_DL_GET_LIST, pid, handles, num_handles, &num_handles);

  int found = 0;
  module_info_t info;
  for (size_t i = 0; i < num_handles && !found; i++) {
    memset(&info, 0, sizeof(info));
    syscall(SYS_DL_GET_INFO_2, pid, 1, handles[i], &info);
    if (!strcmp(info.filename, module_name)) {
      found = (int)info.handle;
    }
  }

  return found;
}

/* opaque; only pointers to these exist here, real layout is in libmonosgen */
typedef struct MonoDomain  MonoDomain;
typedef struct MonoAssembly MonoAssembly;
typedef struct MonoImage   MonoImage;
typedef struct MonoClass   MonoClass;
typedef struct MonoMethod  MonoMethod;
typedef struct MonoThread  MonoThread;

static MonoDomain *  (*p_mono_get_root_domain)(void);
static MonoThread *  (*p_mono_thread_attach)(MonoDomain *);
static MonoAssembly *(*p_mono_domain_assembly_open)(MonoDomain *, const char *);
static MonoImage *   (*p_mono_assembly_get_image)(MonoAssembly *);
static MonoClass *   (*p_mono_class_from_name)(MonoImage *, const char *, const char *);
static MonoMethod *  (*p_mono_class_get_method_from_name)(MonoClass *, const char *, int);
static uint64_t      (*p_mono_compile_method)(MonoMethod *);

static int
resolve_mono_symbols(void) {
  int handle = find_module_handle("libmonosgen-2.0.sprx");
  if (!handle) {
    klog_puts("hotkey_hook: Mono isn't loaded in SceShellUI yet\n");
    return -1;
  }

  *(void **)&p_mono_get_root_domain =
      (void *)kernel_dynlib_dlsym(-1, handle, "mono_get_root_domain");
  *(void **)&p_mono_thread_attach =
      (void *)kernel_dynlib_dlsym(-1, handle, "mono_thread_attach");
  *(void **)&p_mono_domain_assembly_open =
      (void *)kernel_dynlib_dlsym(-1, handle, "mono_domain_assembly_open");
  *(void **)&p_mono_assembly_get_image =
      (void *)kernel_dynlib_dlsym(-1, handle, "mono_assembly_get_image");
  *(void **)&p_mono_class_from_name =
      (void *)kernel_dynlib_dlsym(-1, handle, "mono_class_from_name");
  *(void **)&p_mono_class_get_method_from_name =
      (void *)kernel_dynlib_dlsym(-1, handle, "mono_class_get_method_from_name");
  *(void **)&p_mono_compile_method =
      (void *)kernel_dynlib_dlsym(-1, handle, "mono_compile_method");

  if (!p_mono_get_root_domain || !p_mono_thread_attach || !p_mono_domain_assembly_open ||
      !p_mono_assembly_get_image || !p_mono_class_from_name ||
      !p_mono_class_get_method_from_name || !p_mono_compile_method) {
    klog_puts("hotkey_hook: couldn't resolve Mono symbols\n");
    return -1;
  }
  return 0;
}

/* Sce.PlayStation.Core.Input.GamePad's GamePadData value type — field order
 * and sizes matter here, it's returned by value via the SysV hidden-pointer ABI. */
typedef struct {
  uint8_t skip;
  uint32_t buttons;
  uint32_t buttons_prev;
  uint32_t buttons_down;
  uint32_t buttons_up;
  float analog_left_x;
  float analog_left_y;
  float analog_right_x;
  float analog_right_y;
} cr_gamepad_data_t;

#define CR_BUTTON_L2 4096u
#define CR_BUTTON_R3 32768u

/* Defaults match the original hardcoded L2+R3/800ms - overwritten by the
 * daemon's config broadcast once poll_hotkey_config() picks one up. */
static uint32_t g_hotkey_combo = CR_BUTTON_L2 | CR_BUTTON_R3;
static uint32_t g_hotkey_hold_ms = 800;

static int g_hotkey_config_fd = -1;

static void
init_hotkey_config_socket(void) {
  g_hotkey_config_fd = socket(AF_INET, SOCK_DGRAM, 0);
  if (g_hotkey_config_fd < 0) {
    return;
  }

  int opt = 1;
  setsockopt(g_hotkey_config_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
  setsockopt(g_hotkey_config_fd, SOL_SOCKET, SO_REUSEPORT, &opt, sizeof(opt));

  struct sockaddr_in addr;
  memset(&addr, 0, sizeof(addr));
  addr.sin_family = AF_INET;
  addr.sin_port = htons(CR_HOTKEY_CONFIG_SIGNAL_PORT);
  addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);

  if (bind(g_hotkey_config_fd, (struct sockaddr *)&addr, sizeof(addr)) != 0) {
    klog_puts("hotkey_hook: couldn't bind the config signal port\n");
    close(g_hotkey_config_fd);
    g_hotkey_config_fd = -1;
  }
}

/* Non-blocking - called once per GetData call, drains to the newest packet. */
static void
poll_hotkey_config(void) {
  if (g_hotkey_config_fd < 0) {
    return;
  }
  cr_hotkey_config_packet_t pkt;
  while (recv(g_hotkey_config_fd, &pkt, sizeof(pkt), MSG_DONTWAIT) == (ssize_t)sizeof(pkt)) {
    if (pkt.combo != 0) {
      g_hotkey_combo = pkt.combo;
    }
    if (pkt.hold_ms >= 100 && pkt.hold_ms <= 5000) {
      g_hotkey_hold_ms = pkt.hold_ms;
    }
  }
}

static uint64_t
now_ms(void) {
  struct timespec ts;
  clock_gettime(CLOCK_MONOTONIC, &ts);
  return (uint64_t)ts.tv_sec * 1000ULL + (uint64_t)ts.tv_nsec / 1000000ULL;
}

static void
send_signal(const char *msg) {
  int fd = socket(AF_INET, SOCK_DGRAM, 0);
  if (fd < 0) {
    return;
  }

  struct sockaddr_in addr;
  memset(&addr, 0, sizeof(addr));
  addr.sin_family = AF_INET;
  addr.sin_port = htons(CR_HOTKEY_SIGNAL_PORT);
  addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);

  sendto(fd, msg, strlen(msg), 0, (struct sockaddr *)&addr, sizeof(addr));
  close(fd);
}

static cr_gamepad_data_t (*orig_get_data)(int);

/* Always forwards to the real GetData — SceShellUI's own input handling
 * depends on this result, unlike the old CaptureScreen hook this replaced. */
static cr_gamepad_data_t
hook_get_data(int device_index) {
  cr_gamepad_data_t result;
  memset(&result, 0, sizeof(result));
  if (orig_get_data) {
    result = orig_get_data(device_index);
  }

  poll_hotkey_config();

  static uint64_t held_since_ms = 0;
  static int fired = 0;

  int combo_held = (result.buttons & g_hotkey_combo) == g_hotkey_combo;
  uint64_t now = now_ms();

  if (combo_held) {
    if (held_since_ms == 0) {
      held_since_ms = now;
    } else if (!fired && now - held_since_ms >= g_hotkey_hold_ms) {
      fired = 1;
      send_signal("hotkey");
    }
  } else {
    held_since_ms = 0;
    fired = 0;
  }

  return result;
}

/* elfldr_exec restores SceShellUI's own ucred before resuming, so main()
 * starts unprivileged again. Same debug authid etaHEN's shellui.elf uses. */
#define CR_DEBUG_AUTHID 0x4800000000000006ull

static void
save_fpu_state(uint8_t buf[512]) {
  __asm__ volatile("fxsave (%0)" : : "r"(buf) : "memory");
}

static void
restore_fpu_state(uint8_t buf[512]) {
  __asm__ volatile("fxrstor (%0)" : : "r"(buf) : "memory");
}

int
main(void) {
  /* elfldr_exec hijacks a live thread's rip; ptrace's GETREGS never saved its
   * FPU/SSE state, so save/restore it or our own float ops corrupt it on return. */
  uint8_t fpu_state[512] __attribute__((aligned(16)));
  save_fpu_state(fpu_state);

  klog_puts("hotkey_hook: setting up the hotkey\n");

  init_hotkey_config_socket();

  pid_t self = getpid();
  uint64_t old_authid = kernel_get_ucred_authid(self);
  kernel_set_ucred_authid(self, CR_DEBUG_AUTHID);

  int rc = 1;

  if (resolve_mono_symbols()) {
    goto out;
  }

  MonoDomain *domain = p_mono_get_root_domain();
  if (!domain) {
    klog_puts("hotkey_hook: couldn't get Mono's root domain\n");
    goto out;
  }

  /* pthread_create gives us a thread Mono has never seen; every other Mono
   * call here needs this first or mono_thread_info_current() asserts. */
  p_mono_thread_attach(domain);

  MonoAssembly *assembly = p_mono_domain_assembly_open(
      domain, "/system_ex/common_ex/lib/Sce.PlayStation.Core.dll");
  if (!assembly) {
    klog_puts("hotkey_hook: couldn't open the Core assembly\n");
    goto out;
  }

  MonoImage *image = p_mono_assembly_get_image(assembly);
  if (!image) {
    klog_puts("hotkey_hook: couldn't get the Core image\n");
    goto out;
  }

  MonoClass *klass = p_mono_class_from_name(image, "Sce.PlayStation.Core.Input", "GamePad");
  if (!klass) {
    klog_puts("hotkey_hook: GamePad class not found\n");
    goto out;
  }

  MonoMethod *method = p_mono_class_get_method_from_name(klass, "GetData", 1);
  if (!method) {
    klog_puts("hotkey_hook: GetData method not found\n");
    goto out;
  }

  uint64_t addr = p_mono_compile_method(method);
  void *trampoline = addr ? cr_detour_function(addr, (void *)hook_get_data) : NULL;
  if (trampoline == CR_DETOUR_ALREADY_HOOKED) {
    /* a previous session's hook is still resident - only the daemon can fix
     * this (it needs to restart SceShellUI), so tell it. */
    klog_puts("hotkey_hook: target already hooked by a previous session\n");
    send_signal("old");
    goto out;
  }
  if (trampoline) {
    orig_get_data = (cr_gamepad_data_t(*)(int))trampoline;
    klog_puts("hotkey_hook: hotkey ready\n");
    send_signal("ok");
    rc = 0;
  }

out:
  /* the installed hook itself needs no special privilege (it just sends a
   * UDP packet), so don't leave SceShellUI's authid altered afterward */
  kernel_set_ucred_authid(self, old_authid);
  restore_fpu_state(fpu_state);
  return rc;
}
