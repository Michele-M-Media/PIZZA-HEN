#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/un.h>
#include <unistd.h>

/*
 * PIZZA HEN FIX70.33 -- source-grounded websrv -> etaHEN service bridge.
 *
 * Authority for service semantics is the supplied etaHEN source. websrv 0.34
 * is transport only. Service state is not reimplemented here. A toggle
 * succeeds only when the same etaHEN daemon IPC command reports
 * success; on failure PIZZA rolls the persisted value back.
 *
 * Package Installer and cheat download/reload backends are intentionally not
 * reimplemented here. Their already-frozen commands/routes are only invoked.
 */
#define CRIT_IPC_SOC "/system_tmp/etaHEN_crit_service"
#define UTIL_IPC_SOC "/system_tmp/etaHEN_util_service"
#define STATUS_FILE "/data/PIZZA_HEN/runtime/toolbox_action_status.txt"
#define CHEAT_SESSION_FILE "/data/PIZZA_HEN/runtime/cheat_session.json"
#define CONFIG_FILE "/data/PIZZA_HEN/config.ini"
#define CONFIG_TMP_FILE "/data/PIZZA_HEN/config.ini.fix7033.tmp"
#define SHELL_CONFIG_FILE "/user/data/PIZZA_HEN/config.ini"
#define SHELL_CONFIG_TMP_FILE "/user/data/PIZZA_HEN/config.ini.fix7033.tmp"
#define SHELL_CONTROL_REQUEST "/system_tmp/pizzahen_web_control.request"
#define SHELL_CONTROL_REQUEST_TMP "/system_tmp/pizzahen_web_control.request.tmp"
#define SHELL_CONTROL_ACK "/system_tmp/pizzahen_web_control.ack"
#define DAEMON_BUFF_MAX 0x1000

#define BREW_RELOAD_SETTINGS      0x00C0FFEE
#define BREW_TOGGLE_PS5DEBUG      0x000DE8E6
#define BREW_UTIL_TOGGLE_FTP      0x08000004
#define BREW_UTIL_TOGGLE_KLOG     0x08000005
#define BREW_UTIL_TOGGLE_DPI      0x08000006
#define BREW_UTIL_LAUNCH_PLUGIN   0x08000007
#define BREW_UTIL_GET_GAME_VER    0x08000009
#define BREW_UTIL_GET_GAME_CHEAT  0x0800000A
#define BREW_UTIL_TOGGLE_CHEAT    0x0800000B
#define BREW_UTIL_DOWNLOAD_CHEATS 0x0800000C
#define BREW_UTIL_RELOAD_CHEATS   0x0800000D
#define BREW_UTIL_DOWNLOAD_KSTUFF 0x0800000E
#define BREW_UTIL_TOGGLE_LEGACY_CMD_SERVER 0x0800000F
#define BREW_UTIL_GET_GAMES_LIST  0x08000010
#define BREW_UTIL_LAUNCH_GAME_BY_BUTTON_ID 0x08000011
#define BREW_UTIL_SCAN_USB_PKGS   0x08000012
#define BREW_UTIL_DOWNLOAD_STORE  0x08000013
#define BREW_UTIL_SCAN_PLUGINS    0x08000014
#define BREW_UTIL_STOP_PLUGIN     0x08000015
#define BREW_UTIL_SET_PLUGIN_AUTOSTART 0x08000016
#define BREW_UTIL_REFRESH_PAYLOAD_REPO 0x08000017
#define BREW_UTIL_INSTALL_PAYLOAD_REPO 0x08000018
#define BREW_UTIL_LAUNCH_ELFLDR   0x00E1F1D8
#define BREW_INSTALL_THE_STORE    0x0900000D
#define BREW_TESTKIT_CHECK        0x09000010
#define BREW_LAUNCH_DUMPER        0x09000013
#define BREW_ENABLE_TOOLBOX          0x09000011
#define BREW_PIZZAHEN_SHELL_SERVICE 0x09000016

struct IPCMessage { int magic; int cmd; int error; char msg[DAEMON_BUFF_MAX]; };
static char g_status_token[48];

