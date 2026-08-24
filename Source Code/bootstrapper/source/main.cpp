/* Copyright (C) 2025 etaHEN / LightningMods

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 3, or (at your option) any
later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; see the file COPYING. If not, see
<http://www.gnu.org/licenses/>.  */


/******************************************************************************
 * Standard and System Header Includes
 ******************************************************************************/
 #include <csignal>
 #include <dirent.h>
 #include <errno.h>
 #include <fcntl.h>
 #include <netinet/in.h>
 #include <pthread.h>
 #include <setjmp.h>
 #include <stdarg.h>
 #include <stdbool.h>
 #include <stdint.h>
 #include <stdio.h>
 #include <stdlib.h>
 #include <string.h>
 #include <sys/_iovec.h>
 #include <sys/mount.h>
 #include <sys/signal.h>
 #include <sys/socket.h>
 #include <sys/stat.h>
 #include <sys/sysctl.h>
 #include <sys/types.h>
 #include <sys/un.h>
 #include <sys/wait.h>
 #include <unistd.h>

#include <pizzahen/identity.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <errno.h>
 
 /******************************************************************************
  * Custom Header Includes
  ******************************************************************************/
 #include <util.hpp>
 #include <freebsd-helper.h>
 
 extern "C" {
 #include "elfldr.h"
 #include "faulthandler.h"
 #include "hbldr.h"
 #include "pt.h"
 #include <ps5/klog.h>
 #include <ps5/kernel.h>

 pid_t elfldr_spawn(const char* cwd, int stdio, uint8_t* elf, const char* name);
 int sceKernelMprotect(void* addr, size_t len, int prot);
 int sceSystemServiceLaunchWebBrowser(const char *uri);

 extern uint8_t kstuff_start[];
 extern const unsigned int kstuff_size;
 extern uint8_t kstuff_dr_start[];
 extern const unsigned int kstuff_dr_size;
 extern uint8_t kstuff_base_start[];
 extern const unsigned int kstuff_base_size;
 extern uint8_t websrv_start[];
 extern const unsigned int websrv_size;
 extern uint8_t selector_js_start[];
 extern const unsigned int selector_js_size;
 extern uint8_t selector_html_start[];
 extern const unsigned int selector_html_size;
 extern uint8_t selector_icon_start[];
 extern const unsigned int selector_icon_size;
 extern uint8_t selector_action_start[];
 extern const unsigned int selector_action_size;
 extern uint8_t shadow_selector_action_start[];
 extern const unsigned int shadow_selector_action_size;
 extern uint8_t shadow_selector_html_start[];
 extern const unsigned int shadow_selector_html_size;
 extern uint8_t toolbox_action_start[];
 extern const unsigned int toolbox_action_size;
 extern uint8_t toolbox_api_start[];
 extern const unsigned int toolbox_api_size;
 extern uint8_t shadowmount_start[];
 extern const unsigned int shadowmount_size;
 extern uint8_t shadowmount_experimental_start[];
 extern const unsigned int shadowmount_experimental_size;
 extern uint8_t apr_emu_updater_start[];
 extern const unsigned int apr_emu_updater_size;
 extern uint8_t backpork_start[];
 extern const unsigned int backpork_size;
 extern uint8_t garlic_savemgr_start[];
 extern const unsigned int garlic_savemgr_size;
 extern uint8_t fw_spoof_start[];
 extern const unsigned int fw_spoof_size;
 extern uint8_t airpsx_start[];
 extern const unsigned int airpsx_size;
 extern uint8_t ps5upload_start[];
 extern const unsigned int ps5upload_size;
 extern uint8_t np_fake_signin_start[];
 extern const unsigned int np_fake_signin_size;
 extern uint8_t wkali_start[];
 extern const unsigned int wkali_size;
 extern uint8_t app_dumper_start[];
 extern const unsigned int app_dumper_size;
 extern uint8_t game_compressor_start[];
 extern const unsigned int game_compressor_size;
 extern uint8_t web_file_manager_start[];
 extern const unsigned int web_file_manager_size;
 extern uint8_t linux_loader_start[];
 extern const unsigned int linux_loader_size;
 extern uint8_t pegasus_dl_start[];
 extern const unsigned int pegasus_dl_size;
 extern uint8_t spectrum_library_start[];
 extern const unsigned int spectrum_library_size;
 extern uint8_t remote_play_start[];
 extern const unsigned int remote_play_size;
 extern uint8_t optional_prospero_start[];
 extern const unsigned int optional_prospero_size;
 extern uint8_t optional_psplay_start[];
 extern const unsigned int optional_psplay_size;
 extern uint8_t optional_bfplayer_start[];
 extern const unsigned int optional_bfplayer_size;
 extern uint8_t chukei_dns_start[];
 extern const unsigned int chukei_dns_size;
 extern uint8_t nanodns_start[];
 extern const unsigned int nanodns_size;
 extern uint8_t unrar_ps5_start[];
 extern const unsigned int unrar_ps5_size;
 extern uint8_t ps_game_state_start[];
 extern const unsigned int ps_game_state_size;
 extern uint8_t ghostpad_start[];
 extern const unsigned int ghostpad_size;
 extern uint8_t ghostcontrol_start[];
 extern const unsigned int ghostcontrol_size;
 extern uint8_t ps_discord_start[];
 extern const unsigned int ps_discord_size;
 extern uint8_t custom_tool_manager_start[];
 extern const unsigned int custom_tool_manager_size;
 extern uint8_t wallpaper_modder_start[];
 extern const unsigned int wallpaper_modder_size;
 extern uint8_t ftpsrv_start[];
 extern const unsigned int ftpsrv_size;
 extern uint8_t ps5debug_ng_start[];
 extern const unsigned int ps5debug_ng_size;
 extern uint8_t webman_icon_start[];
 extern const unsigned int webman_icon_size;
 extern uint8_t itemzflow_theme_start[];
 extern const unsigned int itemzflow_theme_size;
 extern uint8_t toolbox_shortcut_icon_start[];
 extern const unsigned int toolbox_shortcut_icon_size;
 extern uint8_t toolbox_shortcut_param_start[];
 extern const unsigned int toolbox_shortcut_param_size;
 extern uint8_t toolbox_launcher_html_start[];
 extern const unsigned int toolbox_launcher_html_size;
 extern uint8_t debug_services_shortcut_param_start[];
 extern const unsigned int debug_services_shortcut_param_size;
 extern uint8_t debug_services_launcher_html_start[];
 extern const unsigned int debug_services_launcher_html_size;

 int sceAppInstUtilInitialize(void);
 int sceAppInstUtilTerminate(void);
 int sceAppInstUtilAppInstallAll(void *);
 int sceAppInstUtilAppUnInstall(const char *);

 extern uint8_t fps_prx_start[];
 extern const unsigned int fps_prx_size;

int sceNotificationSend(int userId, bool isLogged, const char* payload);
 }

 
