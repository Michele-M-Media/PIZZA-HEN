#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, re, sys
R=Path(__file__).resolve().parents[1]
S=R/'Source Code'; A=S/'bootstrapper/assets'; F=R/'ThirdParty/R7.19-USER-SUPPLIED-SERVICES-FROZEN'
ui=(A/'toolbox_launcher.html').read_text(); main=(S/'bootstrapper/source/main.cpp').read_text(); daemon=(S/'bootstrapper/source/daemon.c').read_text(); api=(S/'toolbox_api/src/main.c').read_text(); msg=(S/'util/source/msg.cpp').read_text(); build=(R/'build_v01_rebase_latest_toolbox.sh').read_text()
EXPECTED=['en-US','en-GB','it-IT','fr-FR','fr-CA','de-DE','es-ES','es-419','pt-BR','pt-PT','nl-NL','da-DK','sv-SE','no-NO','fi-FI','pl-PL','cs-CZ','ro-RO','hu-HU','el-GR','tr-TR','ru-RU','uk-UA','id-ID','vi-VN','ja-JP','ko-KR','zh-Hans','zh-Hant','ar-SA','th-TH']
FILES={
'ps5-fw-spoof_v26616621599.elf':'f1754521caa92a6a1ac313a1b6c969ec49d67750e290ba99870958290a0961f0',
'airpsx_v0.19.elf':'ae025ca7727b3a8abf6a705903ca9116a6fa6e7f7ead606916109cf9044c5d63',
'ps5upload_v5.4.8.elf':'b255217ffcb5bc93a0ecdd4612927f241fbef3b3f936874223fcfba4cff17cf5',
'np-fake-signin_v1.3.elf':'f5c66fcb9e3f512e5463a7123d819b87f063d9955639366fa7ad26a2f0abefa4',
'webkit-autoloader-installer_v0.4.0-pre-00e1028.elf':'b920bc73133764a9847975a402b6f3bd4d9d97c797159153ccc5bcb98b6ee025',
'ps5-app-dumper_v1.11.elf':'18483751ebaea6879b020a9dd87c0a4fb4f1bf09f3708d950362a483f78cc0d0'}
PATHS=['/data/PIZZA_HEN/payloads/'+x for x in FILES]
checks=[]
def ck(n,v): checks.append((n,bool(v))); print(f'R719_{n}={"PASS" if v else "FAIL"}')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
for fn,h in FILES.items():
 ck('FROZEN_'+fn.upper().replace('.','_').replace('-','_'),(F/fn).is_file() and sha(F/fn)==h)
 ck('ASSET_'+fn.upper().replace('.','_').replace('-','_'),(A/fn).is_file() and sha(A/fn)==h)
# exact escaped incbins, extern/deploy
symbols={'ps5-fw-spoof_v26616621599.elf':'fw_spoof','airpsx_v0.19.elf':'airpsx','ps5upload_v5.4.8.elf':'ps5upload','np-fake-signin_v1.3.elf':'np_fake_signin','webkit-autoloader-installer_v0.4.0-pre-00e1028.elf':'wkali','ps5-app-dumper_v1.11.elf':'app_dumper'}
ck('ALL_ESCAPED_INCBINS',all((f'.incbin \\"../../../bootstrapper/assets/{fn}\\"' in daemon and f'{sym}_start' in daemon and f'{sym}_size' in daemon) for fn,sym in symbols.items()))
ck('ALL_DEPLOY_PATHS',all(p in main for p in PATHS))
ck('ALL_EXTERNS',all((f'extern uint8_t {sym}_start[];' in main and f'extern const unsigned int {sym}_size;' in main) for sym in symbols.values()))
# UI rows and switches
for iid,name in [('svc_airpsx','AirPSX 0.19'),('svc_ps5upload','PS5Upload 5.4.8'),('svc_fwspoof','PS5 FW Spoof'),('svc_npfake','NP Fake Signin 1.3'),('svc_wkali','WebKit Autoloader Installer'),('svc_appdumper','PS5 App Dumper 1.11')]:
 ck('SWITCH_'+iid.upper(),f'id="{iid}"' in ui and name in ui)
