from pathlib import Path
import hashlib, sys, struct, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
checks=[]
def check(name, cond, detail=''): checks.append((name,bool(cond),detail))
def text(p): return p.read_text(encoding='utf-8')
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()

identity=text(SRC/'include/pizzahen/identity.h')
boot=text(SRC/'bootstrapper/source/main.cpp')
daemon=text(SRC/'daemon/source/main.cpp')
hooks=text(SRC/'shellui/src/HookFunctions.cpp')
bootstrap_cmake=text(SRC/'bootstrapper/CMakeLists.txt')
root_cmake=text(SRC/'CMakeLists.txt')
unpacker_cmake=text(SRC/'unpacker/CMakeLists.txt')
build=text(ROOT/'build_pizzahen_multisdk.sh')
dc=text(SRC/'bootstrapper/source/daemon.c')
seljs=text(SRC/'bootstrapper/assets/kstuff_selector.js')
selhtml=text(SRC/'bootstrapper/assets/kstuff_selector.html')
selc=text(SRC/'selector_action/src/main.c')

for p in (SRC/'shellui/assets/etaHEN_toolbox.xml', SRC/'shellui/assets/etaHEN_Lite.xml'):
    ET.parse(p)
check('XML_PARSE', True)
key=b'U0lTVFIwX0lfU0VFX1lPVQ=='
for stem in ('etaHEN_toolbox','etaHEN_Lite'):
    plain=(SRC/f'shellui/assets/{stem}.xml').read_bytes(); crypt=(SRC/f'shellui/assets/{stem}.sxml').read_bytes()
    decoded=bytes(b ^ key[i % len(key)] for i,b in enumerate(crypt))
    check(f'SXML_MATCH_{stem}', decoded==plain)

png=(SRC/'bootstrapper/assets/pizzahen_sicon.png').read_bytes(); wh=struct.unpack('>II',png[16:24])
check('ICON_64X64', wh==(64,64), str(wh))
check('IDENTITY_LAYER', 'PIZZA_HEN_VERSION' in identity)
check('DASHBOARD_NOTIFICATION', 'PIZZA HEN v0.1 | Michele Media' in daemon)
check('DASHBOARD_ICON_PATH', '/user/data/PIZZA_HEN/pizzahen.png' in daemon)
check('GAME_MANAGER_BUTTON_PRESENT', 'id == "id_open_game_manager"' in hooks)
check('GPL_LICENSE', (ROOT/'LICENSE').exists())

msg=text(SRC/'include/msg.hpp'); embedded=text(SRC/'daemon/source/embeddded_payloads.c'); daemon_cmake=text(SRC/'daemon/CMakeLists.txt')
check('IPC_MAIN_COMMANDS', all(x in msg for x in ('BREW_LAUNCH_DUMPER = 0x9000013','BREW_ADJUST_FAN_SPEED = 0x9000014')))
check('IPC_UTIL_COMMANDS', all(x in msg for x in ('BREW_UTIL_GET_GAMES_LIST = 0x8000010','BREW_UTIL_LAUNCH_GAME_BY_BUTTON_ID = 0x8000011')))
check('PS5DEBUG_ASSET', (SRC/'daemon/assets/ps5debug.elf').read_bytes()[:4]==b'\x7fELF')
check('DAEMON_FPS_DEPENDENCY', 'shellui fps_elf' in daemon_cmake)
check('SHELLUI_SIZE_SYMBOL', '"shellui_elf_size:\\n"' in embedded and '"shellui_prx_size:\\n"' not in embedded)
check('DUMPER_SAFE_DISABLED', 'dumper_elf_size = 0' in embedded)
check('FW1001_BYPERVISOR_STUB', (SRC/'bootstrapper/source/byepervisor_fw1001_stub.cpp').exists() and 'Byepervisor/src' not in bootstrap_cmake)
check('OUT_OF_SOURCE_INCBIN_FIX', '../../../bin/bootstrapper.elf.lzma' in text(SRC/'unpacker/source/main.c'))
check('UTIL_WOLFSSL_BACKEND', 'wolfssl' in text(SRC/'util/CMakeLists.txt'))
check('BOOTSTRAPPER_SQLITE_BACKEND', ' elfldr sqlite SceNotification' in bootstrap_cmake and (SRC/'lib/libsqlite.a').exists())
check('BOOTSTRAPPER_NO_DIRECT_PAD_BACKEND', 'ScePad' not in bootstrap_cmake and '../daemon/include' in bootstrap_cmake)
check('PORTABLE_LZMA_PACKER', (SRC/'tools/pizzahen_pack_lzma.py').exists() and 'FORMAT_ALONE' in text(SRC/'tools/pizzahen_pack_lzma.py'))

