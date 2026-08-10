from pathlib import Path
import hashlib, zipfile
root=Path(__file__).resolve().parents[1]
main=(root/'Source Code/bootstrapper/source/main.cpp').read_text()
daemon=(root/'Source Code/bootstrapper/source/daemon.c').read_text()
cm=(root/'Source Code/unpacker/CMakeLists.txt').read_text()
build=(root/'build_pizzahen_multisdk.sh').read_text()
dbgdir=root/'ThirdParty/ps5debug-NG-1.3.0-UPSTREAM-FROZEN'
elf=dbgdir/'ps5debug-NG_v1.3.0.elf'
src=dbgdir/'ps5debug-NG-1.3.0.zip'
checks=[]
def ok(name, cond):
    checks.append((name,bool(cond))); print(f"{name}={'PASS' if cond else 'FAIL'}")
ok('PS5DEBUG_ELF_PRESENT', elf.exists() and elf.read_bytes()[:4] == b'\x7fELF')
ok('PS5DEBUG_ELF_FROZEN_SHA', hashlib.sha256(elf.read_bytes()).hexdigest() == '8f75fb90b45d7cc4d59147e3323577d7264cf572c78a27f76722202f492ad16a')
ok('PS5DEBUG_SOURCE_FROZEN_SHA', hashlib.sha256(src.read_bytes()).hexdigest() == 'd2a115d907eb876a12d1335068eb874e7a8bb5b3d149db048b8acbe905a38701')
with zipfile.ZipFile(src) as z:
    installer=z.read('ps5debug-NG-1.3.0/installer/source/main.c').decode(errors='replace')
    readme=z.read('ps5debug-NG-1.3.0/README.md').decode(errors='replace')
ok('PS5DEBUG_UPSTREAM_PORT_744', '#define PS5DEBUG_PORT      744' in installer)
ok('PS5DEBUG_FW1001_SOURCE_PRESENT', '10.00 10.01 10.20 10.40 10.60' in installer or '10.01' in readme)
ok('PS5DEBUG_EXTERN', 'extern uint8_t ps5debug_ng_start[];' in main and 'extern const unsigned int ps5debug_ng_size;' in main)
ok('PS5DEBUG_EMBEDDED', 'ps5debug_ng_start:' in daemon and 'ps5debug-NG_v1.3.0.elf' in daemon)
ok('PS5DEBUG_READY_GATE', 'wait_for_local_ps5debug_ng(20000)' in main and 'htons(744)' in main)
ok('PS5DEBUG_AUTO_SPAWN', 'elfldr_spawn("/", STDOUT_FILENO, ps5debug_ng_start' in main)
ok('PS5DEBUG_AFTER_FTP', main.index('PIZZA HEN F6:') < main.index('PIZZA HEN D0:'))
ok('PS5DEBUG_NO_EXTRA_MENU', 'starting ps5debug-NG v1.3.0 automatically' in main)
ok('FTP_GATE_PRESERVED', 'wait_for_local_ftpsrv(12000)' in main and 'PIZZA HEN F3:' in main)
ok('SELECTOR_STILL_BROWSER', 'sceSystemServiceLaunchWebBrowser(selector_url)' in main)
ok('KSTUFF_REQUEST_PATH_PRESERVED', '/data/PIZZA_HEN/runtime/kstuff_request.txt' in main)
ok('SHADOW_PRISTINE_EMBED_PRESERVED', 'shadowmountplus.elf' in daemon)
ok('FIX27_TARGET', 'PIZZA-HEN-v0.1-FIX45-PLUGIN-MANAGER-LIFECYCLE.elf' in cm)
ok('FIX27_TEST_IN_BUILD', 'test_fix27_ps5debug_ng_auto.py' in build)
failed=[n for n,v in checks if not v]
if failed: raise SystemExit('FIX27_STATIC_FAIL='+','.join(failed))
print(f'FIX27_STATIC={len(checks)}/{len(checks)} PASS')
