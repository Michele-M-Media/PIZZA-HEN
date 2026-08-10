#!/usr/bin/env python3
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
main=(SRC/'bootstrapper/source/main.cpp').read_text()
param=json.loads((SRC/'bootstrapper/assets/toolbox_shortcut_param.json').read_text())
action=(SRC/'toolbox_action/src/main.c').read_text()
xml=(SRC/'shellui/assets/etaHEN_toolbox.xml').read_text()

def ok(name, cond):
    print(f"{name}={'PASS' if cond else 'FAIL'}")
    if not cond: raise SystemExit(1)

id=param.get('titleId','')
ok('VALID_PS_TITLE_ID_FORMAT', re.fullmatch(r'[A-Z]{4}[0-9]{5}', id) is not None)
ok('TITLE_ID_IS_PZHN00001', id=='PZHN00001')
ok('MEDIA_CATEGORY_65536', param.get('applicationCategoryType')==65536)
ok('LOCALHOST_DEEPLINK', param.get('deeplinkUri','').startswith('http://127.0.0.1:8080/'))
ok('BOOTSTRAPPER_USES_VALID_ID', 'PZHN00001' in main)
ok('TOOLBOX_ACTION_USES_VALID_ID', 'PZHN00001' in action)
ok('TOOLBOX_LABEL_USES_VALID_ID', 'PZHN00001' in xml)
ok('LEGACY_INVALID_ID_CLEANUP', 'cleanup_legacy_invalid_pizzahen_tile' in main and '/user/app/PIZZA0001' in main)
ok('LEGACY_ID_NOT_ACTIVE_PARAM', 'PIZZA0001' not in (SRC/'bootstrapper/assets/toolbox_shortcut_param.json').read_text())
ok('APPINSTALL_TITLE_DIR', 'sceAppInstUtilAppInstallTitleDir(title_id, "/user/app/", nullptr)' in main)
ok('NOTIFICATION_PRESERVED', 'PIZZA HEN Toolbox icon install failed' in main)
ok('KSTUFF_SELECTOR_PRESERVED', 'start_browser_kstuff_selector()' in main and 'kstuff-lite-1.09' in main and 'kstuff-dr-1.2' in main)
print('FIX34_STATIC=12/12 PASS')