const char json_payload[] =
     "{\n"
     "  \"rawData\": {\n"
     "    \"viewTemplateType\": \"InteractiveToastTemplateB\",\n"
     "    \"channelType\": \"Downloads\",\n"
     "    \"useCaseId\": \"IDC\",\n"
     "    \"toastOverwriteType\": \"No\",\n"
     "    \"isImmediate\": true,\n"
     "    \"priority\": 100,\n"
     "    \"viewData\": {\n"
     "      \"icon\": {\n"
     "        \"type\": \"Url\",\n"
     "        \"parameters\": {\n"
     "          \"url\": \"/user/data/PIZZA_HEN/pizzahen.png\"\n"
     "        }\n"
     "      },\n"
     "      \"message\": {\n"
     "        \"body\": \"PIZZA HEN is starting...\"\n"
     "      },\n"
     "      \"subMessage\": {\n"
     "        \"body\": \"Choose a KStuff engine when the selector opens\"\n"
     "      },\n"
     "      \"actions\": []\n"
     "    },\n"
     "    \"platformViews\": {\n"
     "      \"previewDisabled\": {\n"
     "        \"viewData\": {\n"
     "          \"icon\": {\n"
     "            \"type\": \"Predefined\",\n"
     "            \"parameters\": {\n"
     "              \"icon\": \"download\"\n"
     "            }\n"
     "          },\n"
     "          \"message\": {\n"
     "            \"body\": \"PIZZA HEN is starting...\"\n"
     "          }\n"
     "        }\n"
     "      }\n"
     "    }\n"
     "  },\n"
     "  \"createdDateTime\": \"2025-12-14T03:14:51.473Z\",\n"
     "  \"localNotificationId\": \"588193127\"\n"
     "}";
 
 /******************************************************************************
  * Macros and Constants
  ******************************************************************************/
 #define QAFLAGS_SIZE 16
 #define USER_SERVICE_ID 0x80000011
 #define SYSTEM_SERVICE_ID 0x80000010
 #define LNC_UTIL_ERROR_ALREADY_RUNNING 0x8094000c
 #define LNC_ERROR_APP_NOT_FOUND 0x80940031
 #define ENTRYPOINT_OFFSET 0x70
 
 #define PROCESS_LAUNCHED 1
 
 #define LOOB_BUILDER_SIZE 21
 #define LOOP_BUILDER_TARGET_OFFSET 3
 
 #define USLEEP_NID "QcteRwbsnV0"
 
 #define LOOKUP_SYMBOL(resolver, sym) \
   resolver_lookup_symbol(resolver, sym, strlen(sym))
   
 #define SET_FUNCTION_ADDRESS(resolver, function) \
   *(void **)&(function) = \
       (void *)LOOKUP_SYMBOL(resolver, #function) /* NOLINT */
 
 #define BUILD_IOVEC(str) \
   { .iov_base = (str), .iov_length = __builtin_strlen(str) + 1 }
 
 /******************************************************************************
  * Type Definitions and Structures
  ******************************************************************************/
 typedef struct {
   int32_t type;             // 0x00
   int32_t req_id;           // 0x04
   int32_t priority;         // 0x08
   int32_t msg_id;           // 0x0C
   int32_t target_id;        // 0x10
   int32_t user_id;          // 0x14
   int32_t unk1;             // 0x18
   int32_t unk2;             // 0x1C
   int32_t app_id;           // 0x20
   int32_t error_num;        // 0x24
   int32_t unk3;             // 0x28
   char use_icon_image_uri;  // 0x2C
   char message[1024];       // 0x2D
   char uri[1024];           // 0x42D
   char unkstr[1024];        // 0x82D
 } OrbisNotificationRequest; // Size = 0xC30
 
 typedef enum {
   Flag_None = 0,
   SkipLaunchCheck = 1,
   SkipResumeCheck = 1,
   SkipSystemUpdateCheck = 2,
   RebootPatchInstall = 4,
   VRMode = 8,
   NonVRMode = 16,
   Pft = 32UL,
   RaIsConfirmed = 64UL,
   ShellUICheck = 128UL
 } Flag;
 
 typedef struct {
   uint32_t sz;
   int user_id;
   uint32_t app_opt;
   uint64_t crash_report;
   Flag check_flag;
 } LncAppParam;
 
 typedef struct {
   const void *iov_base;
   size_t iov_length;
 } iovec_t;
 
 typedef struct FileDescriptors {
   int fd = 1;
 } FileDescriptor;
 
 typedef struct {
   uint64_t pad0;
   char version_str[0x1C];
   uint32_t version;
   uint64_t pad1;
 } OrbisKernelSwVersion;
 
 typedef struct {
   char prefix[14];  // "etaHEN_PLUGIN" + null terminator
   char titleID[10]; // 4 uppercase letters, 5 numbers, and a null terminator
   char plugin_version[5];
 } CustomPluginHeader;
 
 typedef struct app_info {
   uint32_t app_id;
   uint64_t unknown1;
   uint32_t app_type;
   char     title_id[10];
   char     unknown2[0x3c];
 } app_info_t;
 
 /******************************************************************************
  * External Declarations
  ******************************************************************************/
 extern "C" {
     int sceKernelSendNotificationRequest(int32_t device,
                                          OrbisNotificationRequest *req,
                                          size_t size, int32_t blocking);
     int sceUserServiceGetForegroundUser(uint32_t *userId);
     int sceLncUtilLaunchApp(const char *tid, const char *argv[],
                             LncAppParam *param);
     uint32_t sceLncUtilKillApp(uint32_t appId);
     int sceSystemServiceGetAppId(const char *titleId);
     int sceUserServiceInitialize(void *param);
     int sceNetCtlInit(void);
     int sceKernelGetProsperoSystemSwVersion(OrbisKernelSwVersion *sw);
     int unmount(const char *path, int flags);
     int sceKernelGetAppInfo(int pid, app_info_t *title);
     int sceKernelGetProcessName(int pid, char *name);
     int sceKernelGetOpenPsIdForSystem(void *psid);
     int sceKernelIsGenuineDevKit();

     bool devkit_byepervisor(void);
     void notify(const char *text, ...) {
      OrbisNotificationRequest req;
      va_list args;
    
      memset(&req, 0, sizeof(OrbisNotificationRequest));
    
      // Process args
      va_start(args, text);
      vsnprintf(req.message, sizeof(req.message), text, args);
      va_end(args);
    
      req.type = 0;
      req.unk3 = 0;
      req.use_icon_image_uri = 1;
      req.target_id = -1;
      snprintf(req.uri, sizeof(req.uri), "cxml://psnotification/tex_icon_system");
    
      printf("Notify: %s\n", req.message);
      sceKernelSendNotificationRequest(0, &req, sizeof(req), 0);
    }

    void ui_trace(const char *text, ...) {
      char line[1024] = {0};
      va_list args;
      va_start(args, text);
      vsnprintf(line, sizeof(line), text, args);
      va_end(args);
      printf("PIZZA HEN UI: %s\n", line);
    }
    
 }
 
 extern int _write(int fd, const void *, size_t); // NOLINT
 extern ssize_t _read(int, void *, size_t);       // NOLINT
 
 extern const unsigned int daemon_size;
 extern uint8_t daemon_start[];
 extern uint8_t util_start[];
 extern const unsigned int util_size;
 extern uint8_t store_png_start;
 extern const unsigned int store_png_size;
 extern uint8_t sicon_start[];
 extern const unsigned int sicon_size;
 extern uint8_t webman_icon_start[];
 extern const unsigned int webman_icon_size;
 
 /******************************************************************************
  * Global Variables
  ******************************************************************************/
 int plugin_count = 0;
 char buff[255];
 char **loaded_filenames = NULL;
 jmp_buf g_catch_buf;
 FileDescriptor sock;
 
 // Constants
 static const int LOGGER_PORT = 9021;
 static const int STDOUT = 1;
 static const int STDERR = 2;
 
 /******************************************************************************
  * Function Prototypes
  ******************************************************************************/
 void write_embedded_assets();
 bool if_exists(const char *path);
 void notify(const char *text, ...);
static void cleanup(void);
 FileDescriptor FileDescriptor_init(int fd);
 int initStdout();
 void release(FileDescriptor *fd);
 pid_t find_pid(const char *name);
 void patch_app_db(void);
 bool is_valid_plugin(const unsigned char *file_buffer);
 uint8_t *get_elf_header_address(unsigned char *file_buffer);
 static bool remount(const char *dev, const char *path);
 
 /******************************************************************************
  * Function Implementations
  ******************************************************************************/
  static bool write_blob_file(const char *path, const void *data, size_t size, mode_t mode) {
      int fd = open(path, O_WRONLY | O_CREAT | O_TRUNC, mode);
      if (fd < 0) return false;
      const uint8_t *p = (const uint8_t *)data;
      size_t left = size;
      while (left) {
          ssize_t n = write(fd, p, left);
          if (n <= 0) { close(fd); return false; }
          p += n;
          left -= (size_t)n;
      }
      fsync(fd);
      close(fd);
      return true;
  }


  /* R7.25.2.10: PS-Play can leave a generated launcher source under
     /data/homebrew/ProsperoPlayer.  Pristine ShadowMountPlus scans
     /data/homebrew and emits "Installing: PS Play (PRSP10001)..." for that
     stale source.  Keep both payload ELFs and ShadowMountPlus unchanged;
     remove only the generated launcher when its param.json identifies PS Play. */
  static bool text_file_contains_two(const char *path, const char *a, const char *b) {
      if (!path || !a || !b) return false;
      int fd = open(path, O_RDONLY);
      if (fd < 0) return false;
      struct stat st{};
      if (fstat(fd, &st) != 0 || st.st_size <= 0 || st.st_size > 65536) { close(fd); return false; }
      size_t size = (size_t)st.st_size;
      char *buf = (char *)malloc(size + 1);
      if (!buf) { close(fd); return false; }
      size_t got = 0;
      while (got < size) {
          ssize_t n = read(fd, buf + got, size - got);
          if (n <= 0) break;
          got += (size_t)n;
      }
      close(fd);
      buf[got] = '\0';
      bool match = got == size && strstr(buf, a) != nullptr && strstr(buf, b) != nullptr;
      free(buf);
      return match;
  }

  static void cleanup_shadowmount_psplay_generated_source(void) {
      const char *root = "/data/homebrew/ProsperoPlayer";
      const char *param = "/data/homebrew/ProsperoPlayer/sce_sys/param.json";
      if (!text_file_contains_two(param, "PRSP10001", "PS Play")) return;
      klog_puts("PIZZA HEN: removing stale PS Play launcher source before ShadowMount scan");
      unlink("/data/homebrew/ProsperoPlayer/eboot.elf");
      unlink("/data/homebrew/ProsperoPlayer/sce_sys/icon0.png");
      unlink(param);
      rmdir("/data/homebrew/ProsperoPlayer/sce_sys");
      rmdir(root);
  }

  // FIX30: one-time Media Contents shortcut, based on the same public
  // AppInstUtil title-directory registration pattern used by PS5 payload tools.
  // The shortcut contains no payload logic: it opens the already-running local
  // websrv page, which redirects to the native PIZZA HEN Toolbox in Debug Settings.
  static int shortcut_needs_update(const char *path, const uint8_t *expected, size_t expected_size) {
      struct stat st{};
      if (stat(path, &st) != 0) return 1;
      if ((size_t)st.st_size != expected_size) return 1;

      int fd = open(path, O_RDONLY);
      if (fd < 0) return 1;
      uint8_t *buf = (uint8_t *)malloc(expected_size ? expected_size : 1);
      if (!buf) { close(fd); return 1; }

      size_t got = 0;
      while (got < expected_size) {
          ssize_t n = read(fd, buf + got, expected_size - got);
          if (n <= 0) { free(buf); close(fd); return 1; }
          got += (size_t)n;
      }
      close(fd);
      int mismatch = memcmp(buf, expected, expected_size);
      free(buf);
      return mismatch != 0;
  }

  static bool shortcut_param_is_legacy_non_media(const char *path) {
      int fd = open(path, O_RDONLY);
      if (fd < 0) return false;
      char buf[4096];
      ssize_t n = read(fd, buf, sizeof(buf) - 1);
      close(fd);
      if (n <= 0) return false;
      buf[n] = 0;
      const char *cat = strstr(buf, "\"applicationCategoryType\"");
      return !cat || !strstr(cat, "65536");
  }

  static void media_tile_status(const char *stage, int rc) {
      mkdir("/data/PIZZA_HEN/runtime", 0777);
      char status[256] = {0};
      int n = snprintf(status, sizeof(status),
                       "stage=%s\nrc=0x%08X\ntitleId=PZHN00001\ncategory=65536\ntitleIdFormat=AAAA99999\n",
                       stage ? stage : "unknown", (unsigned int)rc);
      if (n > 0)
          write_blob_file("/data/PIZZA_HEN/runtime/media_tile_status.txt",
                          status, (size_t)n, 0666);
  }

  // FIX34: initialize the same user/network services that the known-good
  // ps5-payload-manager 0.5.1 initializes before its app-tile installer.
  // "already initialized" return values are diagnostic only; AppInstUtil
  // remains the authoritative success/failure gate.
  static void prepare_media_tile_services(void) {
      int net_rc = sceNetCtlInit();
      int user_prio = 256;
      int user_rc = sceUserServiceInitialize(&user_prio);
      ui_trace("PIZZA HEN TPRE: sceNetCtlInit rc=0x%X, sceUserServiceInitialize rc=0x%X",
               net_rc, user_rc);
  }

  // FIX34: Media tile registration is deliberately retryable.
  // A directory containing matching param/icon files is NOT proof that
  // AppInstUtil registration succeeded. The success marker is written only
  // after AppInstallTitleDir/AppInstallAll returns 0. If registration fails,
  // the marker is removed so the next PIZZA HEN launch retries the DB install.
  // FIX34: FIX30-FIX33 used PIZZA0001. That is not a valid PS title-id
  // shape (working homebrew launchers use four letters followed by five digits).
  // Clean up only our stale, unregistered launcher files before installing the
  // corrected PZHN00001 entry. This does not touch any other app/title.
  static void cleanup_legacy_invalid_pizzahen_tile(void) {
      static const char *legacy_dir = "/user/app/PIZZA0001";
      if (!if_exists(legacy_dir)) return;

      // AppUnInstall may reject the legacy malformed title id; file cleanup is
      // therefore explicit and limited to the files PIZZA HEN itself created.
      int unrc = sceAppInstUtilAppUnInstall("PIZZA0001");
      ui_trace("PIZZA HEN TLEGACY: malformed tile uninstall rc=0x%X", unrc);
      unlink("/user/app/PIZZA0001/.pizzahen_media_registered");
      unlink("/user/app/PIZZA0001/sce_sys/param.json");
      unlink("/user/app/PIZZA0001/sce_sys/icon0.png");
      rmdir("/user/app/PIZZA0001/sce_sys");
      rmdir("/user/app/PIZZA0001");
  }

  static int install_pizzahen_toolbox_shortcut(void) {
      static const char *title_id = "PZHN00001";
      static const char *app_dir = "/user/app/PZHN00001";
      static const char *sys_dir = "/user/app/PZHN00001/sce_sys";
      static const char *param_path = "/user/app/PZHN00001/sce_sys/param.json";
      static const char *icon_path = "/user/app/PZHN00001/sce_sys/icon0.png";
      static const char *registered_marker =
          "/user/app/PZHN00001/.pizzahen_media_registered";

      bool files_need_update = !if_exists(app_dir) ||
          shortcut_needs_update(param_path, toolbox_shortcut_param_start,
                                toolbox_shortcut_param_size) ||
          shortcut_needs_update(icon_path, toolbox_shortcut_icon_start,
                                toolbox_shortcut_icon_size);
      bool registration_needed = !if_exists(registered_marker);

      if (!files_need_update && !registration_needed) {
          ui_trace("PIZZA HEN T0: Media Toolbox tile files + registration marker current");
          media_tile_status("already_registered", 0);
          return 0;
      }

      prepare_media_tile_services();

      int rc = sceAppInstUtilInitialize();
      if (rc != 0) {
          ui_trace("PIZZA HEN T1: sceAppInstUtilInitialize rc=0x%X", rc);
          unlink(registered_marker);
          media_tile_status("appinst_init_failed", rc);
          return rc;
      }

      cleanup_legacy_invalid_pizzahen_tile();

      // Migrate any old pre-FIX34 non-Media registration before rewriting.
      if (if_exists(app_dir) && shortcut_param_is_legacy_non_media(param_path)) {
          unlink(registered_marker);
          int unrc = sceAppInstUtilAppUnInstall(title_id);
          ui_trace("PIZZA HEN T1M: legacy tile migration uninstall rc=0x%X", unrc);
      }

      mkdir("/user/app", 0755);
      if (mkdir(app_dir, 0755) != 0 && errno != EEXIST) {
          rc = -1;
          media_tile_status("mkdir_app_failed", errno);
          goto done;
      }
      if (mkdir(sys_dir, 0755) != 0 && errno != EEXIST) {
          rc = -1;
          media_tile_status("mkdir_sce_sys_failed", errno);
          goto done;
      }

      // Always rewrite assets when the files differ. If only the registration
      // marker is missing, leave matching files alone and retry the DB registration.
      if (files_need_update) {
          if (!write_blob_file(param_path, toolbox_shortcut_param_start,
                               toolbox_shortcut_param_size, 0644) ||
              !write_blob_file(icon_path, toolbox_shortcut_icon_start,
                               toolbox_shortcut_icon_size, 0644)) {
              ui_trace("PIZZA HEN T2: unable to write Media Toolbox tile assets");
              rc = -1;
              media_tile_status("asset_write_failed", rc);
              goto done;
          }
      }

      {
          int (*sceAppInstUtilAppInstallTitleDir)(const char *, const char *, void *) = nullptr;
          uint32_t handle = 0;
          if (!kernel_dynlib_handle(-1, "libSceAppInstUtil.sprx", &handle)) {
              sceAppInstUtilAppInstallTitleDir =
                  reinterpret_cast<int (*)(const char *, const char *, void *)>(
                      kernel_dynlib_resolve(-1, handle, "Wudg3Xe3heE"));
          }

          if (sceAppInstUtilAppInstallTitleDir)
              rc = sceAppInstUtilAppInstallTitleDir(title_id, "/user/app/", nullptr);
          else
              rc = sceAppInstUtilAppInstallAll(nullptr);
      }

      if (rc != 0) {
          unlink(registered_marker);
          ui_trace("PIZZA HEN T3: Media Toolbox tile registration rc=0x%X", rc);
          media_tile_status("registration_failed", rc);
      } else {
          static const char marker[] = "PIZZA_HEN_MEDIA_TILE_V1\n";
          write_blob_file(registered_marker, marker, sizeof(marker) - 1, 0644);
          ui_trace("PIZZA HEN T4: Media Toolbox tile installed/updated (PZHN00001)");
          media_tile_status("registered", 0);
      }

done:
      sceAppInstUtilTerminate();
      return rc;
  }

  // R3: second Media tile. The Debug Services tile does not route through the
  // latest Toolbox UI. It opens a byte-exact copy of the PIZZA HEN v0.1
  // launcher page, which invokes the original pizzahen-toolbox-open.elf helper.
  static void debug_services_tile_status(const char *stage, int rc) {
      mkdir("/data/PIZZA_HEN/runtime", 0777);
      char status[256] = {0};
      int n = snprintf(status, sizeof(status),
                       "stage=%s\nrc=0x%08X\ntitleId=PZHN00002\ncategory=65536\ntitleIdFormat=AAAA99999\n",
                       stage ? stage : "unknown", (unsigned int)rc);
      if (n > 0)
          write_blob_file("/data/PIZZA_HEN/runtime/debug_services_tile_status.txt",
                          status, (size_t)n, 0666);
  }

  static int install_pizzahen_debug_services_shortcut(void) {
      static const char *title_id = "PZHN00002";
      static const char *app_dir = "/user/app/PZHN00002";
      static const char *sys_dir = "/user/app/PZHN00002/sce_sys";
      static const char *param_path = "/user/app/PZHN00002/sce_sys/param.json";
      static const char *icon_path = "/user/app/PZHN00002/sce_sys/icon0.png";
      static const char *registered_marker =
          "/user/app/PZHN00002/.pizzahen_debug_services_registered";

      bool files_need_update = !if_exists(app_dir) ||
          shortcut_needs_update(param_path, debug_services_shortcut_param_start,
                                debug_services_shortcut_param_size) ||
          shortcut_needs_update(icon_path, toolbox_shortcut_icon_start,
                                toolbox_shortcut_icon_size);
      bool registration_needed = !if_exists(registered_marker);

      if (!files_need_update && !registration_needed) {
          ui_trace("PIZZA HEN TD0: Debug Services Media tile files + registration marker current");
          debug_services_tile_status("already_registered", 0);
          return 0;
      }

      prepare_media_tile_services();
      int rc = sceAppInstUtilInitialize();
      if (rc != 0) {
          ui_trace("PIZZA HEN TD1: sceAppInstUtilInitialize rc=0x%X", rc);
          unlink(registered_marker);
          debug_services_tile_status("appinst_init_failed", rc);
          return rc;
      }

      mkdir("/user/app", 0755);
      if (mkdir(app_dir, 0755) != 0 && errno != EEXIST) {
          rc = -1;
          debug_services_tile_status("mkdir_app_failed", errno);
          goto done_debug_services;
      }
      if (mkdir(sys_dir, 0755) != 0 && errno != EEXIST) {
          rc = -1;
          debug_services_tile_status("mkdir_sce_sys_failed", errno);
          goto done_debug_services;
      }

      if (files_need_update) {
          if (!write_blob_file(param_path, debug_services_shortcut_param_start,
                               debug_services_shortcut_param_size, 0644) ||
              !write_blob_file(icon_path, toolbox_shortcut_icon_start,
                               toolbox_shortcut_icon_size, 0644)) {
              ui_trace("PIZZA HEN TD2: unable to write Debug Services Media tile assets");
              rc = -1;
              debug_services_tile_status("asset_write_failed", rc);
              goto done_debug_services;
          }
      }

      {
          int (*sceAppInstUtilAppInstallTitleDir)(const char *, const char *, void *) = nullptr;
          uint32_t handle = 0;
          if (!kernel_dynlib_handle(-1, "libSceAppInstUtil.sprx", &handle)) {
              sceAppInstUtilAppInstallTitleDir =
                  reinterpret_cast<int (*)(const char *, const char *, void *)>(
                      kernel_dynlib_resolve(-1, handle, "Wudg3Xe3heE"));
          }
          if (sceAppInstUtilAppInstallTitleDir)
              rc = sceAppInstUtilAppInstallTitleDir(title_id, "/user/app/", nullptr);
          else
              rc = sceAppInstUtilAppInstallAll(nullptr);
      }

      if (rc != 0) {
          unlink(registered_marker);
          ui_trace("PIZZA HEN TD3: Debug Services Media tile registration rc=0x%X", rc);
          debug_services_tile_status("registration_failed", rc);
      } else {
          static const char marker[] = "PIZZA_HEN_DEBUG_SERVICES_MEDIA_TILE_V1\n";
          write_blob_file(registered_marker, marker, sizeof(marker) - 1, 0644);
          ui_trace("PIZZA HEN TD4: Debug Services Media tile installed/updated (PZHN00002)");
          debug_services_tile_status("registered", 0);
      }

done_debug_services:
      sceAppInstUtilTerminate();
      return rc;
  }

  static int read_kstuff_request(char *out, size_t out_size) {
      if (!out || out_size < 3) return 0;
      int fd = open("/data/PIZZA_HEN/runtime/kstuff_request.txt", O_RDONLY);
      if (fd < 0) return 0;
      ssize_t n = read(fd, out, out_size - 1);
      close(fd);
      if (n <= 0) return 0;
      out[n] = 0;
      for (ssize_t i = 0; i < n; ++i) {
          if (out[i] == '\r' || out[i] == '\n' || out[i] == ' ' || out[i] == '\t') { out[i] = 0; break; }
      }
      return (!strcmp(out, "lite") || !strcmp(out, "dr") || !strcmp(out, "base"));
  }

  static int read_shadowmount_request(char *out, size_t out_size) {
      if (!out || out_size < 7) return 0;
      int fd = open("/data/PIZZA_HEN/runtime/shadowmount_request.txt", O_RDONLY);
      if (fd < 0) return 0;
      ssize_t n = read(fd, out, out_size - 1);
      close(fd);
      if (n <= 0) return 0;
      out[n] = 0;
      for (ssize_t i = 0; i < n; ++i) {
          if (out[i] == '\r' || out[i] == '\n' || out[i] == ' ' || out[i] == '\t') { out[i] = 0; break; }
      }
      return (!strcmp(out, "stable") || !strcmp(out, "experimental") || !strcmp(out, "skip"));
  }

  static bool kstuff_probe_ready(void) {
      char probe[100] = {0};
      return sceKernelMprotect(&probe[0], sizeof(probe), 0x7) >= 0;
  }

  // FIX25: Payload-Manager-style selector transport.
  // Start the frozen websrv locally, wait until 127.0.0.1:8080 accepts
  // connections, then ask the PS5 system service to open the browser directly
  // on the dedicated PIZZA HEN selector page. No fake app and no ShellUI
  // injection are involved in the primary selector path.
  static int wait_for_local_websrv(int timeout_ms) {
      int elapsed = 0;
      while (elapsed <= timeout_ms) {
          int fd = socket(AF_INET, SOCK_STREAM, 0);
          if (fd >= 0) {
              struct sockaddr_in sa{};
              sa.sin_family = AF_INET;
              sa.sin_port = htons(8080);
              sa.sin_addr.s_addr = inet_addr("127.0.0.1");
              if (connect(fd, (struct sockaddr *)&sa, sizeof(sa)) == 0) {
                  close(fd);
                  return 1;
              }
              close(fd);
          }
          usleep(200 * 1000);
          elapsed += 200;
      }
      return 0;
  }

  // FIX26: readiness gate for upstream ftpsrv v0.21. The upstream payload
  // listens on TCP/2121 by default, so a successful loopback connect is a
  // concrete service-ready signal before the bootstrap pipeline advances.
  static int wait_for_local_ftpsrv(int timeout_ms) {
      int elapsed = 0;
      while (elapsed <= timeout_ms) {
          int fd = socket(AF_INET, SOCK_STREAM, 0);
          if (fd >= 0) {
              struct sockaddr_in sa{};
              sa.sin_family = AF_INET;
              sa.sin_port = htons(2121);
              sa.sin_addr.s_addr = inet_addr("127.0.0.1");
              if (connect(fd, (struct sockaddr *)&sa, sizeof(sa)) == 0) {
                  close(fd);
                  return 1;
              }
              close(fd);
          }
          usleep(200 * 1000);
          elapsed += 200;
      }
      return 0;
  }

  // FIX27: readiness gate for upstream ps5debug-NG v1.3.0.
  // Port 744 is the upstream command server, so accepting a loopback TCP
  // connection is the service-ready signal used by the PIZZA HEN pipeline.
  static int wait_for_local_ps5debug_ng(int timeout_ms) {
      int elapsed = 0;
      while (elapsed <= timeout_ms) {
          int fd = socket(AF_INET, SOCK_STREAM, 0);
          if (fd >= 0) {
              struct sockaddr_in sa{};
              sa.sin_family = AF_INET;
              sa.sin_port = htons(744);
              sa.sin_addr.s_addr = inet_addr("127.0.0.1");
              if (connect(fd, (struct sockaddr *)&sa, sizeof(sa)) == 0) {
                  close(fd);
                  return 1;
              }
              close(fd);
          }
          usleep(250 * 1000);
          elapsed += 250;
      }
      return 0;
  }

  static int start_browser_kstuff_selector(void) {
      unlink("/data/PIZZA_HEN/runtime/kstuff_request.txt");
      unlink("/data/PIZZA_HEN/runtime/kstuff_request.tmp");

      if (!wait_for_local_websrv(200)) {
          if (websrv_size < 4 || websrv_start[0] != 0x7f ||
              websrv_start[1] != 'E' || websrv_start[2] != 'L' ||
              websrv_start[3] != 'F') {
              return -20;
          }
          signal(SIGCHLD, SIG_DFL);
          int pid = elfldr_spawn("/", STDOUT_FILENO, websrv_start, "websrv.elf");
          if (pid < 0) return -21;
          if (!wait_for_local_websrv(12000)) return -22;
      }

      static const char selector_url[] =
          "http://127.0.0.1:8080/fs/data/PIZZA_HEN/ui/kstuff-selector.html";
      int rc = sceSystemServiceLaunchWebBrowser(selector_url);
      if (rc != 0) return rc;
      return 0;
  }

  static int wait_for_web_kstuff_request(char *choice, size_t choice_size) {
      // Optional fallback only. websrv does not register or launch a dashboard app.
      // The user may open the existing selector page from another device on the LAN.
      for (int i = 0; i < 180; ++i) {
          if (read_kstuff_request(choice, choice_size)) return 1;
          sleep(1);
      }
      return 0;
  }

  static int start_browser_shadowmount_selector(void) {
      // The KStuff page hands the same browser view to this URL as soon as
      // kstuff_active.txt appears. Launching it again here is intentional:
      // it also covers sessions where KStuff was already active before PIZZA HEN.
      if (!wait_for_local_websrv(12000)) return -30;
      static const char selector_url[] =
          "http://127.0.0.1:8080/fs/data/PIZZA_HEN/ui/shadowmount-selector.html";
      return sceSystemServiceLaunchWebBrowser(selector_url);
  }

  static int wait_for_web_shadowmount_request(char *choice, size_t choice_size) {
      for (int i = 0; i < 180; ++i) {
          if (read_shadowmount_request(choice, choice_size)) return 1;
          sleep(1);
      }
      return 0;
  }

  void write_embedded_assets() {
    mkdir("/data/PIZZA_HEN/", 0777);
    mkdir("/data/PIZZA_HEN/assets/", 0777);
    mkdir("/data/PIZZA_HEN/bin/", 0777);
    mkdir("/data/PIZZA_HEN/payloads/", 0777);
    mkdir("/data/PIZZA_HEN/engines/", 0777);
    mkdir("/data/PIZZA_HEN/runtime/", 0777);
    mkdir("/data/PIZZA_HEN/ui/", 0777);
    mkdir("/data/PIZZA_HEN/themes/", 0777);
    mkdir("/data/PIZZA_HEN/themes/itemzflow/", 0777);
    mkdir("/data/PIZZA_HEN/builtin/", 0777);
    mkdir("/data/homebrew/", 0777);
    mkdir("/data/homebrew/000_PIZZA_HEN_KSTUFF_SELECTOR/", 0777);
    mkdir("/data/homebrew/000_PIZZA_HEN_KSTUFF_SELECTOR/sce_sys/", 0777);

    // R7.18: write the three frozen KStuff engines plus the websrv selector bridge.
    write_blob_file("/data/PIZZA_HEN/engines/kstuff-lite-1.10.elf",
                    &kstuff_start, kstuff_size, 0777);
    write_blob_file("/data/PIZZA_HEN/engines/kstuff-dr-1.2-test1.elf",
                    &kstuff_dr_start, kstuff_dr_size, 0777);
    write_blob_file("/data/PIZZA_HEN/engines/kstuff-base-1.6.7.elf",
                    &kstuff_base_start, kstuff_base_size, 0777);
    write_blob_file("/data/PIZZA_HEN/bin/pizzahen-kstuff-select.elf",
                    &selector_action_start, selector_action_size, 0777);
    write_blob_file("/data/PIZZA_HEN/bin/pizzahen-shadowmount-select.elf",
                    &shadow_selector_action_start, shadow_selector_action_size, 0777);
    write_blob_file("/data/PIZZA_HEN/payloads/apr_emu_updater.elf",
                    &apr_emu_updater_start, apr_emu_updater_size, 0777);
    write_blob_file("/data/PIZZA_HEN/payloads/ps5-backpork.elf",
                    &backpork_start, backpork_size, 0777);
    write_blob_file("/data/PIZZA_HEN/payloads/garlic-savemgr.elf",
                    &garlic_savemgr_start, garlic_savemgr_size, 0777);
    write_blob_file("/data/PIZZA_HEN/payloads/ps5-fw-spoof_v26616621599.elf",
                    &fw_spoof_start, fw_spoof_size, 0777);
    write_blob_file("/data/PIZZA_HEN/payloads/airpsx_v0.19.elf",
                    &airpsx_start, airpsx_size, 0777);
    write_blob_file("/data/PIZZA_HEN/payloads/ps5upload_v5.4.8.elf",
                    &ps5upload_start, ps5upload_size, 0777);
    write_blob_file("/data/PIZZA_HEN/payloads/np-fake-signin_v1.3.elf",
                    &np_fake_signin_start, np_fake_signin_size, 0777);
    write_blob_file("/data/PIZZA_HEN/payloads/webkit-autoloader-installer_v0.4.0-pre-00e1028.elf",
                    &wkali_start, wkali_size, 0777);
    write_blob_file("/data/PIZZA_HEN/payloads/ps5-app-dumper_v1.11.elf",
                    &app_dumper_start, app_dumper_size, 0777);
    write_blob_file("/data/PIZZA_HEN/payloads/game-compressor.elf",
                    &game_compressor_start, game_compressor_size, 0777);
    write_blob_file("/data/PIZZA_HEN/payloads/web-file-mgr.elf",
                    &web_file_manager_start, web_file_manager_size, 0777);
    write_blob_file("/data/PIZZA_HEN/payloads/ps5-linux-loader.elf",
                    &linux_loader_start, linux_loader_size, 0777);
    write_blob_file("/data/PIZZA_HEN/payloads/pegasus-dl.elf",
                    &pegasus_dl_start, pegasus_dl_size, 0777);
    write_blob_file("/data/PIZZA_HEN/payloads/Spectrum-Library.elf",
                    &spectrum_library_start, spectrum_library_size, 0777);
    write_blob_file("/data/PIZZA_HEN/payloads/rp-get-pin.elf",
                    &remote_play_start, remote_play_size, 0777);
    /* R7.25.1: original media-player ELFs are deployed as ordinary PIZZA HEN
       services. They are never launched here; the user controls them from
       Services with the same start/stop mechanism as other on-demand ELFs. */
    write_blob_file("/data/PIZZA_HEN/payloads/ProsperoPlayer_v1.0.elf",
                    &optional_prospero_start, optional_prospero_size, 0777);
    write_blob_file("/data/PIZZA_HEN/payloads/PS-Play_v2.1.elf",
                    &optional_psplay_start, optional_psplay_size, 0777);
    write_blob_file("/data/PIZZA_HEN/payloads/BFplayer-standalone_v0.1.0-alpha.44.elf",
                    &optional_bfplayer_start, optional_bfplayer_size, 0777);
    /* R7.25.2.2: user-supplied DNS ELFs are embedded byte-for-byte and
       exposed only through the standard managed-task service switches. */
    write_blob_file("/data/PIZZA_HEN/payloads/Chukei_DNS_v0.9.0.elf",
                    &chukei_dns_start, chukei_dns_size, 0777);
    write_blob_file("/data/PIZZA_HEN/payloads/nanoDNS_v0.4.elf",
                    &nanodns_start, nanodns_size, 0777);

    /* R7.25.2.7: original user-supplied service payloads. PIZZA HEN only
       embeds/deploys them and exposes the standard Services start/stop UI. */
    write_blob_file("/data/PIZZA_HEN/payloads/unrar-ps5_v1.4.0.elf",
                    &unrar_ps5_start, unrar_ps5_size, 0777);
    write_blob_file("/data/PIZZA_HEN/payloads/PS_Game_State_Lib_v0.1.elf",
                    &ps_game_state_start, ps_game_state_size, 0777);
    write_blob_file("/data/PIZZA_HEN/payloads/Ghostpad_v1.0.0.elf",
                    &ghostpad_start, ghostpad_size, 0777);
    write_blob_file("/data/PIZZA_HEN/payloads/Ghostcontrol-PS5-USB-Controller-Patcher_v1.0.5.elf",
                    &ghostcontrol_start, ghostcontrol_size, 0777);
    write_blob_file("/data/PIZZA_HEN/payloads/PS-DiscordPresence_v0.01.elf",
                    &ps_discord_start, ps_discord_size, 0777);

    /* R7.25.2.6: retire stale boot markers left by older builds.  These tools
       are manual-only in the current Toolbox.  In particular PS-Play contains
       its own launcher installer, so a stale marker must never cause a silent
       boot-time install.  Payload binaries are untouched. */
    const char *manual_only_autostart_markers[] = {
        "/data/PIZZA_HEN/payloads/rp-get-pin.elf.auto_start",
        "/data/PIZZA_HEN/payloads/ps5-linux-loader.elf.auto_start",
        "/data/PIZZA_HEN/payloads/svtplay_v0.2.elf.auto_start",
        "/data/PIZZA_HEN/payloads/ProsperoPlayer_v1.0.elf.auto_start",
        "/data/PIZZA_HEN/payloads/PS-Play_v2.1.elf.auto_start",
        "/data/PIZZA_HEN/payloads/BFplayer-standalone_v0.1.0-alpha.44.elf.auto_start",
        "/data/PIZZA_HEN/payloads/unrar-ps5_v1.4.0.elf.auto_start",
        "/data/PIZZA_HEN/payloads/PS_Game_State_Lib_v0.1.elf.auto_start",
        "/data/PIZZA_HEN/payloads/Ghostpad_v1.0.0.elf.auto_start",
        "/data/PIZZA_HEN/payloads/Ghostcontrol-PS5-USB-Controller-Patcher_v1.0.5.elf.auto_start",
        "/data/PIZZA_HEN/payloads/Remote_Play.elf.auto_start",
        "/data/PIZZA_HEN/payloads/PS-DiscordPresence_v0.01.elf.auto_start",
        "/data/PIZZA_HEN/payloads/garlic-worker_v1.1.6.elf.auto_start",
        "/user/data/PIZZA_HEN/payloads/rp-get-pin.elf.auto_start",
        "/user/data/PIZZA_HEN/payloads/ps5-linux-loader.elf.auto_start",
        "/user/data/PIZZA_HEN/payloads/svtplay_v0.2.elf.auto_start",
        "/user/data/PIZZA_HEN/payloads/ProsperoPlayer_v1.0.elf.auto_start",
        "/user/data/PIZZA_HEN/payloads/PS-Play_v2.1.elf.auto_start",
        "/user/data/PIZZA_HEN/payloads/BFplayer-standalone_v0.1.0-alpha.44.elf.auto_start",
        "/user/data/PIZZA_HEN/payloads/unrar-ps5_v1.4.0.elf.auto_start",
        "/user/data/PIZZA_HEN/payloads/PS_Game_State_Lib_v0.1.elf.auto_start",
        "/user/data/PIZZA_HEN/payloads/Ghostpad_v1.0.0.elf.auto_start",
        "/user/data/PIZZA_HEN/payloads/Ghostcontrol-PS5-USB-Controller-Patcher_v1.0.5.elf.auto_start",
        "/user/data/PIZZA_HEN/payloads/Remote_Play.elf.auto_start",
        "/user/data/PIZZA_HEN/payloads/PS-DiscordPresence_v0.01.elf.auto_start",
        "/user/data/PIZZA_HEN/payloads/garlic-worker_v1.1.6.elf.auto_start",
        nullptr};
    for (const char **marker = manual_only_autostart_markers; *marker; ++marker)
      unlink(*marker);
    /* R7.25.2.8: Remote_Play.elf and garlic-worker_v1.1.6.elf are retired
       from Services. Remove stale copies left by R7.25.2.7 so they cannot
       reappear through the generic payload scanner. */
    unlink("/data/PIZZA_HEN/payloads/Remote_Play.elf");
    unlink("/data/PIZZA_HEN/payloads/garlic-worker_v1.1.6.elf");
    unlink("/user/data/PIZZA_HEN/payloads/Remote_Play.elf");
    unlink("/user/data/PIZZA_HEN/payloads/garlic-worker_v1.1.6.elf");
    /* R7.25.2.5: web-only Themes Avatar payloads. The original web functions
       are preserved; only each payload's self-installer path is disabled in
       the frozen PIZZA-derived ELF so no launcher icon/app is created. */
    write_blob_file("/data/PIZZA_HEN/payloads/PS5-Custom-Tool-Manager-pizza-web-only.elf",
                    &custom_tool_manager_start, custom_tool_manager_size, 0777);
    write_blob_file("/data/PIZZA_HEN/payloads/ps5-wallpaper-modd-pizza-web-only.elf",
                    &wallpaper_modder_start, wallpaper_modder_size, 0777);
    write_blob_file("/data/PIZZA_HEN/bin/pizzahen-toolbox-open.elf",
                    &toolbox_action_start, toolbox_action_size, 0777);
    write_blob_file("/data/PIZZA_HEN/bin/pizzahen-api.elf",
                    &toolbox_api_start, toolbox_api_size, 0777);
    write_blob_file("/data/PIZZA_HEN/ui/kstuff-selector.html",
                    &selector_html_start, selector_html_size, 0666);
    write_blob_file("/data/PIZZA_HEN/ui/shadowmount-selector.html",
                    &shadow_selector_html_start, shadow_selector_html_size, 0666);
    write_blob_file("/data/PIZZA_HEN/ui/toolbox-launcher.html",
                    &toolbox_launcher_html_start, toolbox_launcher_html_size, 0666);
    write_blob_file("/data/PIZZA_HEN/ui/debug-services-launcher.html",
                    &debug_services_launcher_html_start, debug_services_launcher_html_size, 0666);
    write_blob_file("/data/homebrew/000_PIZZA_HEN_KSTUFF_SELECTOR/homebrew.js",
                    &selector_js_start, selector_js_size, 0666);
    write_blob_file("/data/homebrew/000_PIZZA_HEN_KSTUFF_SELECTOR/sce_sys/icon0.png",
                    &selector_icon_start, selector_icon_size, 0666);
    unlink("/data/PIZZA_HEN/runtime/kstuff_request.txt");
    unlink("/data/PIZZA_HEN/runtime/kstuff_request.tmp");
    unlink("/data/PIZZA_HEN/runtime/kstuff_active.txt");
    unlink("/data/PIZZA_HEN/runtime/shadowmount_request.txt");
    unlink("/data/PIZZA_HEN/runtime/shadowmount_request.tmp");
    unlink("/data/PIZZA_HEN/runtime/shadowmount_active.txt");
#if 0
    int fd = open("/system_ex/common_ex/lib/shell.prx", O_WRONLY | O_CREAT | O_TRUNC, 0666);
    if (fd == -1) {
        perror("open failed");
        return;
    }
    if (write(fd, &shellui_prx_start, shellui_prx_size) == -1) {
        perror("write failed");
        return;
    }
    close(fd);
#endif
#if 0
   /// if (!if_exists("/data/PIZZA_HEN/fps.prx")) {
        int fd = open("/data/PIZZA_HEN/fps.prx", O_WRONLY | O_CREAT | O_TRUNC, 0777);
        if (fd == -1) {
            perror("open failed");
            return;
        }
        if (write(fd, &fps_prx_start, fps_prx_size) == -1) {
            perror("write failed");
        }
        close(fd);
  //  }
#endif

    if (!if_exists("/data/PIZZA_HEN/assets/store.png")) {
      int fd = open("/data/PIZZA_HEN/assets/store.png", O_WRONLY | O_CREAT | O_TRUNC, 0666);
      if (fd == -1) {
        perror("open failed");
        return;
      }
      if (write(fd, & store_png_start, store_png_size) == -1) {
        perror("write failed");
      }
      close(fd);
    }

    // PIZZA HEN: update Game Manager/webMAN art when it changes; do not leave
    // an obsolete cached icon on disk.
    if (shortcut_needs_update("/data/PIZZA_HEN/assets/webMAN.png", webman_icon_start, webman_icon_size)) {
      write_blob_file("/data/PIZZA_HEN/assets/webMAN.png", webman_icon_start, webman_icon_size, 0666);
    }

    if (shortcut_needs_update("/data/PIZZA_HEN/themes/itemzflow/background.png", itemzflow_theme_start, itemzflow_theme_size)) {
      write_blob_file("/data/PIZZA_HEN/themes/itemzflow/background.png", itemzflow_theme_start, itemzflow_theme_size, 0666);
    }

    if (!if_exists("/data/PIZZA_HEN/pizzahen.png")) {
      int fd = open("/data/PIZZA_HEN/pizzahen.png", O_WRONLY | O_CREAT | O_TRUNC, 0666);
      if (fd == -1) {
        perror("open failed");
        return;
      }
      if (write(fd, & sicon_start, sicon_size) == -1) {
        perror("write failed");
      }
      close(fd);
    }
 
    if (!if_exists("/system_ex/rnps/apps/NPXS40008/assets/src/modules/categoriesList/assets/texture/pizzahen_sicon.png")) {
      int fd = open("/system_ex/rnps/apps/NPXS40008/assets/src/modules/categoriesList/assets/texture/pizzahen_sicon.png", O_WRONLY | O_CREAT | O_TRUNC, 0666);
      if (fd == -1) {
        perror("open failed");
        return;
      }
      if (write(fd, & sicon_start, sicon_size) == -1) {
        perror("write failed");
      }
      close(fd);
    }
 
    if (!if_exists("/mnt/rnps/apps/NPXS40008/assets/src/modules/categoriesList/assets/texture/pizzahen_sicon.png")) {
      int fd = open("/mnt/rnps/apps/NPXS40008/assets/src/modules/categoriesList/assets/texture/pizzahen_sicon.png", O_WRONLY | O_CREAT | O_TRUNC, 0666);
      if (fd == -1) {
        perror("open failed");
        return;
      }
      if (write(fd, & sicon_start, sicon_size) == -1) {
        perror("write failed");
      }
      close(fd);
    }
}

  bool is_elf_header(uint8_t* data)
  {
      uint8_t header[] = { 0x7f, 'E', 'L', 'F' };

      return !memcmp(data, header, 4);
  }


  uint8_t* get_kstuff_address(bool& require_cleanup) {
      const char* path = PIZZA_HEN_KSTUFF_PATH;
      if (!if_exists(path) && if_exists(PIZZA_HEN_LEGACY_KSTUFF)) {
          path = PIZZA_HEN_LEGACY_KSTUFF;
          ui_trace("PIZZA HEN: using legacy kstuff override: %s", path);
      }
      long offset = 0;
      off_t size;
      uint8_t* address;
      int fd;

      if (!if_exists(path)) {
          goto embedded_kstuff;
      }

      fd = open(path, O_RDONLY);
      if (fd <= 0) {
          goto embedded_kstuff;
      }

      size = lseek(fd, 0, SEEK_END);
      address = (uint8_t*)malloc(size);

      if (!address) {
          goto close_fd;
      }

      lseek(fd, 0, SEEK_SET);

      while (offset != size) {
          int n = read(fd, address + offset, size - offset);

          if (n <= 0)
          {
              goto free_mem;
          }

          offset += n;
      }

      if (!is_elf_header(address)) {
          notify( "Kstuff '%s' doesn't have ELF header.", path);
          goto free_mem;
      }

      require_cleanup = true;
      ui_trace("Loading kstuff from: %s", path);
      return address;

  free_mem:
      free(address);
  close_fd:
      close(fd);
  embedded_kstuff:
      require_cleanup = false;
      return kstuff_start;
  }
 
 bool if_exists(const char *path) {
   struct stat buffer;
   return (stat(path, &buffer) == 0);
 }
 
 static bool remount(const char *dev, const char *path) {
   iovec_t iov[] = {BUILD_IOVEC("fstype"),    BUILD_IOVEC("exfatfs"),
                    BUILD_IOVEC("fspath"),    BUILD_IOVEC(path),
                    BUILD_IOVEC("from"),      BUILD_IOVEC(dev),
                    BUILD_IOVEC("large"),     BUILD_IOVEC("yes"),
                    BUILD_IOVEC("timezone"),  BUILD_IOVEC("static"),
                    BUILD_IOVEC("async"),     {NULL, 0},
                    BUILD_IOVEC("ignoreacl"), {NULL, 0}};
   return nmount((struct iovec *)iov, sizeof(iov) / sizeof(iov[0]),
                 MNT_UPDATE) == 0;
 }
 static void cleanup(void) { 
    if (sock.fd != -1) {
      close(sock.fd);
      sock.fd = -1;
    }
  
    // Notify user about cleanup
    ui_trace("PIZZA HEN has been cleaned up.");
  
    // Exit the program
    exit(0);
 }
 
 // FileDescriptor methods implementations
 FileDescriptor FileDescriptor_init(int fd) {
   FileDescriptor newFd;
   newFd.fd = fd;
   return newFd;
 }
 
 void release(FileDescriptor *fd) { 
   fd->fd = -1; 
 }
 
 // Stdout initialization logic
 int initStdout() {
   // Check for logging file existence logic here
   // For simplicity, I'm assuming it always exists
   char error_msg[500] = {0};
 
   sock.fd = -1;
   sock = FileDescriptor_init(socket(AF_INET, SOCK_STREAM, 0));
   if (sock.fd == -1) {
     snprintf(error_msg, sizeof(error_msg), "Failed to create socket: %s",
              strerror(errno));
     notify(error_msg);
     return -1;
   }
 
   int value = 1;
   if (setsockopt(sock.fd, SOL_SOCKET, SO_REUSEADDR, &value, sizeof(value)) < 0) {
     snprintf(error_msg, sizeof(error_msg), "Failed to set socket options: %s",
              strerror(errno));
     notify(error_msg);
     return -1;
   }
 
   struct sockaddr_in server_addr;
   (void)memset(&server_addr, 0, sizeof(server_addr));
   server_addr.sin_family = AF_INET;
   server_addr.sin_port = htons(LOGGER_PORT);
   server_addr.sin_addr.s_addr = 0;
 
   if (bind(sock.fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) != 0) {
     snprintf(error_msg, sizeof(error_msg), "Failed to bind socket: %s",
              strerror(errno));
     notify(error_msg);
     return -1;
   }
 
   if (listen(sock.fd, 1) != 0) {
     snprintf(error_msg, sizeof(error_msg), "Failed to listen on socket: %s",
              strerror(errno));
     notify(error_msg);
     return -1;
   }
 
   struct sockaddr client_addr;
   socklen_t addr_len = sizeof(client_addr);
   int conn = accept(sock.fd, &client_addr, &addr_len);
   if (conn != -1) {
     dup2(conn, STDOUT);
     dup2(conn, STDERR);
     close(conn);
     return conn;
   }
 
   snprintf(error_msg, sizeof(error_msg), "Failed to accept connection: %s",
            strerror(errno));
   notify(error_msg);
   return -1;
 }
 
 // Function to check if the file buffer contains a valid custom plugin header
 bool is_valid_plugin(const unsigned char *file_buffer) {
   // Check if the prefix matches
   if (strncmp((const char *)file_buffer, "etaHEN_PLUGIN", 13) != 0) {
     puts("Plugin header prefix does not match");
     return false;
   }
 
   // Validate the title ID format (4 uppercase letters followed by 4 numbers)
   const CustomPluginHeader *header = (const CustomPluginHeader *)file_buffer;
   for (int i = 0; i < 4; ++i) {
     if (header->titleID[i] < 'A' || header->titleID[i] > 'Z') {
       puts("Invalid plugin file: titleID must contain 4 uppercase letters as "
            "the start");
       return false;
     }
   }
   for (int i = 4; i < 9; ++i) {
     if (header->titleID[i] < '0' || header->titleID[i] > '9') {
       puts("Invalid plugin file: titleID must contain 5 numbers as the end");
       return false;
     }
   }
 
   // Ensure the title ID is null-terminated
   if (header->titleID[9] != '\0') {
     puts("Invalid plugin file: titleID must be null-terminated");
     return false;
   }
 
   for (int i = 0; i < 3; ++i) {
     if (header->plugin_version[i] == '.') {
       continue;
     } else if (header->plugin_version[i] < '0' ||
                header->plugin_version[i] > '9') {
       puts(
           "Invalid plugin file: version must be in the following format xx.xx");
       return false;
     }
   }
 
   return true;
 }
 
 // Function to return the address of the ELF header, skipping the custom plugin header
 uint8_t *get_elf_header_address(unsigned char *file_buffer) {
   // The ELF header should start right after the custom plugin header
   return file_buffer + sizeof(CustomPluginHeader);
 }
 

pid_t find_pid(const char * name) {
  int mib[4] = {
    CTL_KERN,
    KERN_PROC,
    KERN_PROC_PROC,
    0
  };
  size_t buf_size;
  void * buf;

  int pid = -1;
  // determine size of query response
  if (sysctl(mib, 4, NULL,&buf_size, NULL, 0)) {
    printf("sysctl failed: %s\n", strerror(errno));
    return -1;
  }

  // allocate memory for query response
  if (!(buf = malloc(buf_size))) {
    printf("malloc failed %s\n", strerror(errno));
    return -1;
  }

  // query the kernel for proc info
  if (sysctl(mib, 4, buf,&buf_size, NULL, 0)) {
    printf("sysctl failed: %s\n", strerror(errno));
    free(buf);
    return -1;
  }

  for (char * ptr = static_cast < char * > (buf); ptr < (static_cast < char * > (buf) + buf_size);) {
    struct kinfo_proc * ki = reinterpret_cast < struct kinfo_proc * > (ptr);
    ptr += ki->ki_structsize;

    if(strlen(ki->ki_comm) < 2)
      continue;

    if (strstr(ki->ki_comm, name) != NULL) {
      pid = ki->ki_pid;
      break;
    }
  }

  free(buf);

  return pid;
}

bool is_elf_file(const void* buffer, size_t size) {
    if (size < 4) return false;
    
    const unsigned char elf_magic[] = {0x7F, 'E', 'L', 'F'};
    return memcmp(buffer, elf_magic, 4) == 0;
}


bool load_plugin(const char *path, const char *filename)
{
  int fd = open(path, O_RDONLY);
  if (fd < 0)
  {
    perror("Failed to open file");
    return false;
  }

  struct stat st;
  if (fstat(fd, &st) != 0)
  {
    perror("Failed to get file stats");
    close(fd);
    return false;
  }
  // Allocate buffer and read the entire file.
  uint8_t *buf = (uint8_t *)malloc(st.st_size);
  if (!buf)
  {
    perror("Failed to allocate memory for Plugin file");
    close(fd);
    return false;
  }

  if (read(fd, buf, st.st_size) != st.st_size)
  {
    perror("Failed to read Plugin file");
    free(buf), buf = NULL;
    close(fd);
    return false;
  }
  close(fd);

  const CustomPluginHeader *header = (const CustomPluginHeader *)buf;

  char pbuf[256];
  snprintf(pbuf, sizeof(pbuf), "/system_tmp/%s.PID", header->titleID);

  if (strstr(filename, ".elf") != NULL)
  {
    // Handle ELF plugin loading
    if (!is_elf_file(buf, st.st_size))
    {
      free(buf), buf = NULL;
      return false;
    }

    pid_t pid = -1;
    int f = open(pbuf, O_RDONLY);
    if (f >= 0)
    {
      char t[32];
      int r = read(f, t, sizeof(t) - 1);
      close(f);
      if (r > 0)
      {
        t[r] = 0;
        pid = atoi(t);
      }
    }

    if (pid > 0)
    {
      char name[32];
      if (sceKernelGetProcessName(pid, name) < 0)
      {
        printf("Stale plugin PID file detected for %s, removing\n", header->titleID);
        unlink(pbuf);
        pid = -1;
      }
    }

    printf("seeing if elf is running\n");
    if (pid > 0)
    {
      printf("killing pid %d\n", pid);
      if (kill(pid, SIGKILL))
        perror("kill");
      unlink(pbuf);
    }

    printf("loading elf %s\n", filename);
    pid = elfldr_spawn("/", sock.fd, buf, header->titleID);
    if (pid >= 0)
      printf("  Launched!\n");
    else
      printf("  Already Running!\n");

    free(buf), buf = NULL;

    f = open(pbuf, O_WRONLY | O_CREAT | O_TRUNC, 0666);
    if (f >= 0)
    {
      if (pid >= 0)
      {
        char t[32];
        int l = snprintf(t, sizeof(t), "%d", pid);
        write(f, t, l);
      }
      else
      {
        unlink(pbuf);
      }
      close(f);
    }

    return true;
  }

  if (!is_valid_plugin(buf))
  {
    puts("Invalid plugin file.");
    free(buf), buf = NULL;
    return false;
  }

  puts("============== Plugin info ===============");
  printf("Plugin Prefix: %s\n", header->prefix);
  printf("Plugin TitleID: %s\n", header->titleID);
  printf("Plugin Version: %s\n", header->plugin_version);
  puts("=========================================");

  snprintf(pbuf, sizeof(pbuf), "/system_tmp/%s.PID", header->titleID);

  uint8_t *elf = get_elf_header_address(buf);

  pid_t pid = -1;
  int f = open(pbuf, O_RDONLY);
  if (f >= 0)
  {
    char t[32];
    int r = read(f, t, sizeof(t) - 1);
    close(f);
    if (r > 0)
    {
      t[r] = 0;
      pid = atoi(t);
    }
  }

  if (pid > 0)
  {
    char name[32];
    if (sceKernelGetProcessName(pid, name) < 0)
    {
      printf("Stale plugin PID file detected for %s, removing\n", header->titleID);
      unlink(pbuf);
      pid = -1;
    }
  }

  printf("seeing if plugin is running\n");
  if (pid > 0)
  {
    printf("killing pid %d\n", pid);
    if (kill(pid, SIGKILL))
      perror("kill");
    unlink(pbuf);
  }

  if (strcmp(header->titleID, "EORR37000") == 0)
  {
    notify("The Error disabler plugin is no longer required and has been auto deleted.");
    unlink(path);
    free(buf), buf = NULL;
    return true;
  }

  printf("loading plugin %s\n", path);
  pid = elfldr_spawn("/", sock.fd, elf, header->titleID);
  if (pid >= 0)
    printf("  Launched!\n");
  else
    printf("  Already Running!\n");

  f = open(pbuf, O_WRONLY | O_CREAT | O_TRUNC, 0666);
  if (f >= 0)
  {
    if (pid >= 0)
    {
      char t[32];
      int l = snprintf(t, sizeof(t), "%d", pid);
      write(f, t, l);
    }
    else
    {
      unlink(pbuf);
    }
    close(f);
  }

  free(buf), buf = NULL;

  return true;
}

/* R7.25.2.8: manual-only/retired payloads must never be boot-autostarted.
 * This is the same filename gate already proven in the earlier
 * DNS-DIRECT-PAYLOAD-PSPLAY-AUTOSTART-BLOCK checkpoint, now merged back
 * into the active Services branch. It blocks stale .auto_start markers from
 * PIZZA HEN, legacy etaHEN and USB roots without changing the payload ELF. */
static bool pizzahen_manual_only_payload_name(const char *name) {
  if (!name) return false;
  static const char *names[] = {
      "rp-get-pin.elf",
      "ps5-linux-loader.elf",
      "svtplay_v0.2.elf",
      "ProsperoPlayer_v1.0.elf",
      "PS-Play_v2.1.elf",
      "BFplayer-standalone_v0.1.0-alpha.44.elf",
      "Remote_Play.elf",
      "garlic-worker_v1.1.6.elf",
      nullptr};
  for (const char **it = names; *it; ++it)
    if (strcmp(name, *it) == 0) return true;
  return false;
}

/*=================== LOAD PLUGINS =========================*/
char **find_plugin_files() {
  const char *base_dirs[] = {
    // Plugin directories
    "/mnt/usb0/PIZZA_HEN/plugins", "/mnt/usb0/PIZZA_HEN/plugins",
    "/mnt/usb1/PIZZA_HEN/plugins", "/mnt/usb2/PIZZA_HEN/plugins",
    "/mnt/usb3/PIZZA_HEN/plugins", "/user/data/PIZZA_HEN/plugins",
    "/user/data/etahen/plugins",
    
    // Payload directories
    "/mnt/usb0/PIZZA_HEN/payloads", "/mnt/usb0/PIZZA_HEN/payloads",
    "/mnt/usb1/PIZZA_HEN/payloads", "/mnt/usb2/PIZZA_HEN/payloads",
    "/mnt/usb3/PIZZA_HEN/payloads", "/user/data/PIZZA_HEN/payloads",
    "/user/data/etahen/payloads"
};

  int base_dirs_count = sizeof(base_dirs) / sizeof(base_dirs[0]);

  char **plugin_paths = NULL;
  char full_path[255];
  char auto_start_path[255];
  plugin_count = 0;
  loaded_filenames = (char **)malloc(255 * sizeof(char *));

  for (int i = 0; i < base_dirs_count; i++) {
    DIR *dir = opendir(base_dirs[i]);
    if (dir) {
      struct dirent *entry;
      while ((entry = readdir(dir)) != NULL) {
        (void)memset(full_path, 0, sizeof(full_path));
        if (entry->d_type == DT_REG) { // Regular file
          const char *ext = strrchr(entry->d_name, '.');
          if (ext && (strcmp(ext, ".plugin") == 0 || strcmp(ext, ".elf") == 0)) {
            bool skip = false;
            if (pizzahen_manual_only_payload_name(entry->d_name)) {
              printf("manual-only payload: ignoring stale autostart marker for %s/%s\n",
                     base_dirs[i], entry->d_name);
              continue;
            }
            // Construct full path
            snprintf(full_path, sizeof(full_path), "%s/%s", base_dirs[i],
                     entry->d_name);
            snprintf(auto_start_path, sizeof(auto_start_path),
                     "%s/%s.auto_start", base_dirs[i], entry->d_name);

            if (!if_exists(auto_start_path)) {
              printf("skipping auto start for plugin: %s\n", full_path);
              continue;
            }

            for (int j = 0; j < plugin_count; j++) {
              if (strcmp(loaded_filenames[j], entry->d_name) == 0) {
                skip = true;
                // Only print the message for /data/PIZZA_HEN/plugins/elfldr.plugin
                // as per specific requirement
                if ((strcmp(base_dirs[i], "/data/PIZZA_HEN/plugins") == 0) || (strcmp(entry->d_name, "/data/PIZZA_HEN/payloads") == 0)) {
                  printf("skipping duplicate plugin: %s | already loaded: %s\n",
                         full_path, loaded_filenames[j]);
                }
                break;
              }
            }
            if (skip)
              continue;

            // Add to array
            plugin_paths = (char **)realloc(plugin_paths, (plugin_count + 1) *
                                                              sizeof(char *));
            plugin_paths[plugin_count] = strdup(full_path);

            // Copy filename to loaded_filenames
            loaded_filenames[plugin_count] =
                strdup(entry->d_name); // Use strdup for simplicity
            plugin_count++;
          }
        }
      }
      closedir(dir);
    }
  }

  return plugin_paths;
}
void free_plugin_files(char **plugin_files) {
  // Free memory for loaded_filenames
  for (int i = 0; i < plugin_count; i++) {
    free(loaded_filenames[i]);
  }
  free(loaded_filenames);

  for (int i = 0; i < plugin_count; i++) {
    free((void *)plugin_files[i]);
  }
  free((void *)plugin_files);
}

bool Byepervisor();
bool sceKernelIsTestKit() {
  uint8_t s_PsId[16] = {0};

  size_t v2 = 16;
  if (sysctlbyname("machdep.openpsid_for_sys", &s_PsId, &v2, 0, 0) < 0) {
    printf("sceKernelGetOpenPsIdForSystem failed\n");
    return true;
  }

  char psid_buf[255] = {0};

  for (int i = 0; i < 16; i++) {
    snprintf(psid_buf + strlen(psid_buf), 255 - strlen(psid_buf), "%02x",
             s_PsId[i]);
  }

  const char *whitelisted_psids[] = {
      "b345df7d4c77618d40f19a90e438ad87",
      "ab535275b7196e7e7d43f4f9e7806724",
      "d376c7780b960e5182d326ba3aa2d7a3",
      "a8d89ad976b5cb912837ad29b0cc4610",
      "177e09480b40816a1caca5151565daa5",
           

  };

#if 0
  printf("PSID: %s\n", psid_buf);
  char buff[300];
  snprintf(buff, sizeof buff, "PSID: %s", psid_buf);
  notify(buff);
#endif

  for (int i = 0; i < sizeof(whitelisted_psids) / sizeof(whitelisted_psids[0]);
       i++) {
    if (strcmp(psid_buf, whitelisted_psids[i]) == 0) {
      // printf("PSID (%s) whitelisted\n", psid_buf);
      return false; // report not testkit if is whitelisted
    }
  }

  // printf("PSID (%s) Not whitelisted\n", psid_buf);
  return if_exists("/system/priv/lib/libSceDeci5Ttyp.sprx");
}
#define PUBLIC_TEST 0
#define PIZZA_HEN_DIAG_PREKSTUFF 0
#define PIZZA_HEN_DIAG_POSTB6 0
#define PIZZA_HEN_DIAG_KSTUFF_ISOLATED 0
#define PIZZA_HEN_DIAG_SHADOWMOUNT_ISOLATED 1
#define EXPIRE_YEAR 2026
#define EXPIRE_MONTH 1
#define EXPIRE_DAY 1


bool isPastBetaDate(int year, int month, int day);

int main(void) {
  ui_trace("PIZZA HEN DIAG B1: bootstrapper entered");
  // ptrace(PT_ATTACH, pid, 0, 0);
  /// clearFramePointer();
  int pid = -1;

#if BETA == 1
  char out[1024];
#endif

  signal(SIGCHLD, SIG_IGN);

  klog_puts("Jailbreaking the boostrapper ...");
  // launch socksrv.elf in a new processes
  if (elfldr_raise_privileges(getpid())) {
    notify("PIZZA HEN DIAG B1-FAIL: unable to raise privileges");
    return -1;
  }
  ui_trace("PIZZA HEN DIAG B2: privileges acquired");

#if BETA == 1
  printf("Get_code %d", GetDecryptedConsoleCode(
                            &out[0])); // ignore return value because we need to
                                       // call is_console_whitelisted anyway
  bool is_whitelisted = is_console_whitelisted(
      &buffer[0], &out[0]); // gets PSID if its not whitelisted too
#endif

#if BETA == 1 || PUBLIC_TEST == 1
  if (isPastBetaDate(EXPIRE_YEAR, EXPIRE_MONTH, EXPIRE_DAY)) {
    notify("This PIZZA HEN Beta version expired on %d-%d-%d", EXPIRE_YEAR,
           EXPIRE_MONTH, EXPIRE_DAY);
    return -1;
    raise(SIGSEGV);
  }
#endif

#if 0
  if (sceKernelIsTestKit()) {
    notify("support dropped for testkits if you donated to my ko-fi and are NOT andrew send me a message");
    return 0;
  }
#endif


  klog_printf("   Success!\n");
  if(if_exists("/data/I_want_logging_for_etahen")){
      klog_printf("Redirecting stdout and stderr to logger ...");
     if(initStdout() >= 0)
         klog_puts("   Success!");
     else
         klog_puts("   Failed!");
      
  }


  
  #if BETA == 1 
  if (!is_whitelisted) {
    notify("This console is NOT approved to use this PIZZA HEN beta version\n\nIf "
           "you are not yet approved send LM the pending_approval.bin file "
           "from your USB for the PIZZA_HEN_approval.bin");
    int fd = open("/mnt/usb0/pending_approval.bin", O_CREAT | O_TRUNC | O_RDWR,
                  0777);
    if (fd < 0) {
      fd = open("/mnt/usb1/pending_approval.bin", O_CREAT | O_TRUNC | O_RDWR,
                0777);
      if (fd < 0) {
        fd = open("/mnt/usb2/pending_approval.bin", O_CREAT | O_TRUNC | O_RDWR,
                  0777);
      }

    if (fd >= 0) {
      write(fd, buffer, strlen(buffer));
      close(fd);
    } else {
      notify("No USB Found to save pending_approval.bin\n\nInsert a EXFAT USB "
             "then re-run this payload");
    }

    return -1;
    raise(SIGSEGV);
  }
  #endif


  OrbisKernelSwVersion sys_ver;
  sceKernelGetProsperoSystemSwVersion(&sys_ver);

  if (sys_ver.version < 0x3000000 && !sceKernelIsGenuineDevKit()) {
    klog_printf("FW %s version has Byepervisor available, sstarting....\n", sys_ver.version_str);
    if (!Byepervisor()) {
      printf("Byepervisor failed or is resume_nedded");
      return 0;
    }
  }

  ui_trace("PIZZA HEN DIAG B3: firmware check passed");
  klog_puts("============== Spawner (Bootstrapper) Started =================");

  mkdir("/data/PIZZA_HEN", 0777);
  mkdir("/data/PIZZA_HEN/plugins", 0777);
  mkdir("/data/PIZZA_HEN/payloads", 0777);
  mkdir("/data/PIZZA_HEN/daemons", 0777);
  mkdir("/data/PIZZA_HEN/assets", 0777);
  mkdir("/data/PIZZA_HEN/games", 0777);
  mkdir("/data/PIZZA_HEN/logs", 0777);
  mkdir("/data/PIZZA_HEN/crash", 0777);

  klog_printf("Registering signal handler ...");
  fault_handler_init(cleanup);
  klog_printf("   Success!\n");

  ui_trace("PIZZA HEN DIAG B4: starting remount");
  klog_printf("Remounting system partitions ...");
  if (!remount("/dev/ssd0.system_ex", "/system_ex")) {
    perror("failed to mount /system_ex\nif you see this reboot");
    notify("failed to mount /system_ex\nif you see this reboot");
    return -1;
  }
  if (!remount("/dev/ssd0.system", "/system")) {
    perror("failed to mount /system_\nif you see this reboot");
    notify("failed to mount /system\nif you see this reboot");
    return -1;
  }
  klog_printf("   Success!\n");
  ui_trace("PIZZA HEN DIAG B5: remount complete");

  klog_printf("Writing embedded assets ...");
  write_embedded_assets();
  klog_printf("   Written!\n");
  ui_trace("PIZZA HEN DIAG B6: assets written");
#if PIZZA_HEN_DIAG_PREKSTUFF
  ui_trace("PIZZA HEN DIAG STOP: before post-B6 path");
  return 0;
#endif

  ui_trace("PIZZA HEN DIAG B7: before welcome notification");
	sceNotificationSend(0xFE, true, &json_payload[0]);
  ui_trace("PIZZA HEN DIAG B8: welcome notification returned");

  // R3: Media tiles are deliberately installed only after the KStuff selector
  // has completed and the chosen engine is confirmed ready.

  ui_trace("PIZZA HEN DIAG B9: starting update protection");
  klog_printf("Unmounting /update forcefully ...");
  // block updates
  unlink("/update/PS5UPDATE.PUP");
  unlink("/update/PS5UPDATE.PUP.net.temp");
  ui_trace("PIZZA HEN DIAG B10: update files handled");
  // unlink("/update/PS4UPDATE.PUP.md5");
  ui_trace("PIZZA HEN DIAG B11: before /update unmount");
  if ((int)unmount("/update", 0x80000LL) < 0) {
    unmount("/update", 0);
  }

  klog_puts("   Success!");
  ui_trace("PIZZA HEN DIAG B12: post-B6 path complete; STOP before kstuff");
#if PIZZA_HEN_DIAG_POSTB6
  return 0;
#endif

#if PIZZA_HEN_DIAG_SHADOWMOUNT_ISOLATED
  // FIX25 gate: browser selector follows the same proven pattern as PS5 Payload Manager.
  // websrv serves the UI locally, the PS5 system browser displays it, and this
  // bootstrapper remains the single owner of engine launch.
  ui_trace("PIZZA HEN W0: KStuff selector stage");
  if (sys_ver.version < 0x3000000) {
      ui_trace("PIZZA HEN W0-SKIP: firmware path does not use KStuff");
      return 0;
  }

  if (kstuff_probe_ready()) {
      ui_trace("PIZZA HEN W0-SAFE: KStuff already active; refusing second engine");
  } else {
      char choice[16] = {0};
      ui_trace("PIZZA HEN W1: starting local browser KStuff selector");
      int selector_rc = start_browser_kstuff_selector();
      if (selector_rc < 0) {
          notify("PIZZA HEN W2-FAIL: browser selector rc=0x%X", selector_rc);
          return 0;
      }

      ui_trace("PIZZA HEN W2: browser selector visible - choose Lite 1.10, DR 1.2, or Base 1.6.7");
      if (!wait_for_web_kstuff_request(choice, sizeof(choice))) {
          notify("PIZZA HEN W3-TIMEOUT: no KStuff selected");
          return 0;
      }

      unlink("/data/PIZZA_HEN/runtime/kstuff_request.txt");
      unlink("/data/PIZZA_HEN/runtime/kstuff_request.tmp");

      uint8_t *chosen = nullptr;
      unsigned int chosen_size = 0;
      const char *chosen_name = nullptr;
      if (!strcmp(choice, "dr")) {
          chosen = kstuff_dr_start;
          chosen_size = kstuff_dr_size;
          chosen_name = "kstuff-dr-1.2";
      } else if (!strcmp(choice, "base")) {
          chosen = kstuff_base_start;
          chosen_size = kstuff_base_size;
          chosen_name = "kstuff-base-1.6.7";
      } else {
          chosen = kstuff_start;
          chosen_size = kstuff_size;
          chosen_name = "kstuff-lite-1.10";
      }

      if (chosen_size < 4 || chosen[0] != 0x7f || chosen[1] != 'E' ||
          chosen[2] != 'L' || chosen[3] != 'F') {
          notify("PIZZA HEN W4-FAIL: selected KStuff ELF invalid");
          return -1;
      }
      ui_trace("PIZZA HEN W4: selected %s", chosen_name);
      int kstuff_spawn_rc = elfldr_spawn("/", STDOUT_FILENO, chosen, chosen_name);
      if (kstuff_spawn_rc < 0) {
          notify("PIZZA HEN W4-FAIL: selected KStuff spawn failed");
          return 0;
      }

      int ready_wait = 0;
      while (!kstuff_probe_ready()) {
          if (ready_wait++ >= 15) {
              notify("PIZZA HEN W5-FAIL: selected KStuff did not become ready");
              return 0;
          }
          sleep(1);
      }
      write_blob_file("/data/PIZZA_HEN/runtime/kstuff_active.txt",
                      choice, strlen(choice), 0666);
      ui_trace("PIZZA HEN W5: %s ready", chosen_name);
  }

  cleanup_shadowmount_psplay_generated_source();

  // R7.14: second explicit selector gate. KStuff is ready; now the user
  // chooses exactly one ShadowMount engine before any post-ShadowMount service
  // (FTP, Debug, etc.) is allowed to start.
  uint8_t *selected_shadow = shadowmount_start;
  unsigned int selected_shadow_size = shadowmount_size;
  const char *selected_shadow_name = "ShadowMountPlus-1.6beta16-STABLE";
  const char *selected_shadow_choice = "stable";
  {
      char shadow_choice[24] = {0};
      ui_trace("PIZZA HEN V0: ShadowMount selector stage");
      int shadow_selector_rc = start_browser_shadowmount_selector();
      if (shadow_selector_rc != 0) {
          notify("PIZZA HEN V1-FAIL: ShadowMount selector rc=0x%X", shadow_selector_rc);
          return 0;
      }
      ui_trace("PIZZA HEN V1: choose Stable 1.6beta16, Experimental 1.7alpha8, or skip ShadowMountPlus for dump_installer");
      if (!wait_for_web_shadowmount_request(shadow_choice, sizeof(shadow_choice))) {
          notify("PIZZA HEN V2-TIMEOUT: no ShadowMount selected");
          return 0;
      }
      unlink("/data/PIZZA_HEN/runtime/shadowmount_request.txt");
      unlink("/data/PIZZA_HEN/runtime/shadowmount_request.tmp");
      if (!strcmp(shadow_choice, "experimental")) {
          selected_shadow = shadowmount_experimental_start;
          selected_shadow_size = shadowmount_experimental_size;
          selected_shadow_name = "ShadowMountPlus-1.7alpha8-EXPERIMENTAL";
          selected_shadow_choice = "experimental";
      } else if (!strcmp(shadow_choice, "skip")) {
          selected_shadow = nullptr;
          selected_shadow_size = 0;
          selected_shadow_name = "ShadowMountPlus-SKIPPED-DUMP-INSTALLER";
          selected_shadow_choice = "skip";
      }
      ui_trace("PIZZA HEN V2: selected %s", selected_shadow_name);
  }

  // R3: user-selected KStuff is ready. Register both independent Media entries now.
  // PZHN00001 = latest PIZZA HEN Toolbox.
  // PZHN00002 = Debug Services using the original v0.1 launcher/helper pipeline.
  int toolbox_tile_rc = install_pizzahen_toolbox_shortcut();
  if (toolbox_tile_rc != 0) {
      usleep(250000);
      toolbox_tile_rc = install_pizzahen_toolbox_shortcut();
  }
  if (toolbox_tile_rc != 0)
      notify("PIZZA HEN Toolbox icon install failed (0x%X)\nStatus: /data/PIZZA_HEN/runtime/media_tile_status.txt",
             toolbox_tile_rc);

  int debug_services_tile_rc = install_pizzahen_debug_services_shortcut();
  if (debug_services_tile_rc != 0) {
      usleep(250000);
      debug_services_tile_rc = install_pizzahen_debug_services_shortcut();
  }
  if (debug_services_tile_rc != 0)
      notify("Debug Services icon install failed (0x%X)\nStatus: /data/PIZZA_HEN/runtime/debug_services_tile_status.txt",
             debug_services_tile_rc);

  ui_trace("PIZZA HEN TDUAL: Media tiles ready: PZHN00001 Toolbox + PZHN00002 Debug Services");

  if (!strcmp(selected_shadow_choice, "skip")) {
      ui_trace("PIZZA HEN S0-SKIP: ShadowMountPlus intentionally not launched (EchoStretch dump_installer path)");
      write_blob_file("/data/PIZZA_HEN/runtime/shadowmount_active.txt",
                      selected_shadow_choice, strlen(selected_shadow_choice), 0666);
      ui_trace("PIZZA HEN S6: selected KStuff + ShadowMount skip gate PASS; continuing to FTP/Debug");
  } else {
      ui_trace("PIZZA HEN S0: starting selected %s", selected_shadow_name);
      if (selected_shadow_size < 4 || selected_shadow[0] != 0x7f ||
          selected_shadow[1] != 'E' || selected_shadow[2] != 'L' ||
          selected_shadow[3] != 'F') {
          notify("PIZZA HEN S1-FAIL: selected ShadowMount ELF invalid");
          return -1;
      }
      signal(SIGCHLD, SIG_DFL);
      int shadow_spawn_rc = elfldr_spawn("/", STDOUT_FILENO, selected_shadow,
                                         selected_shadow_name);
      if (shadow_spawn_rc < 0) {
          notify("PIZZA HEN S3-FAIL: selected ShadowMount spawn failed");
          return 0;
      }
      write_blob_file("/data/PIZZA_HEN/runtime/shadowmount_active.txt",
                      selected_shadow_choice, strlen(selected_shadow_choice), 0666);
      sleep(3);
      ui_trace("PIZZA HEN S6: selected KStuff + selected ShadowMount start gate PASS");
  }

  // FIX26: Payload #1 after ShadowMount = upstream ftpsrv v0.21.
  // Keep the upstream ELF pristine and let the bootstrapper only own ordering.
  ui_trace("PIZZA HEN F0: starting ftpsrv v0.21 on port 2121");
  if (ftpsrv_size < 4 || ftpsrv_start[0] != 0x7f ||
      ftpsrv_start[1] != 'E' || ftpsrv_start[2] != 'L' ||
      ftpsrv_start[3] != 'F') {
      notify("PIZZA HEN F1-FAIL: ftpsrv ELF invalid");
      return -1;
  }

  // If TCP/2121 is already active, do not stack a second FTP service.
  if (wait_for_local_ftpsrv(200)) {
      ui_trace("PIZZA HEN F2-SAFE: FTP port 2121 already active; skipping duplicate");
  } else {
      signal(SIGCHLD, SIG_DFL);
      int ftp_spawn_rc = elfldr_spawn("/", STDOUT_FILENO, ftpsrv_start, "ftpsrv.elf");
      if (ftp_spawn_rc < 0) {
          notify("PIZZA HEN F2-FAIL: ftpsrv spawn failed");
          return 0;
      }
      if (!wait_for_local_ftpsrv(12000)) {
          notify("PIZZA HEN F3-FAIL: ftpsrv did not become ready on 2121");
          return 0;
      }
      ui_trace("PIZZA HEN F3: ftpsrv v0.21 ready on port 2121");
  }

  ui_trace("PIZZA HEN F6: KStuff + ShadowMount + FTP PASS");

  // FIX27: Payload #2 (final automatic post-ShadowMount payload) =
  // upstream ps5debug-NG v1.3.0. No menu and no additional confirmation.
  // It starts only after the FTP readiness gate above has passed.
  ui_trace("PIZZA HEN D0: starting ps5debug-NG v1.3.0 automatically");
  if (ps5debug_ng_size < 4 || ps5debug_ng_start[0] != 0x7f ||
      ps5debug_ng_start[1] != 'E' || ps5debug_ng_start[2] != 'L' ||
      ps5debug_ng_start[3] != 'F') {
      notify("PIZZA HEN D1-FAIL: ps5debug-NG ELF invalid");
      return -1;
  }

  // Do not stack a second debugger service if TCP/744 is already active.
  if (wait_for_local_ps5debug_ng(250)) {
      ui_trace("PIZZA HEN D2-SAFE: ps5debug-NG port 744 already active; skipping duplicate");
  } else {
      signal(SIGCHLD, SIG_DFL);
      int debug_spawn_rc = elfldr_spawn("/", STDOUT_FILENO, ps5debug_ng_start,
                                        "ps5debug-NG_v1.3.0.elf");
      if (debug_spawn_rc < 0) {
          notify("PIZZA HEN D2-FAIL: ps5debug-NG spawn failed");
          return 0;
      }
      if (!wait_for_local_ps5debug_ng(20000)) {
          notify("PIZZA HEN D3-FAIL: ps5debug-NG did not become ready on 744");
          return 0;
      }
      ui_trace("PIZZA HEN D3: ps5debug-NG v1.3.0 ready on port 744");
  }

  ui_trace("PIZZA HEN D6: full automatic post-ShadowMount payload chain PASS");
  ui_trace("PIZZA HEN E0: continuing into complete etaHEN-derived Toolbox runtime");
  // FIX30: no early return here. Utility daemon, main daemon, ShellUI Toolbox
  // injection, plugins/payload ELF autostart and the inherited etaHEN feature
  // set below are now reachable again after the known-good PIZZA HEN chain.
#else
#if 1
  char buz[100] = { 0 };
  // Load kstuff if needed
  bool dont_load_kstuff = (if_exists("/mnt/usb0/no_kstuff") || if_exists("/data/PIZZA_HEN/no_kstuff"));
  if (dont_load_kstuff) {
      notify("kstuff loading disabled via file, non-payload homebrew and PS4 FPKGs will be disabled");
      klog_puts("kstuff loading disabled in config.ini or no_kstuff file found");
  }
  if (!dont_load_kstuff && sys_ver.version >= 0x3000000) {
      bool cleanup_kstuff = false;
      uint8_t* kstuff_address = get_kstuff_address(cleanup_kstuff);
      if (elfldr_spawn("/", STDOUT_FILENO, kstuff_address, "kstuff")) {
          int wait = 0;
          bool kstuff_not_loaded = false;
          sleep(1);
          while ((kstuff_not_loaded = sceKernelMprotect(&buz[0], 100, 0x7) < 0)) {
              if (wait++ > 10) {
                  notify("Failed to load kstuff, kstuff will be unavailable");
                  break;
              }
              sleep(1);
          }
          if (!kstuff_not_loaded) klog_puts("kstuff loaded");
          if (cleanup_kstuff) free(kstuff_address);
      } else {
          notify("Failed to load kstuff, kstuff will be unavailable");
      }
  }
  sleep(1);
#endif
#endif

  // FIX32: the permanent Media tile is the primary Toolbox entry point.
  // Prevent automatic ShellUI injection during boot; the tile requests it on demand.
  mkdir("/data/PIZZA_HEN/runtime", 0777);
  static const char browser_mode[] = "1\n";
  write_blob_file("/data/PIZZA_HEN/runtime/browser_toolbox_mode", browser_mode,
                  sizeof(browser_mode) - 1, 0666);

  // FIX34: Media tile registration was already handled at ELF startup,
  // before the KStuff selector and all post-selector readiness gates.
  klog_printf("Starting Utility etaHEN services ...");

  while ((pid = find_pid("etaHEN")) > 0) {
   // printf("killing pid %d\n", pid);
    if (kill(pid, SIGKILL)) {
      perror("kill");
    }
  }

  if (elfldr_spawn("/", sock.fd, util_start, "etaHEN Utility Daemon") >= 0) {
      klog_printf("  Launched!\n");
    // Open the file with write permission, create if not exist, truncate to zero if exists
    int fd = open("/data/PIZZA_HEN/daemons/util.elf", O_WRONLY | O_CREAT | O_TRUNC, 0777);
    if (fd == -1) {
      perror("open failed");
      return -1337;
    }
    // Write the buffer to the file
    if (write(fd, util_start, util_size) == -1) {
       perror("write failed");
    }

    // Close the file descriptor
    close(fd);
  } else {
    klog_printf("failed to launch utility daemon\n");
    notify("failed to launch the PIZZA HEN utility daemon");
    return -2;
  }

  klog_printf("Starting the main etaHEN daemon ...");

  if (elfldr_spawn("/", sock.fd, daemon_start, "etaHEN Critical services") >= 0) {
      klog_printf("  Launched!\n");
  } else {
      klog_printf("failed to launch main daemon\n");
      notify("failed to launch the main PIZZA HEN daemon");
      return -2;
  }

  // return 0;

  char **plugin_paths = find_plugin_files();
  if (plugin_paths && plugin_count > 0) {
    int loaded_plugins = 0;
    // First, load all plugins except elfldr.plugin
    for (int i = 0; i < plugin_count; i++) {
      // Skip loading elfldr.plugin in this loop
      if (strstr(plugin_paths[i], "elfldr") == 0) {
          klog_printf("Loading plugin: %s\n", plugin_paths[i]);
        if (!load_plugin(plugin_paths[i], loaded_filenames[i])) {
          snprintf(buff, sizeof(buff),
                   "[PIZZA HEN] Failed to load plugin!\nPath: %s",
                   plugin_paths[i]);
          notify(buff);
          klog_puts("FAILED!");
          continue;
        }

        klog_puts("Loaded!");
        loaded_plugins++;
      }
    }
    //(void)memset(buff, 0, sizeof(buff));
    // snprintf(buff, sizeof(buff), "Successfully loaded %d plugins",
    // loaded_plugins); notify(buff);
    klog_printf("Successfully loaded %d plugins\n", loaded_plugins);
    free_plugin_files(plugin_paths);
  }
  // raise(SIGKILL, getpid());
  // sceSystemServiceLoadExec("exit", NULL);
  ui_trace("PIZZA HEN E6: complete Toolbox runtime and plugin stage initialized");
  klog_puts("============== Spawner (Bootstrapper) Finished =================");

  return 0;
}
