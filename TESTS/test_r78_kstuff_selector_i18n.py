#!/usr/bin/env python3
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/'Source Code/bootstrapper/assets/kstuff_selector.html').read_text(encoding='utf-8')
js=(ROOT/'Source Code/bootstrapper/assets/kstuff_selector.js').read_text(encoding='utf-8')
locales=['en-US','en-GB','it-IT','fr-FR','fr-CA','de-DE','es-ES','es-419','pt-BR','pt-PT','nl-NL','da-DK','sv-SE','no-NO','fi-FI','pl-PL','cs-CZ','ro-RO','hu-HU','el-GR','tr-TR','ru-RU','uk-UA','id-ID','vi-VN','ja-JP','ko-KR','zh-Hans','zh-Hant','ar-SA','th-TH']
checks={
 'HTML_LOCALE_DETECT': 'navigator.languages' in html and 'phNormalizeLocale' in html,
 'HTML_RTL': "PH_LOCALE==='ar-SA'?'rtl':'ltr'" in html,
 'HTML_ALL_31': all(('"'+l+'"') in html for l in locales),
 'JS_ALL_31': all(('"'+l+'"') in js for l in locales),
 'HTML_VISIBLE_IDS': all(x in html for x in ['selectorSub','selectorBadge','liteMode','drMode','liteDesc','drDesc','selectorFoot']),
 'HTML_DYNAMIC_STATUS': all(x in html for x in ["phFmt('requesting'","phFmt('selected'","phFmt('failed'","phFmt('active'"]),
 'JS_DYNAMIC_LABELS': "phSelectorText('modern')" in js and "phSelectorText('compat')" in js and "phSelectorText('selector')" in js,
 'ITALIAN_SELECTOR': 'Scegli il motore KStuff per questa sessione' in html,
 'ITALIAN_ACTIVE': 'Motore attivo: {engine}' in html,
 'ARABIC_PRESENT': 'اختر محرك KStuff لهذه الجلسة' in html,
 'ENGLISH_FALLBACK': 'Choose the KStuff engine for this session' in html,
}
failed=[]
for k,v in checks.items():
 print(f'R78_{k}={"PASS" if v else "FAIL"}')
 if not v: failed.append(k)
print(f'R7_8_KSTUFF_SELECTOR_I18N={len(checks)-len(failed)}/{len(checks)} '+('PASS' if not failed else 'FAIL'))
raise SystemExit(1 if failed else 0)
