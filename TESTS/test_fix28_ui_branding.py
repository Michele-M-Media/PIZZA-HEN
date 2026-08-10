from pathlib import Path
import struct
root=Path(__file__).resolve().parents[1]
main=(root/'Source Code/bootstrapper/source/main.cpp').read_text()
unpacker=(root/'Source Code/unpacker/source/main.c').read_text()
html=(root/'Source Code/bootstrapper/assets/kstuff_selector.html').read_text()
cm=(root/'Source Code/unpacker/CMakeLists.txt').read_text()
build=(root/'build_pizzahen_multisdk.sh').read_text()
assets=root/'Source Code/bootstrapper/assets'
checks=[]
def ok(name, cond):
    checks.append((name,bool(cond))); print(f"{name}={'PASS' if cond else 'FAIL'}")
ok('WELCOME_BRAND_PIZZA_HEN', 'PIZZA HEN is starting...' in main and 'etaHEN is starting...' not in main)
ok('WELCOME_NO_DEBUG_SETTINGS_ACTION', 'Go to Debug Settings' not in main)
ok('FINAL_READY_QUIET_LOG', 'PIZZA HEN E6: complete Toolbox runtime' in main and 'notify("PIZZA HEN ready")' not in main)
ok('DIAG_BOOTSTRAPPER_NOT_USER_NOTIFICATIONS', 'notify("PIZZA HEN DIAG B1:' not in main and 'ui_trace("PIZZA HEN DIAG B1:' in main)
ok('DIAG_UNPACKER_NOT_USER_NOTIFICATIONS', 'notify("PIZZA HEN DIAG U1:' not in unpacker and 'ui_trace("PIZZA HEN DIAG U1:' in unpacker)
ok('PIPELINE_SUCCESS_CHATTER_LOG_ONLY', 'ui_trace("PIZZA HEN W5:' in main and 'ui_trace("PIZZA HEN F3:' in main and 'ui_trace("PIZZA HEN D3:' in main)
ok('PIPELINE_FAILURES_STILL_VISIBLE', 'notify("PIZZA HEN W5-FAIL:' in main and 'notify("PIZZA HEN F3-FAIL:' in main and 'notify("PIZZA HEN D3-FAIL:' in main)
ok('USER_VISIBLE_DAEMON_ERRORS_REBRANDED', 'failed to launch the main PIZZA HEN daemon' in main and 'failed to launch the PIZZA HEN utility daemon' in main)
ok('SELECTOR_CONTAIN_NOT_COVER', 'object-fit:contain' in html and 'object-fit:cover' not in html)
ok('SELECTOR_SAFE_LOGO_FRAME', 'logoFrame' in html and 'width:88px;height:88px' in html)
for name in ['pizzahen_sicon.png','kstuff_selector_icon.png']:
    data=(assets/name).read_bytes()
    dims=struct.unpack('>II', data[16:24]) if data[:8]==b'\x89PNG\r\n\x1a\n' and len(data)>=24 else (0,0)
    ok(name.upper().replace('.','_')+'_PNG_64', dims==(64,64))
ok('ORIGINAL_LOGO_ASSET_PRESERVED', (assets/'pizzahen_sicon_original.png').exists() and (assets/'kstuff_selector_icon_original.png').exists())
ok('FIX28_TARGET', 'PIZZA-HEN-v0.1-FIX45-PLUGIN-MANAGER-LIFECYCLE.elf' in cm)
ok('FIX28_TEST_IN_BUILD', 'test_fix28_ui_branding.py' in build)
failed=[n for n,v in checks if not v]
if failed: raise SystemExit('FIX28_STATIC_FAIL='+','.join(failed))
print(f'FIX28_STATIC={len(checks)}/{len(checks)} PASS')
