#!/usr/bin/env python3
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
hf=(SRC/'shellui/src/HookFunctions.cpp').read_text(errors='ignore')
tb=(SRC/'bootstrapper/assets/toolbox_launcher.html').read_text(errors='ignore')
dpi=SRC/'util/source/DirectPKGInstaller.cpp'
checks=[]
def check(name, cond):
    print(f'{name}={"PASS" if cond else "FAIL"}')
    checks.append(bool(cond))
url='http://127.0.0.1:8080/fs/data/PIZZA_HEN/ui/toolbox-launcher.html#cheats'
block='if(id_str == "MENU_ID_CHECK_PATCH")'
check('R713_GAME_OPTIONS_SLOT', block in hf)
check('R713_MENU_ID_CHEATRUNNER', 'MENU_ID_CHEATRUNNER' in hf)
check('R713_LABEL_EXACT', 'mono_string_new(Root_Domain, "CheatRunner")' in hf)
check('R713_DIRECT_TOOLBOX_CHEATS_URL', url in hf)
check('R713_SIMPLE_REPLACE_RETURN', 'MENU_ID_CHEATRUNNER' in hf and 'return;' in hf[hf.index('MENU_ID_CHEATRUNNER'):hf.index('MENU_ID_CHEATRUNNER')+600])
check('R713_NO_DIRECT_9999_FROM_GAME_OPTIONS', 'MENU_ID_CHEATRUNNER' in hf and 'http://127.0.0.1:9999' not in hf[hf.index(block):hf.index(block)+1000])
check('R713_TOOLBOX_CHEATS_PANEL_EXISTS', 'id="cheats"' in tb and 'Cheats — CheatRunner 0.17' in tb)
check('R713_TOOLBOX_AUTOSTART_ON_PAGE', "if(id==='cheats'){startCheatRunner(false)}" in tb)
check('R713_NO_NEW_GAME_OPTIONS_AUTOINJECT', "setTimeout(()=>runAction('game-options-ensure')" not in tb)
check('R713_NO_NEW_CHEATRUNNER_PRELOAD', 'pizzahen_cheatrunner_start' not in hf)
check('R713_DPIV2_R711_FROZEN_SHA', hashlib.sha256(dpi.read_bytes()).hexdigest()=='5a14caa77e9e121eea5a5c3ebd2de40c6c4ad1736e79714b7c4a6b6bc2b54d69')
print(f'R7_13_CHEATRUNNER_GAME_OPTIONS_SHORTCUT={sum(checks)}/{len(checks)} '+('PASS' if all(checks) else 'FAIL'))
if not all(checks): raise SystemExit(1)