libelf=text(SRC/'libelfldr/src/elfldr.c')
check('CURRENT_ELFLDR_RFORK', 'rfork_thread' in libelf and 'RFPROC | RFCFDG | RFMEM' in libelf)
check('CURRENT_ELFLDR_EXEC_EVENT', 'EVFILT_PROC' in libelf and 'NOTE_EXEC' in libelf and 'kevent' in libelf)
check('CURRENT_ELFLDR_AUTHID_RESTORE', 'kernel_get_ucred_authid' in libelf and 'kernel_set_ucred_authid' in libelf)
check('CURRENT_ELFLDR_PAYLOAD_ARGS', 'elfldr_payload_args' in libelf)
check('BOOTSTRAPPER_LEGACY_ELFLDR_EXCLUDED', 'source/elfldr' in bootstrap_cmake and 'source/pt' in bootstrap_cmake)
check('DEBUG_PROFILE', 'CMAKE_BUILD_TYPE=Debug' in build)
check('MULTI_SDK_NO_V042_PIN', 'PAYLOAD_SDK_V042' not in build and all(x in build for x in ('PIZZA_HEN_SDK','PS5_PAYLOAD_SDK','PS5SDK','PAYLOAD_SDK')))
check('CURRENT_SDK_CMAKE', 'toolchain/prospero.cmake' in build)
check('LEGACY_SDK_CMAKE_WRAPPER', 'bin/prospero-cmake' in build)
check('LEGACY_V042_CMAKE_LAYOUT', 'cmake/toolchain-ps5.cmake' in build)
check('NO_PROSPERO_MK_HARD_REQUIRE', 'FULL_FIX13_REQUIRES_PROSPERO_MK' not in build)

check('FIX23_FINAL_TARGET', 'PIZZA-HEN-v0.1-FIX45-PLUGIN-MANAGER-LIFECYCLE.elf' in unpacker_cmake)
check('SELECTOR_SUBPROJECT', 'add_subdirectory(selector_action)' in root_cmake and 'add_dependencies(${PROJECT_NAME} daemon util shellui selector_action toolbox_action)' in bootstrap_cmake)
check('SELECTOR_ACTION_ATOMIC', 'kstuff_request.tmp' in selc and 'rename(REQUEST_TMP, REQUEST_FILE)' in selc)
check('SELECTOR_TWO_CHOICES', 'KStuff Lite 1.09' in seljs and 'KStuff DR 1.2' in seljs and 'AUTO' not in seljs.upper())
check('SELECTOR_ACTION_DAEMON_MODE', seljs.count('daemon: true')==2)
check('SELECTOR_FOREGROUND_ATTEMPT', 'showCarousel(items)' in seljs and 'setTimeout' in seljs)
check('DIRECT_SELECTOR_HTML', 'KStuff Lite 1.09' in selhtml and 'KStuff DR 1.2' in selhtml and '/hbldr?' in selhtml)
check('DIRECT_SELECTOR_DAEMON_REQUEST', "daemon:'1'" in selhtml and "path:'/data/PIZZA_HEN/bin/pizzahen-kstuff-select.elf'" in selhtml)
check('ACTIVE_STATUS_FILE_UI', 'kstuff_active.txt' in selhtml and 'kstuff_active.txt' in boot)
check('SELECTOR_BROWSER_FIRST', 'start_browser_kstuff_selector' in boot and 'sceSystemServiceLaunchWebBrowser' in boot)
check('SELECTOR_REQUEST_CHANNEL', 'wait_for_web_kstuff_request' in boot and '/data/PIZZA_HEN/runtime/kstuff_request.txt' in boot and 'W3-TIMEOUT' in boot)
check('SINGLE_KSTUFF_PER_BOOT', 'KStuff already active; refusing second engine' in boot and 'selected KStuff spawn failed' in boot)
check('LITE_ENGINE_PRESENT', 'kstuff_start' in dc and 'bootstrapper/assets/kstuff.elf' in dc)
check('DR_ENGINE_PRESENT', 'kstuff_dr_start' in dc and 'kstuff-dr-1.2-test1.elf' in dc)
check('WEBSRV_PRESENT', 'websrv_start' in dc and 'websrv-ps5.elf' in dc)
check('DIRECT_SELECTOR_EMBEDDED', 'selector_html_start' in dc and 'kstuff_selector.html' in dc)
check('SHADOWMOUNT_PRESENT', 'shadowmount_start' in dc and 'shadowmountplus.elf' in dc)
check('SHADOW_AFTER_KSTUFF', boot.index('selected %s') < boot.index('starting pristine ShadowMountPlus'))
d6_pos=boot.index('PIZZA HEN D6: full automatic post-ShadowMount payload chain PASS')
util_pos=boot.index('etaHEN Utility Daemon', d6_pos)
check('DAEMON_AFTER_POST_CHAIN', 'return 0;' not in boot[d6_pos:util_pos] and util_pos>d6_pos)