static const char *g_numeric_config_keys[] = {
  "FTP","Klog","DPI","Allow_data_in_sandbox",
  "ALLOW_FTP_DEV_ACCESS","StartOption","Rest_Mode_Delay_Seconds","Util_rest_kill",
  "Game_rest_kill","toolbox_auto_start","disable_toolbox_auto_start_for_rest_mode",
  "Display_tids","APP_JB_Debug_Msg","etaHEN_Game_Options","auto_eject_disc",
  "enable_kstuff_on_close","pause_kstuff_on_open","pause_kstuff_on_open_secs",
  "Cheats_shortcut_opt","Toolbox_shortcut_opt",
  "Games_shortcut_opt","Kstuff_shortcut_opt","legacy_cmd_server",
  "libhijacker_cheats","testkit","LiteMode","PS5Debug",
  "overlay_gpu","overlay_cpu","overlay_ram","overlay_fps","overlay_ip","overlay_kstuff","all_cpu_usage","Overlay_pos"
};

static void ensure_dirs(void){ mkdir("/data/PIZZA_HEN",0777); mkdir("/data/PIZZA_HEN/runtime",0777); }
static void write_status(const char *s){ ensure_dirs(); int fd=open(STATUS_FILE,O_WRONLY|O_CREAT|O_TRUNC,0666); if(fd<0)return; write(fd,s,strlen(s)); if(g_status_token[0]){write(fd,"|tx=",4);write(fd,g_status_token,strlen(g_status_token));} write(fd,"\n",1); fsync(fd); close(fd); }
static int finish(const char *ok,const char *fail,int rc){write_status(rc==0?ok:fail);return rc;}
static void capture_status_token(int argc, char **argv) {
  g_status_token[0] = 0;
  for (int i = 0; i < argc; ++i) {
    const char *a = argv[i];
    if (!a || strncmp(a, "tx=", 3)) continue;
    size_t j = 0;
    for (const char *q = a + 3; *q && j + 1 < sizeof(g_status_token); ++q) {
      const char c = *q;
      const int safe = (c >= '0' && c <= '9') || (c >= 'a' && c <= 'z') ||
                       (c >= 'A' && c <= 'Z') || c == '-' || c == '_';
      if (!safe) break;
      g_status_token[j++] = c;
    }
    g_status_token[j] = 0;
    break;
  }
}

static int send_ipc(const char *sock,int cmd,const char *json){int fd=socket(AF_UNIX,SOCK_STREAM,0);if(fd<0)return 2;struct sockaddr_un a;memset(&a,0,sizeof(a));a.sun_family=AF_UNIX;strncpy(a.sun_path,sock,sizeof(a.sun_path)-1);if(connect(fd,(struct sockaddr*)&a,SUN_LEN(&a))!=0){close(fd);return 3;}struct IPCMessage m;memset(&m,0,sizeof(m));m.magic=(int)0xDEADBABE;m.cmd=cmd;snprintf(m.msg,sizeof(m.msg),"%s",json?json:"{}");if(send(fd,&m,sizeof(m),MSG_NOSIGNAL)<0){close(fd);return 4;}if(recv(fd,&m,sizeof(m),MSG_NOSIGNAL)<=0){close(fd);return 5;}close(fd);return m.error==0?0:6;}

/* R7.5: same etaHEN IPC wire format as send_ipc(), but preserve the daemon's
   existing {"var":"..."} return object for the owned web Cheats surface. */
static void reload_daemons(void){(void)send_ipc(CRIT_IPC_SOC,BREW_RELOAD_SETTINGS,"{}");(void)send_ipc(UTIL_IPC_SOC,BREW_RELOAD_SETTINGS,"{}");}

