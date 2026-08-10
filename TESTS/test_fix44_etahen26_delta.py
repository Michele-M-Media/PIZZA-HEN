from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def rd(rel): return (ROOT/rel).read_text(errors='ignore')
checks=[]
def ok(name, cond):
    checks.append((name,bool(cond)))
    print(f"{name}={'PASS' if cond else 'FAIL'}")

app=rd('Source Code/daemon/source/app_plugins.cpp')
main=rd('Source Code/daemon/source/main.cpp')
mono=rd('Source Code/shellui/src/MonoUtils.cpp')
hook=rd('Source Code/shellui/src/HookFunctions.cpp')
hdr=rd('Source Code/shellui/include/HookedFuncs.hpp')
xml=rd('Source Code/shellui/assets/etaHEN_toolbox.xml')
build=rd('build_pizzahen_multisdk.sh')
cm=rd('Source Code/unpacker/CMakeLists.txt')
selector=rd('Source Code/bootstrapper/assets/kstuff_selector.html')
ref=rd('FIX44_ETAHEN26_DELTA_UPDATE.txt')

ok('FIX44_TARGET','PIZZA-HEN-v0.1-FIX45-PLUGIN-MANAGER-LIFECYCLE.elf' in cm)
ok('FIX44_REFERENCE_HASH','512c74a9d6f56bb5a4ab871a0306a8cbefb8b3d5454ba8f1d833b020b245a126' in ref)
ok('FIX44_NO_WHOLESALE_26_REPLACEMENT','does NOT replace' in ref and 'etaHEN-2.6B.bin' not in cm)
ok('FIX44_APP_PLUGIN_CONFIG','/data/PIZZA_HEN/plugins/apps/plugins.ini' in app)
ok('FIX44_DEFAULT_SECTION','[DEFAULT]' in app and 'section == "DEFAULT"' in app)
ok('FIX44_TITLE_SECTIONS','[CUSA00001]' in app and '[PPSA00001]' in app)
ok('FIX44_AUTOLOAD_SUFFIX','?autoload' in app and '?autoload' in mono)
ok('FIX44_ARBITRARY_PATH_EXAMPLE','/mnt/usb0/plugin.sprx' in app)
ok('FIX44_PID_TID_MONITOR','PID change detected' in app and 'sceSystemServiceGetAppTitleId' in app and 'get_game_pid()' in app)
ok('FIX44_SESSION_DEDUP','loaded_paths' in app and 'std::find' in app)
ok('FIX44_LITE_MODE_GUARD','if (!is_lite)' in main and 'app_plugin_monitor_thread' in main)
ok('FIX44_EXISTING_INJECTOR_REUSED','Inject_Toolbox(pid, elf.data())' in app)
ok('FIX44_APP_PLUGIN_MENU','id_app_plugins' in mono and 'app_plugins.xml' in hook and 'generate_app_plugins_xml' in hook)
ok('FIX44_PERSISTENT_TOGGLE','set_app_plugin_autoload' in mono and 'rename(temp_path.c_str(), config_path)' in mono)
ok('FIX44_NO_FAKE_HOT_UNLOAD','plugin_stop' not in app and 'does NOT invent a fake plugin_stop' in ref)
ok('FIX44_FPS_PS4_PS5','FPS Section (PS4 / PS5)' in xml and 'value="0"' in xml)
ok('FIX44_NO_DUPLICATE_FPS_ENGINE','fps_counter loaded!' not in app and 'fps_elf' not in app)
ok('FIX44_KSTUFF_SELECTOR','KStuff Lite 1.09' in selector and 'KStuff DR 1.2' in selector)
ok('FIX44_MULTI_SDK',all(x in build for x in ['PIZZA_HEN_SDK','PS5_PAYLOAD_SDK','PS5SDK','PAYLOAD_SDK','PIZZA_HEN_TOOLCHAIN_FILE']))
ok('FIX44_DIRECT_ITEMZFLOW','launch_pizzahen_backend("ITEM00001", "Game Manager")' in hook)
ok('FIX44_MEDIA_TILE','PZHN00001' in rd('Source Code/bootstrapper/assets/toolbox_shortcut_param.json'))

failed=[n for n,v in checks if not v]
if failed: raise SystemExit('FIX44_STATIC_FAIL='+','.join(failed))
print(f'FIX44_STATIC={len(checks)}/{len(checks)} PASS')
