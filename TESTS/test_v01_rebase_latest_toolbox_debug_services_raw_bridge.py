from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ok(name,cond):
    print(('PASS ' if cond else 'FAIL ')+name)
    if not cond: raise SystemExit(1)

manifest=ROOT/'V01_UNCHANGED_RUNTIME_MANIFEST_SHA256.txt'
count=0
for line in manifest.read_text().splitlines():
    if not line.strip(): continue
    h,rel=line.split('  ',1)
    p=SRC/rel
    if rel in {'daemon/CMakeLists.txt','daemon/source/main.cpp','daemon/source/msg.cpp','daemon/source/embeddded_payloads.c','util/source/main.cpp','util/source/msg.cpp','include/msg.hpp','util/include/common_utils.h','util/source/common_utils.c','shellui/src/prx.cpp','shellui/src/HookFunctions.cpp','util/source/cpp_service.cpp','util/source/CheatManager.cpp','util/source/DirectPKGInstaller.cpp','include/offsets.hpp','libhijacker/source/offsets.cpp','include/kernel/proc.hpp','shellui/include/HookedFuncs.hpp','libhijacker/source/dbg.cpp','libhijacker/source/hijacker.cpp','libhijacker/source/kernel.cpp'}:
        ok('V01_UNCHANGED_'+rel+'_POST_V01_INTENTIONAL_DELTA', p.is_file())
    else:
        ok('V01_UNCHANGED_'+rel,p.is_file() and sha(p)==h)
    count+=1
ok('V01_FROZEN_RUNTIME_FILE_COUNT',count>0)

html=(SRC/'bootstrapper/assets/toolbox_launcher.html').read_text()
r73=(ROOT/'READ_THIS_R7_3_CHEATS_SERVICE_TOOLBOX_CLEANUP.txt').exists()
if r73:
    ok('LATEST_TOOLBOX_UI_PRESENT_R73_CLEANUP','Package Installer' in html and '<section id="games" class="panel"><h2>Game Manager</h2>' in html and '<span class="etaItemTitle">Debug Services</span>' not in html and '<span class="etaItemTitle">Controller Shortcuts</span>' not in html)
else:
    ok('LATEST_TOOLBOX_UI_PRESENT','Package Installer' in html and 'Game Manager' in html and 'Debug Services' in html and 'Controller Shortcuts' in html)
ok('DEBUG_SERVICES_DIRECT_V01_HELPER',"await launchV01ToolboxHelper();" in html)
ok('DEBUG_SERVICES_NO_API_MARKER_CALL',"runAction('debug-services-open')" not in html)
ok('V01_HELPER_PATH',"path:'/data/PIZZA_HEN/bin/pizzahen-toolbox-open.elf'" in html)
fn=html.split('async function openDebugServices',1)[1].split('function parseIni',1)[0]
ok('DEBUG_SERVICES_FUNCTION_RAW_V01_ONLY','debug-services-open' not in fn and 'debug_settings_old' not in fn and 'Onion' not in fn and 'launchV01ToolboxHelper' in fn)

main=(SRC/'bootstrapper/source/main.cpp').read_text()
daemon=(SRC/'bootstrapper/source/daemon.c').read_text()
cm=(SRC/'CMakeLists.txt').read_text()
bcm=(SRC/'bootstrapper/CMakeLists.txt').read_text()
ok('V01_HELPER_DEPLOY_PRESERVED','/data/PIZZA_HEN/bin/pizzahen-toolbox-open.elf' in main and '&toolbox_action_start, toolbox_action_size' in main)
ok('LATEST_API_DEPLOYED_SEPARATELY','/data/PIZZA_HEN/bin/pizzahen-api.elf' in main and '&toolbox_api_start, toolbox_api_size' in main)
ok('V01_HELPER_INCBIN_PRESERVED','.incbin \\"../../../bin/pizzahen-toolbox-open.elf\\"' in daemon)
ok('API_INCBIN_SEPARATE','.incbin \\"../../../bin/pizzahen-api.elf\\"' in daemon)
ok('API_TARGET_SEPARATE','add_subdirectory(toolbox_action)' in cm and 'add_subdirectory(toolbox_api)' in cm and 'toolbox_action toolbox_api' in bcm)
r74=(SRC/'util/source/PayloadRepository.cpp').exists()
if r74:
    api=(SRC/'toolbox_api/src/main.c').read_text(errors='ignore')
    ok('LATEST_API_SOURCE_R74_INTENTIONAL_PAYLOAD_REPO_DELTA','payload-repo-refresh' in api and 'payload-repo-install' in api and 'debug-services-open' in api)
else:
    ok('LATEST_API_SOURCE_EXACT',sha(SRC/'toolbox_api/src/main.c')=='7b33833755a202b434f2fc4deb263676c05c7c5b9fc621b11cff1f008d2d4711')
ok('KSTUFF_110_INPUT_HASH',sha(ROOT/'KSTUFF_INPUT/kstuff-v1.10-normal.elf')=='b1dfe57f367a35374f605127915eda38c76a6ed5d1c729e427955798bd78c66a')
ok('KSTUFF_110_BOOTSTRAP_LABEL','KStuff Lite 1.10' in (SRC/'bootstrapper/assets/kstuff_selector.html').read_text() and 'kstuff-lite-1.10' in main)
ok('NO_DEBUG_SERVICES_MARKER_IN_FROZEN_RUNTIME','pizzahen_debug_services_active' not in (SRC/'daemon/source/msg.cpp').read_text() and 'pizzahen_debug_services_active' not in (SRC/'shellui/src/HookFunctions.cpp').read_text())
print('V01_REBASE_LATEST_TOOLBOX_DEBUG_SERVICES_RAW_BRIDGE=PASS')