static int key_allowed(const char *key){if(!key||!*key)return 0;for(size_t i=0;i<sizeof(g_numeric_config_keys)/sizeof(g_numeric_config_keys[0]);i++)if(!strcmp(key,g_numeric_config_keys[i]))return 1;return 0;}
static int numeric_allowed(const char *v){if(!v||!*v||strlen(v)>10)return 0;for(const char*p=v;*p;p++)if(*p<'0'||*p>'9')return 0;return 1;}
static int config_get_int(const char *key,int fallback){FILE*f=fopen(CONFIG_FILE,"r");if(!f)return fallback;char line[1024];int in=0,val=fallback;size_t n=strlen(key);while(fgets(line,sizeof(line),f)){if(line[0]=='[')in=!strncmp(line,"[Settings]",10);if(in&&!strncmp(line,key,n)&&line[n]=='='){val=atoi(line+n+1);break;}}fclose(f);return val;}
static int config_set_numeric(const char *key,const char *value){if(!key_allowed(key)||!numeric_allowed(value))return 9;ensure_dirs();FILE*in=fopen(CONFIG_FILE,"r"),*out=fopen(CONFIG_TMP_FILE,"w");if(!out){if(in)fclose(in);return 10;}int inset=0,have=0,repl=0;char line[1024];while(in&&fgets(line,sizeof(line),in)){if(line[0]=='['){inset=!strncmp(line,"[Settings]",10);if(inset)have=1;}if(inset){size_t n=strlen(key);if(!strncmp(line,key,n)&&line[n]=='='){fprintf(out,"%s=%s\n",key,value);repl=1;continue;}}fputs(line,out);}if(in)fclose(in);if(!have)fprintf(out,"\n[Settings]\n");if(!repl)fprintf(out,"%s=%s\n",key,value);fflush(out);fsync(fileno(out));fclose(out);if(rename(CONFIG_TMP_FILE,CONFIG_FILE)!=0){unlink(CONFIG_TMP_FILE);return 11;}chmod(CONFIG_FILE,0777);return 0;}
static int copy_file_atomic(const char*src,const char*tmp,const char*dst){int in=open(src,O_RDONLY);if(in<0)return 20;int out=open(tmp,O_WRONLY|O_CREAT|O_TRUNC,0777);if(out<0){close(in);return 21;}char b[4096];ssize_t n;int rc=0;while((n=read(in,b,sizeof(b)))>0){ssize_t o=0;while(o<n){ssize_t w=write(out,b+o,(size_t)(n-o));if(w<=0){rc=22;break;}o+=w;}if(rc)break;}if(n<0)rc=23;fsync(out);close(out);close(in);if(rc){unlink(tmp);return rc;}if(rename(tmp,dst)!=0){unlink(tmp);return 24;}chmod(dst,0777);return 0;}
static int mirror_shell_config(void){mkdir("/user/data/PIZZA_HEN",0777);return copy_file_atomic(CONFIG_FILE,SHELL_CONFIG_TMP_FILE,SHELL_CONFIG_FILE);}
static int locale_safe(const char *s){if(!s||!*s||strlen(s)>15)return 0;for(const char*p=s;*p;++p){char c=*p;if(!((c>='a'&&c<='z')||(c>='A'&&c<='Z')||(c>='0'&&c<='9')||c=='-'))return 0;}return 1;}
static int write_locale_file(const char *path,const char *locale){int fd=open(path,O_WRONLY|O_CREAT|O_TRUNC,0666);if(fd<0)return 41;size_t n=strlen(locale);if(write(fd,locale,n)!=(ssize_t)n){close(fd);return 42;}write(fd,"\n",1);fsync(fd);close(fd);chmod(path,0666);return 0;}
static int persist_ui_locale(const char *locale){if(!locale_safe(locale))return 40;ensure_dirs();mkdir("/user/data/PIZZA_HEN",0777);mkdir("/user/data/PIZZA_HEN/runtime",0777);int rc=write_locale_file("/data/PIZZA_HEN/runtime/ui_locale.txt",locale);if(rc)return rc;return write_locale_file("/user/data/PIZZA_HEN/runtime/ui_locale.txt",locale);}

