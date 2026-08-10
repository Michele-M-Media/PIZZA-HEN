from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
main=(SRC/'bootstrapper/source/main.cpp').read_text(encoding='utf-8')
cm=(SRC/'bootstrapper/CMakeLists.txt').read_text(encoding='utf-8')
unpack=(SRC/'unpacker/CMakeLists.txt').read_text(encoding='utf-8')
bs=(ROOT/'build_pizzahen_multisdk.sh').read_text(encoding='utf-8')
checks=[]
def ok(name, cond): checks.append((name, bool(cond)))

ok('PAD_HEADER', '#include <pad.hpp>' in main)
ok('PAD_LINK', 'ScePad' in cm)
ok('PAD_INCLUDE_PATH', '../daemon/include' in cm)
ok('PAD_INIT', 'scePadInit()' in main)
ok('PAD_PRIV_BEST_EFFORT', 'scePadSetProcessPrivilege(1)' in main)
ok('PAD_OPEN_FOREGROUND_USER', 'sceUserServiceGetForegroundUser(&user_id)' in main and 'scePadOpen(user_id' in main)
ok('PAD_CROSS_LITE', 'ORBIS_PAD_BUTTON_CROSS' in main and 'strncpy(out, "lite"' in main)
ok('PAD_CIRCLE_DR', 'ORBIS_PAD_BUTTON_CIRCLE' in main and 'strncpy(out, "dr"' in main)
ok('PAD_DEBOUNCE', 'data.buttons & ~previous' in main)
ok('PAD_TIMEOUT_MANUAL_ONLY', 'timeout_ms = 120000' in main and 'return 0;' in main)
ok('NO_FAKE00000_LAUNCH', 'sceLncUtilLaunchApp("FAKE00000"' not in main)
ok('NO_FAKE00000_REGISTRATION_ASSUMPTION', 'websrv installs FAKE00000 itself' not in main)
ok('NO_MEDIA_METADATA_WRITE', '/user/app/FAKE00000/sce_sys/param.json' not in main)
ok('REMOTE_FALLBACK_ONLY', 'W2-FALLBACK: starting remote selector on port 8080' in main)
ok('REMOTE_SELECTOR_REQUEST_CHANNEL', 'wait_for_web_kstuff_request' in main and 'kstuff_request.txt' in main)
ok('ONE_ENGINE_GUARD', 'KStuff already active; refusing second engine' in main)
ok('LITE_ENGINE_PRESENT', 'kstuff-lite-1.09' in main)
ok('DR_ENGINE_PRESENT', 'kstuff-dr-1.2' in main)
ok('FIX22_TARGET', 'PIZZA-HEN-v0.1-FIX22-PAD-KSTUFF-SELECTOR.elf' in unpack)
ok('FIX22_BUILD_OUTPUT', 'PIZZA-HEN-v0.1-FIX22-PAD-KSTUFF-SELECTOR' in bs)
failed=[n for n,v in checks if not v]
for n,v in checks: print(f'{n}={"PASS" if v else "FAIL"}')
print(f'FIX22_STATIC={sum(v for _,v in checks)}/{len(checks)} PASS' if not failed else f'FIX22_STATIC_FAIL={failed}')
sys.exit(1 if failed else 0)
