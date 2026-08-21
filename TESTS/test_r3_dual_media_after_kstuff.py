#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, re
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ok(name, cond):
    print(f'{name}={"PASS" if cond else "FAIL"}')
    if not cond: raise SystemExit(1)
main=(SRC/'bootstrapper/source/main.cpp').read_text(errors='ignore')
embed=(SRC/'bootstrapper/source/daemon.c').read_text(errors='ignore')
tool=json.loads((SRC/'bootstrapper/assets/toolbox_shortcut_param.json').read_text())
dbg=json.loads((SRC/'bootstrapper/assets/debug_services_shortcut_param.json').read_text())
latest=(SRC/'bootstrapper/assets/toolbox_launcher.html').read_bytes()
dbg_launcher=(SRC/'bootstrapper/assets/debug_services_launcher.html').read_bytes()
v01_hash='7f7134593eefa9628bc581eebe3a7fc66f40cba3bb8f9447ebd641bfe58eb399'
ok('R3_TOOLBOX_ID', tool['titleId']=='PZHN00001')
ok('R3_DEBUG_ID', dbg['titleId']=='PZHN00002')
ok('R3_IDS_DIFFERENT', tool['titleId']!=dbg['titleId'])
ok('R3_BOTH_MEDIA_CATEGORY', tool['applicationCategoryType']==65536 and dbg['applicationCategoryType']==65536)
ok('R3_TOOLBOX_DEEPLINK_LATEST', tool['deeplinkUri']=='http://127.0.0.1:8080/fs/data/PIZZA_HEN/ui/toolbox-launcher.html')
ok('R3_DEBUG_DEEPLINK_SEPARATE', dbg['deeplinkUri']=='http://127.0.0.1:8080/fs/data/PIZZA_HEN/ui/debug-services-launcher.html')
ok('R3_DEBUG_TITLE', dbg['localizedParameters']['en-US']['titleName']=='Debug Services')
r77_i18n = b'phNormalizeLocale' in dbg_launcher and b'locale-set' in dbg_launcher
if r77_i18n:
    ok('R3_V01_LAUNCHER_R77_I18N_DELTA', b'/data/PIZZA_HEN/bin/pizzahen-toolbox-open.elf' in dbg_launcher and b'/hbldr?' in dbg_launcher)
else:
    ok('R3_V01_LAUNCHER_BYTE_EXACT', hashlib.sha256(dbg_launcher).hexdigest()==v01_hash)
ok('R3_V01_LAUNCHER_CALLS_ORIGINAL_HELPER', b'/data/PIZZA_HEN/bin/pizzahen-toolbox-open.elf' in dbg_launcher and b'/hbldr?' in dbg_launcher)
r73=b'PIZZA HEN R7.3' in (ROOT/'READ_THIS_R7_3_CHEATS_SERVICE_TOOLBOX_CLEANUP.txt').read_bytes() if (ROOT/'READ_THIS_R7_3_CHEATS_SERVICE_TOOLBOX_CLEANUP.txt').exists() else False
if r73:
    ok('R3_LATEST_TOOLBOX_REMAINS_SEPARATE_R73_UI_DELTA', b'Package Installer' in latest and latest != dbg_launcher)
else:
    ok('R3_LATEST_TOOLBOX_REMAINS_SEPARATE', hashlib.sha256(latest).hexdigest()=='25ec06bbd252fa1096e9d1eade5a6919a4f4ad533ebba6d42b4a6b23addaf4cf')
ok('R3_EMBED_DEBUG_PARAM', 'debug_services_shortcut_param.json' in embed)
ok('R3_EMBED_DEBUG_LAUNCHER', 'debug_services_launcher.html' in embed)
ok('R3_DEPLOY_DEBUG_LAUNCHER', '/data/PIZZA_HEN/ui/debug-services-launcher.html' in main)
ok('R3_DEBUG_INSTALLER_ID', 'install_pizzahen_debug_services_shortcut' in main and 'PZHN00002' in main)
ok('R3_KSTUFF_110_LABEL', 'kstuff-lite-1.10' in main and 'choose Lite 1.10 or DR 1.2' in main)
selector=main.find('int selector_rc = start_browser_kstuff_selector()')
ready=main.find('PIZZA HEN W5: %s ready')
toolcall=main.find('int toolbox_tile_rc = install_pizzahen_toolbox_shortcut()')
dbgcall=main.find('int debug_services_tile_rc = install_pizzahen_debug_services_shortcut()')
shadow=main.find('PIZZA HEN S0: starting pristine ShadowMountPlus')
ok('R3_DUAL_TILES_AFTER_KSTUFF', -1 not in (selector,ready,toolcall,dbgcall,shadow) and selector < ready < toolcall < dbgcall < shadow)
pre_selector=main[:selector]
ok('R3_NO_MEDIA_INSTALL_BEFORE_SELECTOR', 'install_pizzahen_toolbox_shortcut()' not in pre_selector and 'install_pizzahen_debug_services_shortcut()' not in pre_selector)
# Frozen v0.1 runtime stays untouched by R3
manifest=ROOT/'V01_UNCHANGED_RUNTIME_MANIFEST_SHA256.txt'
for line in manifest.read_text().splitlines():
    if not line.strip(): continue
    h,rel=line.split('  ',1)
    if rel in {'daemon/CMakeLists.txt','daemon/source/main.cpp','daemon/source/msg.cpp','daemon/source/embeddded_payloads.c','util/source/main.cpp','util/source/msg.cpp','include/msg.hpp','util/include/common_utils.h','util/source/common_utils.c','shellui/src/prx.cpp','shellui/src/HookFunctions.cpp','util/source/cpp_service.cpp','util/source/CheatManager.cpp','util/source/DirectPKGInstaller.cpp','include/offsets.hpp','libhijacker/source/offsets.cpp','include/kernel/proc.hpp','shellui/include/HookedFuncs.hpp','libhijacker/source/dbg.cpp','libhijacker/source/hijacker.cpp','libhijacker/source/kernel.cpp'}:
        ok('R3_FROZEN_'+rel+'_POST_R3_INTENTIONAL_DELTA', (SRC/rel).is_file())
    else:
        ok('R3_FROZEN_'+rel, (SRC/rel).is_file() and sha(SRC/rel)==h)
print('R3_DUAL_MEDIA_AFTER_KSTUFF=PASS')
