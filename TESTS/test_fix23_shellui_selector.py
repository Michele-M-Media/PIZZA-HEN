from pathlib import Path
import sys, re, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
boot=(SRC/'bootstrapper/source/main.cpp').read_text(encoding='utf-8')
hook=(SRC/'shellui/src/HookFunctions.cpp').read_text(encoding='utf-8')
prx=(SRC/'shellui/src/prx.cpp').read_text(encoding='utf-8')
msg=(SRC/'daemon/source/msg.cpp').read_text(encoding='utf-8')
cm=(SRC/'unpacker/CMakeLists.txt').read_text(encoding='utf-8')
build=(ROOT/'build_pizzahen_multisdk.sh').read_text(encoding='utf-8')
checks=[]
def ok(name, cond): checks.append((name, bool(cond)))

ok('SHELLUI_SELECTOR_ENTRY', 'start_shellui_kstuff_selector' in boot)
ok('SHELLUI_INJECT', 'Inject_Toolbox(shellui_pid, shellui_prx_start)' in boot)
ok('SHELLUI_READY_GATE', 'wait_for_shellui_online(15)' in boot and 'pizzahen_kstuff_selector_ui_opened' in boot)
ok('SHELLUI_DEEPLINK', 'pssettings:play?mode=settings&function=debug_settings' in prx)
ok('NO_PAD_BLIND_SELECTOR', 'select_kstuff_with_pad' not in boot)
ok('NO_FAKE00000', 'FAKE00000' not in boot)
ok('TRANSIENT_SELECTOR_FLAG', '/system_tmp/pizzahen_kstuff_selector_active' in boot and '/system_tmp/pizzahen_kstuff_selector_active' in hook and '/system_tmp/pizzahen_kstuff_selector_active' in prx)
ok('TRANSIENT_REQUEST_CHANNEL', '/system_tmp/pizzahen_kstuff_request.txt' in boot and '/system_tmp/pizzahen_kstuff_request.txt' in hook)
ok('SELECTOR_XML_TITLE', 'PIZZA HEN — Select KStuff Engine' in hook)
ok('SELECTOR_XML_LITE', 'KStuff Lite 1.09 — Modern Mode' in hook)
ok('SELECTOR_XML_DR', 'KStuff DR 1.2 — Compatibility Mode' in hook)
m=re.search(r'R"XML\((<\?xml.*?</system_settings>)\)XML"', hook, re.S)
selector_xml_ok=False
if m:
    try:
        ET.fromstring(m.group(1))
        selector_xml_ok=True
    except ET.ParseError:
        pass
ok('SELECTOR_XML_PARSE', selector_xml_ok)
ok('SELECTOR_INITIAL_FOCUS', 'initial_focus_to="id_kstuff_select_lite"' in hook)
ok('SELECTOR_BUTTON_LITE', 'id_kstuff_select_lite' in hook)
ok('SELECTOR_BUTTON_DR', 'id_kstuff_select_dr' in hook)
ok('SELECTOR_ATOMIC_REQUEST', 'rename(tmp, dst) == 0' in hook)
ok('SELECTOR_CLOSES_TO_HOME', 'GoToHome();' in hook)
ok('SELECTOR_REMOVES_FLAG', 'unlink("/system_tmp/pizzahen_kstuff_selector_active")' in hook)
ok('ONE_ENGINE_GUARD', 'KStuff already active; refusing second engine' in boot)
ok('LITE_ENGINE_SELECTION', 'chosen_name = "kstuff-lite-1.09"' in boot)
ok('DR_ENGINE_SELECTION', 'chosen_name = "kstuff-dr-1.2"' in boot)
ok('W4_AFTER_UI', boot.index('opening graphical KStuff selector') < boot.index('selected %s'))
ok('SHADOW_AFTER_SELECTED_ENGINE', boot.index('selected %s') < boot.index('starting pristine ShadowMountPlus'))
ok('SHELLUI_REUSE', '/system_tmp/pizzahen_shellui_preloaded' in msg and 'already resident from KStuff selector' in msg)
ok('FIX23_TARGET', 'PIZZA-HEN-v0.1-FIX45-PLUGIN-MANAGER-LIFECYCLE.elf' in cm)
ok('FIX23_BUILD_TEST', 'test_fix23_shellui_selector.py' in build)
ok('SHADOW_PRISTINE_MODE', 'SHADOWMOUNT_MODE=PRISTINE_UPSTREAM_PREBUILT' in build)
failed=[n for n,v in checks if not v]
for n,v in checks: print(f'{n}={"PASS" if v else "FAIL"}')
print(f'FIX23_STATIC={sum(v for _,v in checks)}/{len(checks)} PASS' if not failed else f'FIX23_STATIC_FAIL={failed}')
sys.exit(1 if failed else 0)