static int safe_field(const char*s){if(!s||!*s||strlen(s)>80)return 0;for(const char*p=s;*p;p++){char c=*p;if(!((c>='a'&&c<='z')||(c>='A'&&c<='Z')||(c>='0'&&c<='9')||c=='_'||c=='-'))return 0;}return 1;}
static int send_shell_control(const char *command,const char*key,const char*value){if(!safe_field(command)||(key&&!safe_field(key))||(value&&!numeric_allowed(value)))return 30;if(send_ipc(CRIT_IPC_SOC,BREW_PIZZAHEN_SHELL_SERVICE,"{}")!=0)return 35;char token[48];snprintf(token,sizeof(token),"%s",g_status_token[0]?g_status_token:"pizzahen");unlink(SHELL_CONTROL_ACK);unlink(SHELL_CONTROL_REQUEST);unlink(SHELL_CONTROL_REQUEST_TMP);FILE*f=fopen(SHELL_CONTROL_REQUEST_TMP,"w");if(!f)return 31;fprintf(f,"token=%s\ncommand=%s\nkey=%s\nvalue=%s\n",token,command,key?key:"none",value?value:"0");fflush(f);fsync(fileno(f));fclose(f);if(rename(SHELL_CONTROL_REQUEST_TMP,SHELL_CONTROL_REQUEST)!=0)return 32;for(int ms=0;ms<5000;ms+=50){int fd=open(SHELL_CONTROL_ACK,O_RDONLY);if(fd>=0){char b[512];ssize_t n=read(fd,b,sizeof(b)-1);close(fd);if(n>0){b[n]=0;char want[80];snprintf(want,sizeof(want),"token=%s",token);if(strstr(b,want)){unlink(SHELL_CONTROL_ACK);return strstr(b,"status=ok")?0:34;}}}usleep(50000);}return 33;}

static int is_shell_key(const char*k){static const char*keys[]={
  "overlay_gpu","overlay_cpu","overlay_ram","overlay_fps","overlay_ip","overlay_kstuff","all_cpu_usage","Overlay_pos",
  "Display_tids","etaHEN_Game_Options","Allow_data_in_sandbox","ALLOW_FTP_DEV_ACCESS","StartOption","Rest_Mode_Delay_Seconds",
  "Util_rest_kill","Game_rest_kill","toolbox_auto_start","disable_toolbox_auto_start_for_rest_mode","APP_JB_Debug_Msg",
  "enable_kstuff_on_close","pause_kstuff_on_open","pause_kstuff_on_open_secs","auto_eject_disc","LiteMode",
  "Cheats_shortcut_opt","Toolbox_shortcut_opt","Games_shortcut_opt","Kstuff_shortcut_opt"};
  if(!k)return 0;for(size_t i=0;i<sizeof(keys)/sizeof(keys[0]);i++)if(!strcmp(k,keys[i]))return 1;return 0;}

static int eta_service_toggle(const char *key,int on,int cmd,int is_v2){int old=config_get_int(key,0);char json[96];if(cmd==BREW_UTIL_TOGGLE_DPI)snprintf(json,sizeof(json),"{ \"toggle\": %d, \"is_v2\": %d }",on?1:0,is_v2?1:0);else snprintf(json,sizeof(json),"{ \"toggle\": %d }",on?1:0);int rc=send_ipc(UTIL_IPC_SOC,cmd,json);if(rc)return rc;char v[2]={on?'1':'0',0};rc=config_set_numeric(key,v);if(rc){if(cmd==BREW_UTIL_TOGGLE_DPI)snprintf(json,sizeof(json),"{ \"toggle\": %d, \"is_v2\": %d }",old?1:0,is_v2?1:0);else snprintf(json,sizeof(json),"{ \"toggle\": %d }",old?1:0);(void)send_ipc(UTIL_IPC_SOC,cmd,json);return rc;}reload_daemons();return 0;}

static int is_action_name(const char*s){static const char*a[]={"open","set","reload-settings","dpi1-on","dpi1-off","legacy-cmd-on","legacy-cmd-off","pkg-scan","games-list","launch-game","plugin-launch","plugin-stop","plugin-autostart","plugin-scan","payload-repo-refresh","payload-repo-install","pizza-overlay-stop","kstuff-pause","store-download","elfldr-start","download-kstuff","remove-kstuff","kstuff-autoload-on","kstuff-autoload-off","testkit","dumper-launch","install-store","ps5debug-on","ps5debug-off","remote-play-pin","debug-services-open","game-options-ensure","locale-set"};if(!s)return 0;for(size_t i=0;i<sizeof(a)/sizeof(a[0]);i++)if(!strcmp(s,a[i]))return 1;return 0;}
static int find_action_index(int argc, char **argv) {
  if (argc > 0 && is_action_name(argv[0])) return 0;
  if (argc > 1 && is_action_name(argv[1])) return 1;
  return -1;
}

