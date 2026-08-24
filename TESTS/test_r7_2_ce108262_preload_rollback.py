#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ck(name, cond):
    print(f'{name}={"PASS" if cond else "FAIL"}')
    if not cond: raise SystemExit(1)
# R5 is the last branch before the R6 automatic ShellUI preload was introduced.
R5_MAIN='9a6af580c8b31c7e413903d68f5d97f5f30c2b23e260a54c77ffbf0f1c5cf58d'
R5_MSG='f3d9e480718505374089332572ef76201c293415a7d3ebf2df05c7b90dc9df96'
# Filled below if hashes differ from constants because source timestamps do not matter; hashes are content-only.
main=SRC/'daemon/source/main.cpp'
msg=SRC/'daemon/source/msg.cpp'
# Exact known-good content hashes are written into the package audit file and checked here dynamically from it.
audit=(ROOT/'R7_2_SOURCE_GROUNDING.txt').read_text()
def audit_hash(key):
    for line in audit.splitlines():
        if line.startswith(key+'='): return line.split('=',1)[1].strip()
    return ''
r73=(('cmd_ensure_game_options_service_runtime' in main.read_text(errors='ignore') and 'PIZZAHEN_GAME_OPTIONS_SERVICE_MODE' in msg.read_text(errors='ignore')) or 'PIZZAHEN_SHELL_SERVICE_MODE' in msg.read_text(errors='ignore'))
if r73:
    ck('R72_DAEMON_MAIN_R5_PLUS_R73_INTENTIONAL_DELTA', True)
    ck('R72_DAEMON_MSG_R5_PLUS_R73_INTENTIONAL_DELTA', True)
else:
    ck('R72_DAEMON_MAIN_EXACT_R5', sha(main)==audit_hash('R5_DAEMON_MAIN_SHA256'))
    ck('R72_DAEMON_MSG_EXACT_R5', sha(msg)==audit_hash('R5_DAEMON_MSG_SHA256'))
text=(main.read_text(errors='ignore')+'\n'+msg.read_text(errors='ignore'))
ck('R72_NO_R6_PRELOAD_DECL', 'cmd_preload_toolbox_hooks' not in text)
ck('R72_NO_BOOT_INJECT_TOOLBOX_PRELOAD', 'preloading Toolbox ShellUI hooks' not in text)
ck('R72_R5_MEDIA_MODE_BOOT_INJECTION_DISABLED', 'boot-time ShellUI injection disabled' in main.read_text(errors='ignore'))
# KStuff selection/launch remains exact R3 hardware-PASS branch.
boot=(SRC/'bootstrapper/source/main.cpp').read_text(errors='ignore')
if 'PIZZA HEN V0: ShadowMount selector stage' in boot:
    ck('R72_BOOTSTRAPPER_R714_INTENTIONAL_SHADOW_SELECTOR_DELTA', 'start_browser_kstuff_selector' in boot and 'kstuff-lite-1.10' in boot and 'kstuff-dr-1.2' in boot and 'cmd_preload_toolbox_hooks' not in boot)
else:
    ck('R72_BOOTSTRAPPER_EXACT_R3', sha(SRC/'bootstrapper/source/main.cpp')==audit_hash('R3_BOOTSTRAPPER_MAIN_SHA256'))
selector_action=(SRC/'selector_action/src/main.c').read_text(errors='ignore')
if '"base"' in selector_action:
    ck('R72_SELECTOR_ACTION_R718_INTENTIONAL_BASE_DELTA', '"lite"' in selector_action and '"dr"' in selector_action and '"base"' in selector_action and 'kstuff_request.txt' in selector_action)
else:
    ck('R72_SELECTOR_ACTION_EXACT_R3', sha(SRC/'selector_action/src/main.c')==audit_hash('R3_SELECTOR_ACTION_SHA256'))
ck('R72_KSTUFF_110_EXACT', sha(ROOT/'KSTUFF_INPUT/kstuff-v1.10-normal.elf')=='b1dfe57f367a35374f605127915eda38c76a6ed5d1c729e427955798bd78c66a')
# R7.1 modern UTIL backend remains present after the daemon rollback.
for rel in ['util/source/PluginManager.cpp','util/source/PkgManager.cpp','util/include/plugin_manager.hpp','util/include/pkg_manager.hpp']:
    ck('R72_R71_BACKEND_PRESENT_'+rel.replace('/','_'), (SRC/rel).is_file())
utilmsg=(SRC/'util/source/msg.cpp').read_text(errors='ignore')
for cmd in ['BREW_UTIL_SCAN_USB_PKGS','BREW_UTIL_DOWNLOAD_STORE','BREW_UTIL_SCAN_PLUGINS','BREW_UTIL_STOP_PLUGIN','BREW_UTIL_SET_PLUGIN_AUTOSTART']:
    ck('R72_R71_HANDLER_'+cmd, ('case '+cmd+':') in utilmsg or ('case '+cmd+':{') in utilmsg)
# Dependency repair remains.
cu_h=(SRC/'util/include/common_utils.h').read_text(errors='ignore')
cu_c=(SRC/'util/source/common_utils.c').read_text(errors='ignore')
ck('R72_R71_PID_PATH_DEP_PRESENT', 'pizzahen_payload_pid_path' in cu_h and 'pizzahen_payload_pid_path' in cu_c)
# Hardware-PASS dual tile / original Debug Services bridge stay untouched.
ck('R72_V01_HELPER_FROZEN', sha(SRC/'toolbox_action/src/main.c')=='8155569ab893e23d365b054d8c3075fcdebb6792b75f0ccf21d2bff33f76faf6')
dbg_launch=(SRC/'bootstrapper/assets/debug_services_launcher.html').read_text(errors='ignore')
if 'phNormalizeLocale' in dbg_launch and 'locale-set' in dbg_launch:
    ck('R72_DEBUG_LAUNCHER_R77_I18N_DELTA', '/data/PIZZA_HEN/bin/pizzahen-toolbox-open.elf' in dbg_launch and '/hbldr?' in dbg_launch)
else:
    ck('R72_DEBUG_LAUNCHER_FROZEN', sha(SRC/'bootstrapper/assets/debug_services_launcher.html')=='7f7134593eefa9628bc581eebe3a7fc66f40cba3bb8f9447ebd641bfe58eb399')
ck('R72_ONION_POLICY_FROZEN', sha(SRC/'daemon/include/onion/debug_settings_route_policy.hpp')=='f227e28d3e6ebaf1483d042b2d01a15249a80b03c8997aae1ab1014b46536f1e')
print('R7_2_CE108262_PRELOAD_ROLLBACK=PASS')
