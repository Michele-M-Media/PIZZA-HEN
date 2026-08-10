from pathlib import Path
import hashlib, zipfile, sys, re
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
checks=[]
def ok(name, cond): checks.append((name, bool(cond)))
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()

webdir=ROOT/'ThirdParty/websrv-0.34-UPSTREAM-FROZEN'
web=webdir/'websrv-ps5.elf'
webzip=webdir/'websrv-0.34.zip'
drdir=ROOT/'ThirdParty/kstuff-dr-1.2-test1-UPSTREAM-FROZEN'
dr=drdir/'kstuff-dr-1.2-test1.elf'
drzip=drdir/'kstuff-lite-1.2-dr-test1.zip'
smdir=ROOT/'ThirdParty/ShadowMountPlus-1.6beta16-UPSTREAM-FROZEN'
sm=smdir/'shadowmountplus.elf'
smzip=smdir/'ShadowMountPlus-1.6beta16.zip'
js=(SRC/'bootstrapper/assets/kstuff_selector.js').read_text(encoding='utf-8')
html=(SRC/'bootstrapper/assets/kstuff_selector.html').read_text(encoding='utf-8')
main=(SRC/'bootstrapper/source/main.cpp').read_text(encoding='utf-8')
dc=(SRC/'bootstrapper/source/daemon.c').read_text(encoding='utf-8')
sel=(SRC/'selector_action/src/main.c').read_text(encoding='utf-8')
cm=(SRC/'unpacker/CMakeLists.txt').read_text(encoding='utf-8')
bs=(ROOT/'build_pizzahen_multisdk.sh').read_text(encoding='utf-8')

ok('WEBSRV_ELF_MAGIC', web.read_bytes()[:4] == b'\x7fELF')
ok('WEBSRV_ELF_SHA256', sha(web)=='54730c867c6e1148536fdcb370e63a7762d989ea87b62488ad4caff64d43f263')
ok('WEBSRV_SOURCE_SHA256', sha(webzip)=='cf89f500848d68a266655c5cea63831a32f5e489ddb93d898bb0b8699da8d5d0')
ok('DR_ELF_MAGIC', dr.read_bytes()[:4] == b'\x7fELF')
ok('DR_ELF_SHA256', sha(dr)=='9c1b242eaed3704ef18be45d001a2c4ebf2d9222cfe3cbb0f0c3db33309abac9')
ok('DR_SOURCE_SHA256', sha(drzip)=='56f2a64fec342d6f5f8c9d29bbbbebae53dd1dea6836f1879347d5a4a16924ac')
ok('SHADOW_ELF_MAGIC', sm.read_bytes()[:4] == b'\x7fELF')
ok('SHADOW_ELF_SHA256', sha(sm)=='a35246fb3bb6042b25653b51cdcbc33254b40339342bf1d2dd0d2eceee2ca526')
ok('SHADOW_SOURCE_SHA256', sha(smzip)=='5af04b9481545a869660aa1942d3396d890757660f29a702a2244823fa28ec23')

with zipfile.ZipFile(webzip) as z:
    names=set(z.namelist())
    ok('WEBSRV_HOMEBREW_API_SOURCE', any(n.endswith('/assets/homebrewApi.js') for n in names))
    ok('WEBSRV_DEMO_EXTENSION_SOURCE', any(n.endswith('/homebrew/demo/homebrew.js') for n in names))
with zipfile.ZipFile(smzip) as z:
    names=set(z.namelist())
    ok('SHADOW_UPSTREAM_FAKELIB_SOURCE', 'ShadowMountPlus-1.6beta16/src/sm_fakelib.c' in names)

