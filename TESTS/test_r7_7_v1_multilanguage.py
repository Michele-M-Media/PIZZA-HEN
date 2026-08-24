#!/usr/bin/env python3
from pathlib import Path
import json, re, sys
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
locales=['ar-SA', 'zh-Hans', 'zh-Hant', 'cs-CZ', 'da-DK', 'nl-NL', 'en-GB', 'en-US', 'fi-FI', 'fr-CA', 'fr-FR', 'de-DE', 'el-GR', 'hu-HU', 'id-ID', 'it-IT', 'ja-JP', 'ko-KR', 'no-NO', 'pl-PL', 'pt-BR', 'pt-PT', 'ro-RO', 'ru-RU', 'es-419', 'es-ES', 'sv-SE', 'th-TH', 'tr-TR', 'uk-UA', 'vi-VN']
web=(SRC/'bootstrapper/assets/toolbox_launcher.html').read_text(encoding='utf-8')
dbg=(SRC/'bootstrapper/assets/debug_services_launcher.html').read_text(encoding='utf-8')
api=(SRC/'toolbox_api/src/main.c').read_text(encoding='utf-8')
cpp=(SRC/'shellui/src/HookFunctions.cpp').read_text(encoding='utf-8')
tp=json.loads((SRC/'bootstrapper/assets/toolbox_shortcut_param.json').read_text(encoding='utf-8'))
dp=json.loads((SRC/'bootstrapper/assets/debug_services_shortcut_param.json').read_text(encoding='utf-8'))
build=(ROOT/'build_v01_rebase_latest_toolbox.sh').read_text(encoding='utf-8')
checks={
'R77_31_LOCALES_WEB': all(('"'+x+'"') in web for x in locales),
'R77_DEBUG_LAUNCHER_HARDWARE_FROZEN': __import__('hashlib').sha256(dbg.encode('utf-8')).hexdigest()=='7f7134593eefa9628bc581eebe3a7fc66f40cba3bb8f9447ebd641bfe58eb399',
'R77_31_LOCALES_NATIVE': all(('"'+x+'"') in cpp for x in locales),
'R77_SHORTCUT_LOCALES_TOOLBOX': all(x in tp['localizedParameters'] for x in locales),
'R77_SHORTCUT_LOCALES_DEBUG': all(x in dp['localizedParameters'] for x in locales),
'R77_OS_WEBVIEW_LANGUAGE': 'navigator.languages' in web and 'navigator.language' in web and 'phNormalizeLocale' in web,
'R77_LOCALE_SET_ACTION': '"locale-set"' in api and 'persist_ui_locale' in api,
'R77_LOCALE_DUAL_PATH': '/data/PIZZA_HEN/runtime/ui_locale.txt' in api and '/user/data/PIZZA_HEN/runtime/ui_locale.txt' in api,
'R77_DEBUG_DIRECT_V01_HELPER': "/data/PIZZA_HEN/bin/pizzahen-toolbox-open.elf" in dbg and "/hbldr?" in dbg and "pizzahen-api.elf" not in dbg and "locale-set" not in dbg,
'R77_NATIVE_READS_LOCALE': '/user/data/PIZZA_HEN/runtime/ui_locale.txt' in cpp and 'ph_locale_index()' in cpp,
'R77_NATIVE_LOCALIZES_XML': 'ph_localize_xml(new_xml_string, ph_strip_details);' in cpp,
'R77_DEBUG_TITLE_LOCALIZED': 'PH_DEBUG_SERVICES' in cpp,
'R77_ARABIC_RTL': "PH_LOCALE==='ar-SA'?'rtl':'ltr'" in web,
'R77_NO_TOOLBOX_AUTOINJECT': "game-options-ensure').catch" not in web and "setTimeout(()=>runAction('game-options-ensure')" not in web,
'R77_HIDDEN_HOSTS_PRESERVED': all(('id="'+x+'"') in web for x in ['system','rest','shortcuts','advanced','store','webman']),
'R77_PAYLOAD_MANAGER_PRESERVED': 'AGGIORNA REPOSITORY' in web and 'payload-repo-refresh' in web,
'R77_SCANNER_PRESERVED': 'plugin-scan' in web and 'SCANSIONA' in web,
'R77_OUTPUT_NAMES_V200_INTENTIONAL_DELTA': 'PIZZA-HEN-v2.00.elf' in build and 'PIZZA-HEN-v2.00.bin' in build and 'PIZZA_HEN_VERSION=2.00-COMPLETE-I18N-HARDWARE-BASELINE' in build,
}
fail=[k for k,v in checks.items() if not v]
for k,v in checks.items(): print(k+'='+('PASS' if v else 'FAIL'))
if fail: sys.exit(1)
print('R7_7_V1_MULTILANGUAGE=PASS')
