#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, sys

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
EXPECTED_LAUNCHER='7f7134593eefa9628bc581eebe3a7fc66f40cba3bb8f9447ebd641bfe58eb399'
EXPECTED_HELPER='8155569ab893e23d365b054d8c3075fcdebb6792b75f0ccf21d2bff33f76faf6'
locales=['ar-SA','zh-Hans','zh-Hant','cs-CZ','da-DK','nl-NL','en-GB','en-US','fi-FI','fr-CA','fr-FR','de-DE','el-GR','hu-HU','id-ID','it-IT','ja-JP','ko-KR','no-NO','pl-PL','pt-BR','pt-PT','ro-RO','ru-RU','es-419','es-ES','sv-SE','th-TH','tr-TR','uk-UA','vi-VN']

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
fail=0
def ck(name, cond):
    global fail
    print(f'R725213_{name}={"PASS" if cond else "FAIL"}')
    if not cond: fail += 1

launcher=SRC/'bootstrapper/assets/debug_services_launcher.html'
helper=SRC/'toolbox_action/src/main.c'
param=SRC/'bootstrapper/assets/debug_services_shortcut_param.json'
main=(SRC/'bootstrapper/source/main.cpp').read_text(errors='ignore')
embed=(SRC/'bootstrapper/source/daemon.c').read_text(errors='ignore')
build=(ROOT/'build_v01_rebase_latest_toolbox.sh').read_text(errors='ignore')
dbg=launcher.read_text(errors='ignore')
dp=json.loads(param.read_text())

ck('LAUNCHER_SHA_HARDWARE_FROZEN', sha(launcher)==EXPECTED_LAUNCHER)
ck('HELPER_SHA_FROZEN', sha(helper)==EXPECTED_HELPER)
ck('DIRECT_HELPER_PATH', '/data/PIZZA_HEN/bin/pizzahen-toolbox-open.elf' in dbg)
ck('DIRECT_HBLDR', '/hbldr?' in dbg)
ck('NO_PREHELPER_API', 'pizzahen-api.elf' not in dbg and 'locale-set' not in dbg and 'persistLocale' not in dbg)
ck('NO_R77_I18N_BLOB', 'PH_I18N=' not in dbg and 'phNormalizeLocale' not in dbg)
ck('DEBUG_TILE_ID', dp.get('titleId')=='PZHN00002')
ck('DEBUG_TILE_CATEGORY', dp.get('applicationCategoryType')==65536)
ck('DEBUG_TILE_DEEPLINK', dp.get('deeplinkUri')=='http://127.0.0.1:8080/fs/data/PIZZA_HEN/ui/debug-services-launcher.html')
ck('DEBUG_TILE_31_LOCALES', all(x in dp.get('localizedParameters',{}) for x in locales))
ck('DEPLOY_LAUNCHER', '/data/PIZZA_HEN/ui/debug-services-launcher.html' in main and 'debug_services_launcher_html_start' in main)
ck('INSTALL_DEBUG_TILE', 'install_pizzahen_debug_services_shortcut' in main and 'PZHN00002' in main)
ck('EMBED_LAUNCHER', 'debug_services_launcher.html' in embed)
ck('BUILD_HOOK', 'test_r725213_debug_services_hardware_launcher_restore.py' in build)
ck('BUILD_METADATA', 'R725213_DEBUG_SERVICES_LAUNCHER=R3_V01_HARDWARE_FROZEN_RESTORED' in build)

print(f'R7_25_2_13_DEBUG_SERVICES_HARDWARE_LAUNCHER_RESTORE={15-fail}/15 {"PASS" if fail==0 else "FAIL"}')
sys.exit(1 if fail else 0)
