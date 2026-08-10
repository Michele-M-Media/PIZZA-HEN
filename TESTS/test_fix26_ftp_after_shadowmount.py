from pathlib import Path
import hashlib, zipfile
root=Path(__file__).resolve().parents[1]
main=(root/'Source Code/bootstrapper/source/main.cpp').read_text()
daemon=(root/'Source Code/bootstrapper/source/daemon.c').read_text()
cm=(root/'Source Code/unpacker/CMakeLists.txt').read_text()
build=(root/'build_pizzahen_multisdk.sh').read_text()
ftpdir=root/'ThirdParty/ftpsrv-0.21-UPSTREAM-FROZEN'
elf=ftpdir/'ftpsrv-ps5.elf'
src=ftpdir/'ftpsrv-0.21.zip'
checks=[]
def ok(name, cond):
    checks.append((name,bool(cond))); print(f"{name}={'PASS' if cond else 'FAIL'}")
ok('FTP_ELF_PRESENT', elf.exists() and elf.read_bytes()[:4] == b'\x7fELF')
ok('FTP_ELF_FROZEN_SHA', hashlib.sha256(elf.read_bytes()).hexdigest() == 'c580f0534ac6349dc5a4a5c656eaced537b4c2b18da51886d943cea6393436c8')
ok('FTP_SOURCE_FROZEN_SHA', hashlib.sha256(src.read_bytes()).hexdigest() == 'b8e95cccf97ee46be320fede8662404de4f27a5f8f99770d151ddd3fbfc124f8')
with zipfile.ZipFile(src) as z:
    mp=z.read('ftpsrv-0.21/main-prospero.c').decode(errors='replace')
ok('FTP_UPSTREAM_DEFAULT_PORT', 'uint16_t port = 2121;' in mp)
ok('FTP_EXTERN', 'extern uint8_t ftpsrv_start[];' in main and 'extern const unsigned int ftpsrv_size;' in main)
ok('FTP_EMBEDDED', 'ftpsrv_start:' in daemon and 'ftpsrv-ps5.elf' in daemon)
ok('FTP_READY_GATE', 'wait_for_local_ftpsrv(12000)' in main and 'htons(2121)' in main)
ok('FTP_SPAWN', 'elfldr_spawn("/", STDOUT_FILENO, ftpsrv_start, "ftpsrv.elf")' in main)
ok('FTP_AFTER_SHADOW', main.index('PIZZA HEN S6:') < main.index('PIZZA HEN F0:'))
ok('FTP_BEFORE_PAYLOAD2', main.index('PIZZA HEN F0:') < main.index('PIZZA HEN D0:'))
ok('SELECTOR_STILL_BROWSER', 'sceSystemServiceLaunchWebBrowser(selector_url)' in main)
ok('KSTUFF_REQUEST_PATH_PRESERVED', '/data/PIZZA_HEN/runtime/kstuff_request.txt' in main)
ok('SHADOW_PRISTINE_EMBED_PRESERVED', 'shadowmountplus.elf' in daemon)
ok('FIX26_TARGET', 'PIZZA-HEN-v0.1-FIX45-PLUGIN-MANAGER-LIFECYCLE.elf' in cm)
ok('FIX26_TEST_IN_BUILD', 'test_fix26_ftp_after_shadowmount.py' in build)
failed=[n for n,v in checks if not v]
if failed: raise SystemExit('FIX26_STATIC_FAIL='+','.join(failed))
print(f'FIX26_STATIC={len(checks)}/{len(checks)} PASS')
