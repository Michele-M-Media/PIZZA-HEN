#include <pthread.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/syscall.h>
#include <sys/time.h>

#include "cr_hotkey_hook.h"
#include "cr_browser.h"
#include "cr_config.h"
#include "cr_game_monitor.h"
#include "cr_hotkey_buttons.h"
#include "cr_hotkey_signal.h"
#include "cr_log.h"
#include "cr_paths.h"
#include "elfldr.h"
#include "priv_bootstrap.h"
#include "pt.h"

#include "cr_getdata_payload_blob.h"

volatile int g_hotkey_hook_running = 1;

/* If SceShellUI keeps restarting right after we hook it, something we're
 * doing is likely the cause; stop after this many and require a relaunch. */
#define CR_HOTKEY_MAX_REINJECTS 5

/* Just a find_pid_by_name() call when nothing changed — cheap enough to
 * poll often, so a SceShellUI restart (e.g. rest-mode wake) is caught fast. */
#define CR_HOTKEY_POLL_MS 20000

#ifdef __SCE__
/* Reads combo/hold_ms out of g_cfg and pushes it via a throwaway socket -
 * same pattern as the payload's own send_hotkey_signal(). */
static void
broadcast_hotkey_config(void) {
  int fd = socket(AF_INET, SOCK_DGRAM, 0);
  if (fd < 0) {
    return;
  }

  struct sockaddr_in addr;
  memset(&addr, 0, sizeof(addr));
  addr.sin_family = AF_INET;
  addr.sin_port = htons(CR_HOTKEY_CONFIG_SIGNAL_PORT);
  addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);

  pthread_mutex_lock(&g_cfg_lock);
  cr_hotkey_config_packet_t pkt;
  pkt.combo = cr_hotkey_button_value(g_cfg.hotkey_button_a) | cr_hotkey_button_value(g_cfg.hotkey_button_b);
  pkt.hold_ms = (uint32_t)g_cfg.hotkey_hold_ms;
  pthread_mutex_unlock(&g_cfg_lock);

  sendto(fd, &pkt, sizeof(pkt), 0, (struct sockaddr *)&addr, sizeof(addr));
  close(fd);
}

/* A target already hooked by a previous session makes cr_detour_function
 * skip silently - only killing SceShellUI (it respawns) clears that. */
#define CR_SHELLUI_RESPAWN_TIMEOUT_MS 15000
#define CR_SHELLUI_RESPAWN_POLL_MS 300

static void
restart_shellui(void) {
  pid_t old_pid = find_pid_by_name("SceShellUI");
  if (old_pid <= 0) {
    return;
  }
  cr_log("info", "hotkey_hook", "killing SceShellUI (pid=%d) to clear any stale hooks", (int)old_pid);
  kill(old_pid, SIGKILL);

  int waited_ms = 0;
  pid_t new_pid;
  do {
    usleep(CR_SHELLUI_RESPAWN_POLL_MS * 1000);
    waited_ms += CR_SHELLUI_RESPAWN_POLL_MS;
    new_pid = find_pid_by_name("SceShellUI");
  } while (g_hotkey_hook_running && (new_pid <= 0 || new_pid == old_pid) &&
           waited_ms < CR_SHELLUI_RESPAWN_TIMEOUT_MS);

  if (new_pid > 0 && new_pid != old_pid) {
    cr_log("info", "hotkey_hook", "SceShellUI respawned (pid=%d)", (int)new_pid);
  } else {
    cr_log("warn", "hotkey_hook", "SceShellUI didn't respawn within %ds", CR_SHELLUI_RESPAWN_TIMEOUT_MS / 1000);
  }
}

/* elfldr_exec succeeding only means the thread spawned, not that Mono was
 * loaded or the hook took - wait for the payload's own ok/old confirmation instead. */
#define CR_HOTKEY_CONFIRM_TIMEOUT_MS 10000

static int
inject_hook(pid_t pid, int sig_fd) {
  int rc = pt_attach_timed(pid, 2000);
  if (rc != 0) {
    cr_log("warn", "hotkey_hook", "couldn't attach to SceShellUI (pid=%d, rc=%d)", (int)pid, rc);
    return -1;
  }

  rc = elfldr_exec(pid, -1, (uint8_t *)g_cr_getdata_payload_elf);
  if (rc != 0) {
    cr_log("warn", "hotkey_hook", "couldn't hook into SceShellUI (pid=%d, rc=%d)", (int)pid, rc);
    return -1;
  }

  struct timeval tv;
  tv.tv_sec = CR_HOTKEY_CONFIRM_TIMEOUT_MS / 1000;
  tv.tv_usec = (CR_HOTKEY_CONFIRM_TIMEOUT_MS % 1000) * 1000;
  setsockopt(sig_fd, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));

  char buf[8];
  memset(buf, 0, sizeof(buf));
  ssize_t n = recv(sig_fd, buf, sizeof(buf) - 1, 0);
  if (n > 0 && !strcmp(buf, "old")) {
    cr_log("info", "hotkey_hook", "SceShellUI (pid=%d) still has a stale hook from a "
                                   "previous session - restarting it", (int)pid);
    restart_shellui();
    return -1;
  }
  if (n > 0 && !strcmp(buf, "ok")) {
    cr_log("info", "hotkey_hook", "hooked into SceShellUI (pid=%d)", (int)pid);
    return 0;
  }

  cr_log("warn", "hotkey_hook", "injected into SceShellUI (pid=%d) but no confirmation "
                                 "yet (Mono likely not loaded) - will retry", (int)pid);
  return -1;
}
#endif

