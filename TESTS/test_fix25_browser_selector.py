from pathlib import Path
root=Path(__file__).resolve().parents[1]
main=(root/'Source Code/bootstrapper/source/main.cpp').read_text()
html=(root/'Source Code/bootstrapper/assets/kstuff_selector.html').read_text()
cm=(root/'Source Code/unpacker/CMakeLists.txt').read_text()
build=(root/'build_pizzahen_multisdk.sh').read_text()
checks=[]
def ok(name, cond):
    checks.append((name,bool(cond))); print(f"{name}={'PASS' if cond else 'FAIL'}")
ok('BROWSER_API_DECLARED', 'sceSystemServiceLaunchWebBrowser' in main)
ok('BROWSER_SELECTOR_PRIMARY', 'start_browser_kstuff_selector();' in main)
ok('LOCAL_WEBSRV_SPAWN', 'elfldr_spawn("/", STDOUT_FILENO, websrv_start, "websrv.elf")' in main)
ok('LOCAL_WEBSRV_READY_GATE', 'wait_for_local_websrv(12000)' in main)
ok('DIRECT_SELECTOR_URL', 'http://127.0.0.1:8080/fs/data/PIZZA_HEN/ui/kstuff-selector.html' in main)
ok('NO_FAKE_APP_IN_PRIMARY', 'sceLncUtilLaunchApp("FAKE00000"' not in main)
ok('REQUEST_PATH_MATCH', 'open("/data/PIZZA_HEN/runtime/kstuff_request.txt", O_RDONLY)' in main)
ok('SELECTOR_ACTION_ROUTE', '/hbldr?' in html and 'args:choice' in html)
ok('TWO_VISIBLE_CHOICES', 'KStuff Lite 1.09' in html and 'KStuff DR 1.2' in html)
ok('ONE_ENGINE_WORDING', 'one engine per session' in html)
ok('FIX25_TARGET', 'PIZZA-HEN-v0.1-FIX45-PLUGIN-MANAGER-LIFECYCLE.elf' in cm)
ok('FIX25_TEST_IN_BUILD', 'test_fix25_browser_selector.py' in build)
failed=[n for n,v in checks if not v]
if failed: raise SystemExit('FIX25_STATIC_FAIL='+','.join(failed))
print(f'FIX25_STATIC={len(checks)}/{len(checks)} PASS')
