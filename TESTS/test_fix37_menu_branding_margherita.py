from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'Source Code'
TB = SRC / 'shellui/assets/etaHEN_toolbox.xml'
LITE = SRC / 'shellui/assets/etaHEN_Lite.xml'
HF = SRC / 'shellui/src/HookFunctions.cpp'
MU = SRC / 'shellui/src/MonoUtils.cpp'
PARAM = SRC / 'bootstrapper/assets/toolbox_shortcut_param.json'
CM = SRC / 'unpacker/CMakeLists.txt'

checks = []
def ok(name, cond):
    if not cond:
        raise SystemExit(f'{name}=FAIL')
    checks.append(name)
    print(f'{name}=PASS')

for p in (TB, LITE):
    ET.parse(p)

tb = TB.read_text(encoding='utf-8')
lite = LITE.read_text(encoding='utf-8')
hf = HF.read_text(encoding='utf-8')
mu = MU.read_text(encoding='utf-8')
param = PARAM.read_text(encoding='utf-8')
cm = CM.read_text(encoding='utf-8')

ok('FIX37_NO_DONATION_MENU', 'Support the Project' not in tb and 'Support the Project' not in lite and 'Consider Donating' not in tb and 'Consider Donating' not in lite)
ok('FIX37_NO_UPSTREAM_CREDITS_MENU', 'etaHEN Upstream Credits' not in tb and 'etaHEN Upstream Credits' not in lite)
about = tb[tb.index('id_pizzahen_about'):]
ok('FIX37_NO_LIGHTNINGMODS_ABOUT_UI', 'LightningMods' not in about and 'LightningMods' not in lite)
ok('FIX37_INCLUDED_OPEN_SOURCE_PROJECTS', 'Included Open-source Projects' in tb and 'Included Open-source Projects' in lite)
ok('FIX37_ABOUT_PIZZA_HEN', 'About PIZZA HEN' in tb and 'About PIZZA HEN' in lite)
ok('FIX37_ABOUT_NO_ITEMZFLOW', 'Itemzflow' not in about)
ok('FIX37_ABOUT_NO_LIGHTNINGMODS', 'LightningMods' not in about)
ok('FIX37_MARGHERITA_RECIPE', all(x in tb for x in ['Pizza Margherita Recipe', '500 g farina 00', 'fior di latte', 'basilico', 'olio EVO']))
ok('FIX37_LEGACY_FTP_REBRAND', 'title="Legacy FTP"' in tb and 'Legacy etaHEN FTP' not in tb)
ok('FIX37_DYNAMIC_PIZZA_HEN_BRANDING', all(x in hf for x in ['PIZZA HEN is currently installing the selected PKG', 'PIZZA HEN PKG Sort', 'PIZZA HEN Toolbox', '★ PIZZA HEN Cheats']))
ok('FIX37_DYNAMIC_CHEATS_REBRAND', 'PIZZA HEN Cheats - No ' in mu and 'PIZZA HEN Payload Homebrew - Applications' in mu)
ok('FIX37_REMOTE_PLAY_REBRAND', 'Account activated by PIZZA HEN' in mu)
ok('FIX37_MEDIA_TILE_PRESERVED', '"applicationCategoryType": 65536' in param and 'PZHN00001' in param)
ok('FIX37_TARGET', 'PIZZA-HEN-v0.1-FIX45-PLUGIN-MANAGER-LIFECYCLE.elf' in cm)
ok('FIX37_GPL_NOTICE_PRESERVED', 'Copyright (C) 2025 etaHEN / LightningMods' in hf)

print(f'FIX37_STATIC={len(checks)}/{len(checks)} PASS')