ck('AIRPSX_TCP_REAL','airpsx-status' in api and 'airpsx_port_ready' in api and 'htons(1214)' in api and "waitStatusAction('airpsx-status',on,40)" in ui)
ck('PS5UPLOAD_TCP_REAL','ps5upload-status' in api and 'ps5upload_port_ready' in api and 'htons(9114)' in api and "waitStatusAction('ps5upload-status',on,80)" in ui)
ck('TEMP_TASK_PID_STATE',all(x in ui for x in ['syncManagedTaskControl','toggleManagedTaskService','watchR719Task','managedPayloadRunning(path)','waitManagedPayloadState(path,false)']))
ck('DEDICATED_FILTER',all(('it.path!=='+c) in ui for c in ['AIRPSX_PATH','PS5UPLOAD_PATH','FW_SPOOF_PATH','NP_FAKE_SIGNIN_PATH','WKALI_PATH','APP_DUMPER_PATH']))
# no boot/autostart for six
ck('NO_NEW_AUTOSTART',all((f'plugin-autostart \'+'+c not in ui) for c in ['AIRPSX_PATH','PS5UPLOAD_PATH','FW_SPOOF_PATH','NP_FAKE_SIGNIN_PATH','WKALI_PATH','APP_DUMPER_PATH']) and not any(p in main[main.find('startup complete'):main.find('startup complete')+4000] for p in PATHS if main.find('startup complete')>=0))
# notifications localized via existing 31-language helper
ck('NOTIFY_SPECIAL_CASES',all(p in msg for p in PATHS) and all(n in msg for n in ['AirPSX 0.19 — %s','PS5Upload 5.4.8 — %s','PS5 FW Spoof — %s','NP Fake Signin 1.3 — %s','WebKit Autoloader Installer — %s','PS5 App Dumper 1.11 — %s']) and 'ph_service_notify_lang()' in msg)
# parse PH_I18N
m=re.search(r'const PH_I18N=(\{.*?\});',ui,re.S)
try: D=json.loads(m.group(1)) if m else {}
except Exception: D={}
keys=['services_summary','services_hint','airpsx_desc','ps5upload_desc','fwspoof_desc','npfake_desc','wkali_desc','appdumper_desc','task_running','task_finished','one_shot_applied','reboot_clears_spoof','signout_reverses_npfake']
ck('I18N_31_LOCALES',list(D.keys())==EXPECTED)
ck('I18N_KEYS_ALL_31',all(all(k in D.get(loc,{}) and str(D[loc][k]).strip() for k in keys) for loc in EXPECTED))
ck('I18N_BASE_MAP',all(x in ui for x in ['"Remote browser control service — resident HTTP service on TCP 1214":"airpsx_desc"','"High-speed transfer service — resident payload on TCP 9113 / 9114":"ps5upload_desc"','"One-shot firmware spoof to 99.99 — the payload exits after applying; reboot clears the effect":"fwspoof_desc"','"One-shot fake PSN sign-in — the payload exits after applying; use PS5 Sign out to reverse it":"npfake_desc"']))
# semantics honest
ck('ONE_SHOT_HONEST',"'one_shot_applied'" in ui and 'reboot_clears_spoof' in ui and 'signout_reverses_npfake' in ui and 'TOOLBOX_SERVICES_ONE_SHOT_PROCESS_STATE_REBOOT_CLEARS_EFFECT' in build and 'TOOLBOX_SERVICES_ONE_SHOT_PROCESS_STATE_SIGN_OUT_REVERSES_EFFECT' in build)
ck('BUILD_VERIFY_ALL',all(('verify_frozen_elf_only '+label) in build for label in ['FW_SPOOF','AIRPSX','PS5UPLOAD','NP_FAKE_SIGNIN','WKALI','APP_DUMPER']))
ck('BUILD_METADATA','R719_AIRPSX_PORT=1214' in build and 'R719_PS5UPLOAD_MANAGEMENT_PORT=9114' in build and 'R719_WKALI_PORT=18181' in build and 'R719_I18N_LOCALES=31' in build)
ck('CE108262_RULE','cmd_preload_toolbox_hooks();' not in main)
failed=[n for n,v in checks if not v]
print(f'R7_19_SIX_SERVICES_FULL_I18N={len(checks)-len(failed)}/{len(checks)} PASS' if not failed else f'R7_19_SIX_SERVICES_FULL_I18N=FAIL {failed}')
sys.exit(1 if failed else 0)
