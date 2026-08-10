#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
xml=(ROOT/'Source Code/shellui/assets/etaHEN_toolbox.xml').read_text(errors='ignore')
lite=(ROOT/'Source Code/shellui/assets/etaHEN_Lite.xml').read_text(errors='ignore')
hook=(ROOT/'Source Code/shellui/src/HookFunctions.cpp').read_text(errors='ignore')
games=(ROOT/'Source Code/util/source/gameslist.cpp').read_text(errors='ignore')
build=(ROOT/'build_pizzahen_multisdk.sh').read_text(errors='ignore')
cm=(ROOT/'Source Code/unpacker/CMakeLists.txt').read_text(errors='ignore')
checks=[]
def ok(name, cond):
    if not cond: raise SystemExit(f'{name}=FAIL')
    print(f'{name}=PASS'); checks.append(name)
ok('FIX41_TARGET','PIZZA-HEN-v0.1-FIX45-PLUGIN-MANAGER-LIFECYCLE.elf' in cm)
ok('FIX41_GAMEHUB_REMOVED','PIZZA HEN Game Hub' not in xml and 'PIZZA HEN Game Hub' not in hook)
ok('FIX41_FOLDER_IMAGE_LIBRARY_REMOVED','Folder &amp; Image Library' not in xml and 'PIZZA HEN Folder &amp; Image Library' not in xml)
ok('FIX41_WEBMAN_RESTORED','(Beta) PS5 webMAN Games' in xml)
ok('FIX41_GAME_MANAGER_DIRECT','id_open_game_manager' in xml and 'Open Game Manager' in xml)
ok('FIX41_NEW_INTEGRATION_LABEL','PIZZA HEN Game Manager integration by Michele Media' in xml)
ok('FIX41_ITEMZFLOW_DIRECT_ROUTE','launch_pizzahen_backend("ITEM00001", "Game Manager")' in hook)
ok('FIX41_WORKING_SYSTEMSERVICE','sceSystemServiceLaunchApp(title_id, argv, &ctx)' in hook)
ok('FIX41_NO_CIBORG_UI','PKGI12345' not in xml and 'id_ph_image_manager' not in hook)
ok('FIX41_NO_IMAGE_SCANNER','.ffpkg' not in games and '.ffpfsc' not in games and '.exfat' not in games)
ok('FIX41_START_OPTION_SIMPLE','Game Manager (if installed)' in xml and 'Game Manager (if installed)' in lite)
ok('FIX41_THEME_PRESERVED','apply_pizzahen_itemzflow_theme' in hook and '/data/PIZZA_HEN/themes/itemzflow/background.png' in hook)
ok('FIX41_KSTUFF_SELECTOR_PRESERVED','id_kstuff_select_lite' in hook and 'id_kstuff_select_dr' in hook)
ok('FIX41_MULTI_SDK',all(x in build for x in ['PIZZA_HEN_SDK','PS5_PAYLOAD_SDK','PS5SDK','PAYLOAD_SDK','PIZZA_HEN_TOOLCHAIN_FILE']))
ok('FIX41_MEDIA_TILE_PRESERVED','PZHN00001' in (ROOT/'Source Code/bootstrapper/assets/toolbox_shortcut_param.json').read_text(errors='ignore'))
print(f'FIX41_STATIC={len(checks)}/{len(checks)} PASS')
