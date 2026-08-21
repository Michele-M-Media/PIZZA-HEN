#!/usr/bin/env python3
from pathlib import Path
import json

root=Path(__file__).resolve().parents[1]
src=root/'Source Code'
param_path=src/'bootstrapper/assets/toolbox_shortcut_param.json'
param=json.loads(param_path.read_text())
boot=(src/'bootstrapper/source/main.cpp').read_text()
daemon_msg=(src/'daemon/source/msg.cpp').read_text()
daemon_main=(src/'daemon/source/main.cpp').read_text()
launcher=(src/'bootstrapper/assets/toolbox_launcher.html').read_text()
top_cmake=(src/'CMakeLists.txt').read_text()
boot_cmake=(src/'bootstrapper/CMakeLists.txt').read_text()
unpacker=(src/'unpacker/CMakeLists.txt').read_text()
action=(src/'toolbox_action/src/main.c').read_text()
action_cmake=(src/'toolbox_action/CMakeLists.txt').read_text()
embed=(src/'bootstrapper/source/daemon.c').read_text()

checks=[]
def ok(name, cond):
    checks.append((name,bool(cond)))
    print(f'{name}={"PASS" if cond else "FAIL"}')

ok('MEDIA_CATEGORY_65536', param.get('applicationCategoryType') == 65536)
ok('MEDIA_TITLE_ID', param.get('titleId') == 'PZHN00001')
ok('MEDIA_DEEPLINK_LOCAL_WEBSRV', param.get('deeplinkUri') == 'http://127.0.0.1:8080/fs/data/PIZZA_HEN/ui/toolbox-launcher.html')
ok('MEDIA_SELF_UPDATE_CONTENT_COMPARE', 'shortcut_needs_update' in boot and 'memcmp(buf, expected, expected_size)' in boot)
ok('MEDIA_NO_STALE_MARKER_GATE', 'toolbox_shortcut_registered' not in boot)
ok('APPINST_TITLEDIR', 'sceAppInstUtilAppInstallTitleDir(title_id, "/user/app/", nullptr)' in boot)
ok('APPINST_TERMINATE', 'sceAppInstUtilTerminate();' in boot)
ok('MEDIA_LEGACY_CATEGORY_MIGRATION', 'shortcut_param_is_legacy_non_media' in boot and 'sceAppInstUtilAppUnInstall(title_id)' in boot)
ok('BROWSER_TOOLBOX_MODE_MARKER', 'browser_toolbox_mode' in boot and '/data/PIZZA_HEN/runtime/browser_toolbox_mode' in boot)
ok('MEDIA_TILE_BEFORE_DAEMONS', boot.find('install_pizzahen_toolbox_shortcut()') < boot.find('Starting Utility etaHEN services'))
ok('BOOT_BROWSER_UI_WITH_TOOLBOX_HOOK_PRELOAD', 'global_conf.toolbox_auto_start = false;' in daemon_main and 'browser_toolbox_mode' in daemon_main and 'cmd_preload_toolbox_hooks()' in daemon_main)

start=daemon_msg.find('bool cmd_enable_toolbox()')
end=daemon_msg.find('void handleIPC', start)
cmd=daemon_msg[start:end] if start >= 0 and end > start else ''
ok('TOOLBOX_FAILURE_NEVER_KILLS_SHELLUI', 'ForceKillProc(pid)' not in cmd)
ok('TOOLBOX_FAILURE_REBRANDED', 'Failed to load the PIZZA HEN Toolbox' in cmd and 'Failed to inject the PIZZA HEN Toolbox' in cmd)
ok('CONFIG_CREATED_LOG_ONLY', 'PIZZA HEN config created @ /data/PIZZA_HEN/config.ini' in daemon_msg and 'notify(true, "etaHEN config created!' not in daemon_msg)
notify_daemon=(src/'daemon/source/commands.cpp').read_text()
notify_util=(src/'util/source/common_utils.c').read_text()
ok('USER_NOTIFY_PREFIX_PIZZA_HEN', '[PIZZA HEN] %s' in notify_daemon and '[PIZZA HEN] %s' in notify_util)

ok('TOOLBOX_ACTION_SUBPROJECT', 'add_subdirectory(toolbox_action)' in top_cmake)
ok('TOOLBOX_ACTION_DEPENDENCY', 'toolbox_action' in boot_cmake)
ok('TOOLBOX_ACTION_EMBEDDED', 'pizzahen-toolbox-open.elf' in embed and 'toolbox_action_start' in embed)
ok('TOOLBOX_ACTION_WRITTEN', '/data/PIZZA_HEN/bin/pizzahen-toolbox-open.elf' in boot)
ok('TOOLBOX_ACTION_IPC', 'BREW_ENABLE_TOOLBOX 0x09000011' in action and '/system_tmp/etaHEN_crit_service' in action)
ok('TOOLBOX_ACTION_STATUS', 'toolbox_action_status.txt' in action)
ok('TOOLBOX_ACTION_BUILD', 'OUTPUT_NAME "pizzahen-toolbox-open.elf"' in action_cmake)
ok('LAUNCHER_HBLDR_ON_DEMAND', "/hbldr?" in launcher and 'pizzahen-toolbox-open.elf' in launcher)
ok('LAUNCHER_SAFE_FAILURE_TEXT', 'You can safely try again' in launcher)
ok('LAUNCHER_OPENS_SETTINGS_AFTER_SUCCESS', 'pizzahen-toolbox-open.elf' in launcher and 'pssettings:play?mode=settings&function=debug_settings' in daemon_msg)
ok('FIX32_FINAL_TARGET', 'PIZZA-HEN-v0.1-FIX45-PLUGIN-MANAGER-LIFECYCLE.elf' in unpacker)

failed=[n for n,v in checks if not v]
if failed:
    raise SystemExit('FIX32_STATIC_FAIL='+','.join(failed))
print(f'FIX32_STATIC={len(checks)}/{len(checks)} PASS')