web=ROOT/'ThirdParty/websrv-0.34-UPSTREAM-FROZEN/websrv-ps5.elf'; webzip=ROOT/'ThirdParty/websrv-0.34-UPSTREAM-FROZEN/websrv-0.34.zip'
dr=ROOT/'ThirdParty/kstuff-dr-1.2-test1-UPSTREAM-FROZEN/kstuff-dr-1.2-test1.elf'; drzip=ROOT/'ThirdParty/kstuff-dr-1.2-test1-UPSTREAM-FROZEN/kstuff-lite-1.2-dr-test1.zip'
sm=ROOT/'ThirdParty/ShadowMountPlus-1.6beta16-UPSTREAM-FROZEN/shadowmountplus.elf'; smzip=ROOT/'ThirdParty/ShadowMountPlus-1.6beta16-UPSTREAM-FROZEN/ShadowMountPlus-1.6beta16.zip'
check('WEBSRV_FROZEN_SHA', sha(web)=='54730c867c6e1148536fdcb370e63a7762d989ea87b62488ad4caff64d43f263')
check('WEBSRV_SOURCE_FROZEN_SHA', sha(webzip)=='cf89f500848d68a266655c5cea63831a32f5e489ddb93d898bb0b8699da8d5d0')
check('DR_FROZEN_SHA', sha(dr)=='9c1b242eaed3704ef18be45d001a2c4ebf2d9222cfe3cbb0f0c3db33309abac9')
check('DR_SOURCE_FROZEN_SHA', sha(drzip)=='56f2a64fec342d6f5f8c9d29bbbbebae53dd1dea6836f1879347d5a4a16924ac')
check('SHADOW_FROZEN_SHA', sha(sm)=='a35246fb3bb6042b25653b51cdcbc33254b40339342bf1d2dd0d2eceee2ca526')
check('SHADOW_SOURCE_FROZEN_SHA', sha(smzip)=='5af04b9481545a869660aa1942d3396d890757660f29a702a2244823fa28ec23')
check('NO_PATCHED_SHADOWMOUNT_TREE', not (ROOT/'ThirdParty/ShadowMountPlus-1.6beta16-PIZZA-HEN').exists())
check('SHADOW_PREBUILT_BUILD_MODE', 'SHADOWMOUNT_MODE=PRISTINE_UPSTREAM_PREBUILT' in build and 'BUILD_PORTABLE.sh' not in build)
check('FIX11_LITE_BASELINE', 'KSTUFF_BASELINE=FIX11_HARDWARE_PASS' in build)
check('FIX21_STATIC_IN_BUILD', 'test_fix21_websrv_selector.py' in build)
check('FIX25_STATIC_IN_BUILD', 'test_fix25_browser_selector.py' in build)
check('FIX30_STATIC_IN_BUILD', 'test_fix30_complete_toolbox.py' in build)
check('CORE_STATIC_IN_BUILD', 'test_pizzahen_source.py' in build)

failed=[x for x in checks if not x[1]]
for n,v,d in checks: print(f'{n}={"PASS" if v else "FAIL"}'+(f' ({d})' if d else ''))
print(f'STATIC_TESTS={sum(v for _,v,_ in checks)}/{len(checks)} PASS')
if failed:
    print('FAILED=' + ','.join(n for n,_,_ in failed))
    sys.exit(1)