void *
hotkey_hook_thread(void *arg) {
  (void)arg;
  syscall(SYS_thr_set_name, -1, "CheatRunner.elf");

#ifdef __SCE__
  while (g_hotkey_hook_running && !cr_priv_can_patch_game_memory()) {
    usleep(500 * 1000);
  }
  if (!g_hotkey_hook_running) {
    return NULL;
  }

  int fd = socket(AF_INET, SOCK_DGRAM, 0);
  if (fd < 0) {
    cr_log("warn", "hotkey_hook", "couldn't open the signal socket");
    return NULL;
  }

  int opt = 1;
  setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
  /* SO_REUSEPORT lets a new instance bind immediately even if a SIGKILL'd old process is still alive in kernel sleep. */
  setsockopt(fd, SOL_SOCKET, SO_REUSEPORT, &opt, sizeof(opt));

  struct sockaddr_in addr;
  memset(&addr, 0, sizeof(addr));
  addr.sin_family = AF_INET;
  addr.sin_port = htons(CR_HOTKEY_SIGNAL_PORT);
  addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);

  if (bind(fd, (struct sockaddr *)&addr, sizeof(addr)) != 0) {
    cr_log("warn", "hotkey_hook", "couldn't bind the signal port");
    close(fd);
    return NULL;
  }

  /* recv() times out periodically so this loop can both notice shutdown
   * and re-check the hook on a timer. */
  struct timeval tv;
  tv.tv_sec = 1;
  tv.tv_usec = 0;
  setsockopt(fd, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));

  pid_t last_hooked_pid = -1;
  int reinject_count = 0;
  int gave_up = 0;
  uint64_t next_check_ms = now_ms();

  char buf[64];
  while (g_hotkey_hook_running) {
    uint64_t now = now_ms();

    pthread_mutex_lock(&g_cfg_lock);
    int hotkey_enabled = g_cfg.hotkey_enabled;
    pthread_mutex_unlock(&g_cfg_lock);

    if (!hotkey_enabled) {
      /* Master off switch - never attach to/inject into SceShellUI. Some
       * firmwares (4.xx) can crash from this hook; cheap poll so re-enabling works without a restart. */
      next_check_ms = now + 5000;
    } else if (!gave_up && now >= next_check_ms) {
      pid_t pid = find_pid_by_name("SceShellUI");
      if (pid <= 0) {
        next_check_ms = now + 5000;
      } else if (pid == last_hooked_pid) {
        /* same process we already hooked — nothing to do until it restarts. */
        next_check_ms = now + CR_HOTKEY_POLL_MS;
      } else {
        int inject_rc = inject_hook(pid, fd);
        /* inject_hook bumps SO_RCVTIMEO to wait for the payload's
         * confirmation - put it back to the steady-state 1s poll. */
        tv.tv_sec = 1;
        tv.tv_usec = 0;
        setsockopt(fd, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));

        if (inject_rc == 0) {
          last_hooked_pid = pid;
          broadcast_hotkey_config();
          next_check_ms = now + CR_HOTKEY_POLL_MS;
          reinject_count++;
          if (reinject_count > CR_HOTKEY_MAX_REINJECTS) {
            gave_up = 1;
            cr_log("warn", "hotkey_hook",
                   "SceShellUI restarted %d times in a row — giving up on the hotkey "
                   "until CheatRunner is relaunched", reinject_count);
          }
        } else {
          next_check_ms = now + 5000;
        }
      }
    }

    ssize_t n = recv(fd, buf, sizeof(buf), 0);
    if (n <= 0) {
      /* timeout — also the natural ~1s tick to re-push config in case it
       * changed since the last inject (e.g. edited from the dashboard). */
      if (last_hooked_pid > 0) {
        broadcast_hotkey_config();
      }
      continue;
    }

    pthread_mutex_lock(&g_cfg_lock);
    int port = g_cfg.http_port;
    pthread_mutex_unlock(&g_cfg_lock);

    /* A game running when the hotkey fires means it was pressed in-game -
     * jump straight to its trainer, matching the #trainer= hash the frontend handles. */
    running_game_state_t rgs;
    running_state_get(&rgs);

    char url[128];
    if (rgs.running && rgs.title_id[0]) {
      snprintf(url, sizeof(url), "http://127.0.0.1:%d/#trainer=%s", port, rgs.title_id);
    } else {
      snprintf(url, sizeof(url), "http://127.0.0.1:%d/", port);
    }
    cr_log("info", "hotkey_hook", "hotkey held — opening %s", url);
    cr_browser_open_url(url);
  }

  close(fd);
#endif /* __SCE__ */

  return NULL;
}
