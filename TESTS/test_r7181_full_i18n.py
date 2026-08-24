#!/usr/bin/env python3
import json,re,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
A=ROOT/'Source Code/bootstrapper/assets'
EXPECTED=['en-US','en-GB','it-IT','fr-FR','fr-CA','de-DE','es-ES','es-419','pt-BR','pt-PT','nl-NL','da-DK','sv-SE','no-NO','fi-FI','pl-PL','cs-CZ','ro-RO','hu-HU','el-GR','tr-TR','ru-RU','uk-UA','id-ID','vi-VN','ja-JP','ko-KR','zh-Hans','zh-Hant','ar-SA','th-TH']
checks=[]
def ck(name,cond): checks.append((name,bool(cond)))
def obj(path,var):
 s=path.read_text();m=re.search(r'const '+re.escape(var)+r'=(\{.*?\});',s,re.S);return s,json.loads(m.group(1))
# toolbox
ts,td=obj(A/'toolbox_launcher.html','PH_I18N')
req=['homebrew_channel','homebrew_channel_desc','homebrew_channel_opening','apr_emu_update','apr_emu_desc','apr_emu_starting','services_summary','services_hint','elfldr_desc','backpork_desc','garlic_desc','resident_state_mismatch','tcp_state_mismatch']
ck('R7181_TOOLBOX_31_LOCALES',list(td.keys())==EXPECTED)
ck('R7181_TOOLBOX_NEW_KEYS_ALL_31',all(all(k in td[c] and td[c][k].strip() for k in req) for c in EXPECTED))
ck('R7181_TOOLBOX_NO_NEW_FALLBACK_COPY',all(td[c]['homebrew_channel_desc']!=td['en-US']['homebrew_channel_desc'] for c in EXPECTED if c not in ('en-US','en-GB')))
ck('R7181_TOOLBOX_BASEMAP_NEW_ITEMS',all(x in ts for x in ['"Homebrew Channel":"homebrew_channel"','"APR EMU UPDATE":"apr_emu_update"','"BestPig BackPork — background fakelib sideload monitor":"backpork_desc"','"earthonion Garlic SaveMgr — local save manager web server on TCP 8082":"garlic_desc"']))
ck('R7181_TOOLBOX_DYNAMIC_STATUS_I18N',"phText('homebrew_channel_opening')" in ts and "phText('apr_emu_starting')" in ts and "phText('resident_state_mismatch')" in ts and "phText('tcp_state_mismatch')" in ts)
# kstuff js/html both complete
for fn in ['kstuff_selector.js','kstuff_selector.html']:
 s,d=obj(A/fn,'PH_SELECTOR_I18N')
 ck('R7181_KSTUFF_31_'+fn,list(d.keys())==EXPECTED)
 ck('R7181_KSTUFF_BASE_ALL_'+fn,all(all(k in d[c] and d[c][k].strip() for k in ['base','base_desc','base_author','footer']) for c in EXPECTED))
ck('R7181_KSTUFF_ARABIC_RTL',"PH_LOCALE==='ar-SA'?'rtl':'ltr'" in (A/'kstuff_selector.html').read_text())
# shadow full 31
ss,sd=obj(A/'shadowmount_selector.html','I18N')
sreq=['sub','badge','stable','experimental','skip','skipDesc','stableAuthor','experimentalAuthor','stableDesc','experimentalDesc','waiting','requesting','selected','active','failed','foot']
ck('R7181_SHADOW_31_LOCALES',list(sd.keys())==EXPECTED)
ck('R7181_SHADOW_KEYS_ALL_31',all(all(k in sd[c] and sd[c][k].strip() for k in sreq) for c in EXPECTED))
ck('R7181_SHADOW_ARABIC_RTL',"L==='ar-SA'?'rtl':'ltr'" in ss)
ck('R7181_SHADOW_AUTHOR_I18N',"stableAuthor').textContent=T.stableAuthor" in ss and "experimentalAuthor').textContent=T.experimentalAuthor" in ss)
# notifications
ms=(ROOT/'Source Code/util/source/msg.cpp').read_text()
ck('R7181_NOTIFY_31_LOCALES',all(('"'+c+'"') in ms for c in EXPECTED) and ms.count('PhServiceNotifyLang')>=2)
ck('R7181_NOTIFY_ADDED_SERVICES_I18N','nt->started' in ms and 'nt->stopped' in ms and 'nt->failed' in ms and 'nt->deploy_failed' in ms)
ck('R7181_NOTIFY_OLD_HARDCODED_GONE',all(x not in ms for x in ['BackPork 0.1 Started','BackPork 0.1 Stopped','Garlic SaveMgr Started','Garlic SaveMgr Stopped','ELF Loader 0.24 Started','ELF Loader 0.24 Stopped','ELF Loader 0.24 Failed to Start']))
# policy
doc=(ROOT/'R7_18_1_FULL_I18N_REPAIR.txt').read_text()
ck('R7181_I18N_FIRST_POLICY','every new PIZZA HEN user-visible title, description, selector label, status, error and notification' in doc)
for n,v in checks: print(f'{n}={"PASS" if v else "FAIL"}')
failed=[n for n,v in checks if not v]
print(f'R7_18_1_FULL_I18N={len(checks)-len(failed)}/{len(checks)} PASS' if not failed else f'R7_18_1_FULL_I18N=FAIL {failed}')
sys.exit(1 if failed else 0)