ok('SELECTOR_LITE', 'KStuff Lite 1.09' in js and 'EchoStretch - Modern Mode' in js)
ok('SELECTOR_DR', 'KStuff DR 1.2' in js and 'Drakmor - Compatibility Mode' in js)
ok('SELECTOR_NO_AUTO', 'AUTO' not in js.upper())
ok('SELECTOR_DAEMON_ACTION_LITE', 'args: ["lite"], daemon: true' in js)
ok('SELECTOR_DAEMON_ACTION_DR', 'args: ["dr"], daemon: true' in js)
ok('SELECTOR_FOREGROUND_ATTEMPT', 'setTimeout(() => showCarousel(items)' in js)
ok('SELECTOR_FALLBACK_TILE', 'KStuff Engine Selector' in js)
ok('DIRECT_HTML_SELECTOR_TWO_CHOICES', 'KStuff Lite 1.09' in html and 'KStuff DR 1.2' in html)
ok('DIRECT_HTML_HBLDR_DAEMON', "daemon:'1'" in html and "path:'/data/PIZZA_HEN/bin/pizzahen-kstuff-select.elf'" in html)
ok('DIRECT_HTML_ACTIVE_STATUS', 'kstuff_active.txt' in html and 'Active engine:' in html)
ok('DIRECT_HTML_NO_LIVE_SWITCH_CLAIM', 'Live switching is not enabled' in html)
ok('REQUEST_ATOMIC_TMP_RENAME', 'kstuff_request.tmp' in sel and 'rename(REQUEST_TMP, REQUEST_FILE)' in sel)
ok('REQUEST_ONLY_TWO_VALUES', '"lite"' in sel and '"dr"' in sel and 'auto' not in sel.lower())

ok('WEBSRV_EMBEDDED', 'websrv_start' in dc and 'websrv-ps5.elf' in dc)
ok('DR_EMBEDDED', 'kstuff_dr_start' in dc and 'kstuff-dr-1.2-test1.elf' in dc)
ok('SELECTOR_ACTION_EMBEDDED', 'selector_action_start' in dc and 'pizzahen-kstuff-select.elf' in dc)
ok('SELECTOR_HTML_EMBEDDED', 'selector_html_start' in dc and 'kstuff_selector.html' in dc)
ok('SHADOW_EMBEDDED_PRISTINE', 'shadowmount_start' in dc and 'shadowmountplus.elf' in dc)
ok('SINGLE_KSTUFF_OWNER', 'single' in main.lower() and 'engine launch' in main.lower())
ok('SAFE_EXISTING_GUARD', 'KStuff already active; refusing second engine' in main)
ok('REQUEST_LITE', '!strcmp(out, "lite")' in main and 'chosen_name = "kstuff-lite-1.09"' in main)
ok('REQUEST_DR', '!strcmp(choice, "dr")' in main)
ok('SHADOW_AFTER_KSTUFF', main.index('selected %s') < main.index('starting pristine ShadowMountPlus'))
ok('FIX23_FINAL_TARGET', 'PIZZA-HEN-v0.1-FIX45-PLUGIN-MANAGER-LIFECYCLE.elf' in cm)
ok('BUILD_TEST_FIX21', 'test_fix21_websrv_selector.py' in bs)
ok('NO_OBSOLETE_PROSPERO_MK_HARD_GATE', 'FULL_FIX13_REQUIRES_PROSPERO_MK' not in bs)
ok('LEGACY_V042_CMAKE_LAYOUT', 'cmake/toolchain-ps5.cmake' in bs)
ok('SHADOW_PREBUILT_MODE', 'SHADOWMOUNT_MODE=PRISTINE_UPSTREAM_PREBUILT' in bs)
ok('KSTUFF_LITE_FIX11_BASELINE', 'KSTUFF_BASELINE=FIX11_HARDWARE_PASS' in bs)
ok('NO_PATCHED_SHADOW_TREE', not (ROOT/'ThirdParty/ShadowMountPlus-1.6beta16-PIZZA-HEN').exists())

failed=[n for n,v in checks if not v]
for n,v in checks: print(f'{n}={"PASS" if v else "FAIL"}')
print(f'FIX21_STATIC={sum(v for _,v in checks)}/{len(checks)} PASS' if not failed else f'FIX21_STATIC_FAIL={failed}')
sys.exit(1 if failed else 0)