/* websrv 0.34 splits the /hbldr args string directly into argv.  Keep every
   action parameter relative to whichever argv slot contains the action. */
static const char *action_arg(int argc, char **argv, int action_index, int offset) {
  const int i = action_index + offset;
  if (action_index < 0 || offset < 1 || i < 0 || i >= argc || !argv[i]) return NULL;
  if (!strncmp(argv[i], "tx=", 3)) return NULL;
  return argv[i];
}

int main(int argc, char **argv) {
  capture_status_token(argc, argv);
  unlink(STATUS_FILE);
  const int action_index = find_action_index(argc, argv);
  const char *action = action_index >= 0 ? argv[action_index] : "open";
  int rc = 0;
  if(!strcmp(action,"open"))return finish("ok:websrv","fail:websrv",0);
  if(!strcmp(action,"reload-settings")){reload_daemons();return finish("ok:reload-settings","fail:reload-settings",0);}
  if(!strcmp(action,"dpi1-on")||!strcmp(action,"dpi1-off")){int on=!strcmp(action,"dpi1-on");rc=eta_service_toggle("DPI",on,BREW_UTIL_TOGGLE_DPI,0);return finish(on?"ok:dpi1-on":"ok:dpi1-off","fail:dpi1",rc);}
  if(!strcmp(action,"legacy-cmd-on")||!strcmp(action,"legacy-cmd-off")){int on=!strcmp(action,"legacy-cmd-on"),old=config_get_int("legacy_cmd_server",0);char j[48];snprintf(j,sizeof(j),"{ \"toggle\": %d }",on);rc=send_ipc(UTIL_IPC_SOC,BREW_UTIL_TOGGLE_LEGACY_CMD_SERVER,j);if(!rc){char v[2]={on?'1':'0',0};rc=config_set_numeric("legacy_cmd_server",v);if(rc){snprintf(j,sizeof(j),"{ \"toggle\": %d }",old?1:0);(void)send_ipc(UTIL_IPC_SOC,BREW_UTIL_TOGGLE_LEGACY_CMD_SERVER,j);}else reload_daemons();}return finish(on?"ok:legacy-cmd-on":"ok:legacy-cmd-off","fail:legacy-cmd",rc);}
  if(!strcmp(action,"set")){const char *key = action_arg(argc, argv, action_index, 1); const char *value = action_arg(argc, argv, action_index, 2);if(!key||!value)return finish("ok:set","fail:set-args",7);rc=config_set_numeric(key,value);if(!rc)rc=mirror_shell_config();if(!rc)reload_daemons();if(!rc&&is_shell_key(key))rc=send_shell_control("set",key,value);return finish("ok:set","fail:set",rc);}
  if(!strcmp(action,"ps5debug-on")){rc=send_ipc(CRIT_IPC_SOC,BREW_TOGGLE_PS5DEBUG,"{}");if(!rc)rc=config_set_numeric("PS5Debug","1");return finish("ok:ps5debug-on","fail:ps5debug",rc);}
  if(!strcmp(action,"ps5debug-off")){/* etaHEN source states PS5Debug requires restart to disable. */rc=config_set_numeric("PS5Debug","0");return finish("ok:ps5debug-off-next-reboot","fail:ps5debug-off",rc);}
  if(!strcmp(action,"kstuff-pause")){const char*m=action_arg(argc, argv, action_index, 1);if(!m||strlen(m)!=1||m[0]<'0'||m[0]>'3')return finish("ok:kstuff-pause","fail:kstuff-pause-mode",7);rc=send_shell_control("kstuff_pause",NULL,m);return finish("ok:kstuff-pause","fail:kstuff-pause",rc);}
  if(!strcmp(action,"kstuff-autoload-on")||!strcmp(action,"kstuff-autoload-off")){int on=!strcmp(action,"kstuff-autoload-on");mkdir("/user/data/PIZZA_HEN",0777);if(on){rc=unlink("/user/data/PIZZA_HEN/no_kstuff");if(rc&&errno==ENOENT)rc=0;}else{int fd=open("/user/data/PIZZA_HEN/no_kstuff",O_WRONLY|O_CREAT|O_TRUNC,0777);if(fd<0)rc=errno?errno:1;else{close(fd);rc=0;}}return finish(on?"ok:kstuff-autoload-on":"ok:kstuff-autoload-off","fail:kstuff-autoload",rc);}
  if(!strcmp(action,"remote-play-pin")){rc=send_shell_control("remote_play_pin",NULL,"0");return finish("ok:remote-play-pin","fail:remote-play-pin",rc);}
  if(!strcmp(action,"game-options-ensure")){rc=mirror_shell_config();if(!rc)rc=send_ipc(CRIT_IPC_SOC,BREW_PIZZAHEN_SHELL_SERVICE,"{}");return finish("ok:game-options-ready","fail:game-options-ready",rc);}
  if(!strcmp(action,"debug-services-open")){
    /* FIX70.51: arm only. The actual Toolbox open is performed by the
       byte-exact v0.1 /data/PIZZA_HEN/bin/pizzahen-toolbox-open.elf helper,
       launched through websrv /hbldr exactly like the released v0.1 path. */
    const char *marker="/system_tmp/pizzahen_debug_services_active";
    int fd=open(marker,O_WRONLY|O_CREAT|O_TRUNC,0777);
    if(fd<0)return finish("ok:debug-services-open","fail:debug-services-marker",errno?errno:1);
    close(fd);
    return finish("ok:debug-services-armed","fail:debug-services-marker",0);
  }
  if(!strcmp(action,"locale-set")){const char*l=action_arg(argc,argv,action_index,1);return finish("ok:locale-set","fail:locale-set",persist_ui_locale(l));}
  /* PIZZA HEN v1.0: legacy Toolbox cheat IPC actions retired.
     CheatRunner v0.17 owns the active cheat API on 127.0.0.1:9999. */
  if(!strcmp(action,"pkg-scan"))return finish("ok:pkg-scan","fail:pkg-scan",send_ipc(UTIL_IPC_SOC,BREW_UTIL_SCAN_USB_PKGS,"{}"));
  if(!strcmp(action,"games-list"))return finish("ok:games-list","fail:games-list",send_ipc(UTIL_IPC_SOC,BREW_UTIL_GET_GAMES_LIST,"{ \"shortcut\": 0 }"));
  if(!strcmp(action,"launch-game")){const char*id=action_arg(argc, argv, action_index, 1);if(!id)return finish("ok:launch-game","fail:launch-game-id",7);char j[512];snprintf(j,sizeof(j),"{ \"button_id\": \"%s\" }",id);return finish("ok:launch-game","fail:launch-game",send_ipc(UTIL_IPC_SOC,BREW_UTIL_LAUNCH_GAME_BY_BUTTON_ID,j));}
  if(!strcmp(action,"plugin-launch")){const char *plugin_path = action_arg(argc, argv, action_index, 1);const char *title_id = action_arg(argc, argv, action_index, 2);if(!plugin_path||strchr(plugin_path,'"'))return finish("ok:plugin-launch","fail:plugin-args",7);if(!title_id||!*title_id){const char *slash=strrchr(plugin_path,'/');title_id=slash?slash+1:plugin_path;}if(strchr(title_id,'"'))return finish("ok:plugin-launch","fail:plugin-title",7);char j[DAEMON_BUFF_MAX];snprintf(j,sizeof(j),"{ \"plugin_path\": \"%s\", \"title_id\": \"%s\" }",plugin_path,title_id);return finish("ok:plugin-launch","fail:plugin-launch",send_ipc(UTIL_IPC_SOC,BREW_UTIL_LAUNCH_PLUGIN,j));}
  if(!strcmp(action,"plugin-stop")){const char*p=action_arg(argc, argv, action_index, 1),*t=action_arg(argc, argv, action_index, 2),*k=action_arg(argc, argv, action_index, 3);if(!p||!t||!k)return finish("ok:plugin-stop","fail:plugin-stop-args",7);char j[DAEMON_BUFF_MAX];snprintf(j,sizeof(j),"{ \"plugin_path\": \"%s\", \"title_id\": \"%s\", \"is_payload\": %d }",p,t,!strcmp(k,"payload"));return finish("ok:plugin-stop","fail:plugin-stop",send_ipc(UTIL_IPC_SOC,BREW_UTIL_STOP_PLUGIN,j));}
  if(!strcmp(action,"plugin-autostart")){const char*p=action_arg(argc, argv, action_index, 1),*e=action_arg(argc, argv, action_index, 2);if(!p||!e)return finish("ok:plugin-autostart","fail:plugin-autostart-args",7);char j[DAEMON_BUFF_MAX];snprintf(j,sizeof(j),"{ \"plugin_path\": \"%s\", \"enabled\": %d }",p,atoi(e)?1:0);return finish("ok:plugin-autostart","fail:plugin-autostart",send_ipc(UTIL_IPC_SOC,BREW_UTIL_SET_PLUGIN_AUTOSTART,j));}
  if(!strcmp(action,"plugin-scan"))return finish("ok:plugin-scan","fail:plugin-scan",send_ipc(UTIL_IPC_SOC,BREW_UTIL_SCAN_PLUGINS,"{}"));
  if(!strcmp(action,"payload-repo-refresh"))return finish("ok:payload-repo-refresh","fail:payload-repo-refresh",send_ipc(UTIL_IPC_SOC,BREW_UTIL_REFRESH_PAYLOAD_REPO,"{}"));
  if(!strcmp(action,"payload-repo-install")){const char*f=action_arg(argc,argv,action_index,1);if(!f||!*f||strchr(f,'/')||strstr(f,"..")||strchr(f,'"'))return finish("ok:payload-repo-install","fail:payload-repo-args",7);char j[DAEMON_BUFF_MAX];snprintf(j,sizeof(j),"{ \"filename\": \"%s\" }",f);return finish("ok:payload-repo-install","fail:payload-repo-install",send_ipc(UTIL_IPC_SOC,BREW_UTIL_INSTALL_PAYLOAD_REPO,j));}
  if(!strcmp(action,"pizza-overlay-stop")){rc=unlink("/data/phu_overlay.lock");if(rc&&errno==ENOENT)rc=0;return finish("ok:pizza-overlay-stop","fail:pizza-overlay-stop",rc);}
  if(!strcmp(action,"store-download"))return finish("ok:store-download","fail:store-download",send_ipc(UTIL_IPC_SOC,BREW_UTIL_DOWNLOAD_STORE,"{}"));
  if(!strcmp(action,"download-kstuff"))return finish("ok:download-kstuff","fail:download-kstuff",send_ipc(UTIL_IPC_SOC,BREW_UTIL_DOWNLOAD_KSTUFF,"{}"));
  if(!strcmp(action,"remove-kstuff")){rc=unlink("/data/PIZZA_HEN/kstuff.elf");if(rc&&errno==ENOENT)rc=0;return finish("ok:remove-kstuff","fail:remove-kstuff",rc);}
  if(!strcmp(action,"testkit"))return finish("ok:testkit","fail:testkit",send_ipc(CRIT_IPC_SOC,BREW_TESTKIT_CHECK,"{}"));
  if(!strcmp(action,"dumper-launch"))return finish("ok:dumper-launch","fail:dumper-launch",send_ipc(CRIT_IPC_SOC,BREW_LAUNCH_DUMPER,"{}"));
  if(!strcmp(action,"install-store"))return finish("ok:install-store","fail:install-store",send_ipc(CRIT_IPC_SOC,BREW_INSTALL_THE_STORE,"{}"));
  if(!strcmp(action,"elfldr-start"))return finish("ok:elfldr-start","fail:elfldr-start",send_ipc(UTIL_IPC_SOC,BREW_UTIL_LAUNCH_ELFLDR,"{}"));
  return finish("ok:noop","fail:unknown-action",7);
}
