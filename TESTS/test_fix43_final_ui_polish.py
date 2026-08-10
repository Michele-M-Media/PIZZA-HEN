from pathlib import Path
root=Path(__file__).resolve().parents[1]
def rd(rel): return (root/rel).read_text(errors='ignore')
xml=rd('Source Code/shellui/assets/etaHEN_toolbox.xml')
mono=rd('Source Code/shellui/src/MonoUtils.cpp')
hdr=rd('Source Code/shellui/include/HookedFuncs.hpp')
html=rd('Source Code/bootstrapper/assets/toolbox_launcher.html')
cm=rd('Source Code/unpacker/CMakeLists.txt')
build=rd('build_pizzahen_multisdk.sh')
checks=[]
def ok(n,c):
 print(f'{n}={"PASS" if c else "FAIL"}'); checks.append((n,bool(c)))
ok('FIX43_TARGET','PIZZA-HEN-v0.1-FIX45-PLUGIN-MANAGER-LIFECYCLE.elf' in cm)
ok('FIX43_GPU_DEFAULT_OFF','Settings.overlay_gpu", "0"' in mono and 'bool overlay_gpu = false;' in hdr)
ok('FIX43_CPU_DEFAULT_OFF','Settings.overlay_cpu", "0"' in mono and 'bool overlay_cpu = false;' in hdr)
ok('FIX43_RAM_DEFAULT_OFF','Settings.overlay_ram", "0"' in mono and 'bool overlay_ram = false;' in hdr)
ok('FIX43_OVERLAY_UI_STILL_USER_CONTROLLABLE',all(x in xml for x in ['id_overlay_gpu','id_overlay_cpu','id_overlay_ram']))
ok('FIX43_LEGACY_OVERLAY_MIGRATION','overlay_defaults_opt_in_v1' in mono and 'SaveSettings();' in mono)
ok('FIX43_OLD_PS5DEBUG_TOGGLE_REMOVED','id_sistro_ps5debug' not in xml and 'Enable PS5Debug by Sistr0 and CTN' not in xml)
ok('FIX43_AUTOMATIC_PS5DEBUG_NG_STATUS','ps5debug-NG v1.3.0' in xml and 'TCP 744 (automatic)' in xml)
ok('FIX43_TOOLBOX_COPY_CLEAN','ShellUI is never killed' not in html and 'failed injection' not in html and 'Welcome to the PIZZA HEN kitchen' in html)
ok('FIX43_TOOLBOX_STATUS_COPY','Preparing the PIZZA HEN kitchen' in html and 'Everything is ready. Opening PIZZA HEN Toolbox' in html)
ok('FIX43_SELECTOR_PRESERVED','KStuff Lite 1.09' in rd('Source Code/bootstrapper/assets/kstuff_selector.html') and 'KStuff DR 1.2' in rd('Source Code/bootstrapper/assets/kstuff_selector.html'))
ok('FIX43_MULTI_SDK',all(x in build for x in ['PIZZA_HEN_SDK','PS5_PAYLOAD_SDK','PS5SDK','PAYLOAD_SDK','PIZZA_HEN_TOOLCHAIN_FILE']))
failed=[n for n,c in checks if not c]
if failed: raise SystemExit('FIX43_STATIC_FAIL='+','.join(failed))
print(f'FIX43_STATIC={len(checks)}/{len(checks)} PASS')
