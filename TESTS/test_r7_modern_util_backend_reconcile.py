from pathlib import Path
import hashlib,re
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ok(n,c):
    print(('PASS ' if c else 'FAIL ')+n)
    if not c: raise SystemExit(1)

# Source-exact FIX70.37 manager files, frozen by their audited hashes.
refs={
 'util/source/PluginManager.cpp':'3dbf9a92053afce96b4639c2fc635a53c484b82c6b0a1c9c77a959257330bdf0',
 'util/source/PkgManager.cpp':'1a2b4a6bc32862d19c71d2dd27b35c44dc88eff25b3ff62f02629061f0f1bf0c',
 'util/include/plugin_manager.hpp':'ef426e775efa2fddcc85f22e2959887f7598e5da2f97473f087743d23116d2de',
 'util/include/pkg_manager.hpp':'561f211c8a176cc5a3fbf2870a6f5247d8f9f422f55e15645a5e25866ece0fce',
}
for rel,h in refs.items():
    ok('R7_PRESENT_'+rel,(SRC/rel).is_file())
    ok('R7_FIX70_37_EXACT_'+rel,sha(SRC/rel)==h)

hdr=(SRC/'include/msg.hpp').read_text()
ids={'BREW_UTIL_SCAN_USB_PKGS':'0x8000012','BREW_UTIL_DOWNLOAD_STORE':'0x8000013','BREW_UTIL_SCAN_PLUGINS':'0x8000014','BREW_UTIL_STOP_PLUGIN':'0x8000015','BREW_UTIL_SET_PLUGIN_AUTOSTART':'0x8000016'}
for k,v in ids.items(): ok('R7_ABI_'+k,re.search(r'\b'+re.escape(k)+r'\s*=\s*'+re.escape(v),hdr) is not None)

msg=(SRC/'util/source/msg.cpp').read_text()
for k in ids: ok('R7_HANDLER_'+k,('case '+k+':') in msg or ('case '+k+':{') in msg)
ok('R7_MANAGER_INCLUDES','#include <pkg_manager.hpp>' in msg and '#include <plugin_manager.hpp>' in msg)
a=msg.index('  case BREW_UTIL_DOWNLOAD_STORE: {'); b=msg.index('  case BREW_KILL_DAEMON:{',a)
block_hash=hashlib.sha256(msg[a:b].encode()).hexdigest()
ok('R7_FIX70_37_EXACT_UTIL_HANDLER_BLOCK',block_hash=='be50b36285605c1765659ccf93e94da7ad7b22bf5d77655f3a2b0bfcb9627723')

# Frozen bridge boundaries: exact hashes from the hardware-PASS R6 branch.
frozen={
 'toolbox_action/src/main.c':'8155569ab893e23d365b054d8c3075fcdebb6792b75f0ccf21d2bff33f76faf6',
 'toolbox_api/src/main.c':'7b33833755a202b434f2fc4deb263676c05c7c5b9fc621b11cff1f008d2d4711',
 'daemon/source/main.cpp':'a1eba914cc62cf67de75ffbd025d9542c5a76fd27d38e58655b2b48e1846206f',
 'daemon/source/msg.cpp':'beaa02339b3e9fc80e3d3acd068b1137fbf13e6c04a0da6719a855d0cd11fa14',
 'shellui/src/HookFunctions.cpp':'34e0c82ae5a5c530b9a70a835ae9717db56843196e7b42befac585ac9386d247',
 'shellui/src/prx.cpp':'fa0a2e3465a33d17c1cce1fe960b8d9b9e0448a5e55d7ef3f76c2e088f3f7ed7',
 'bootstrapper/assets/debug_services_launcher.html':'7f7134593eefa9628bc581eebe3a7fc66f40cba3bb8f9447ebd641bfe58eb399',
}
for rel,h in frozen.items(): ok('R7_R6_FROZEN_'+rel,sha(SRC/rel)==h)

ok('R7_NO_SHELL_SERVICE_REINVENTION','BREW_PIZZAHEN_SHELL_SERVICE' not in (SRC/'daemon/source/msg.cpp').read_text())
print('R7_MODERN_UTIL_BACKEND_RECONCILE=PASS')
