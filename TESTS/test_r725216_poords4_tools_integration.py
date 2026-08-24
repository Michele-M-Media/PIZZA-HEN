#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys, zipfile

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
UI=(SRC/'bootstrapper/assets/toolbox_launcher.html').read_text(encoding='utf-8')
MAIN=(SRC/'daemon/source/main.cpp').read_text(encoding='utf-8')
EMBED=(SRC/'daemon/source/embeddded_payloads.c').read_text(encoding='utf-8')
BUILD=(ROOT/'build_v01_rebase_latest_toolbox.sh').read_text(encoding='utf-8')
THIRD=(ROOT/'THIRD_PARTY.md').read_text(encoding='utf-8')
FROZEN=ROOT/'ThirdParty/PoorDS4-0.1.0-rc38-USER-SUPPLIED-FROZEN'

EXP={
 'PoorDS4rc38.elf':'62d21fe837ee53dd4291e45d99259d4557def05e2d4196ab54e020ba28b5399e',
 'PoorDS4-status.elf':'c26a35a2c9ba9074ad33cf27a5afbd05536978518c546552df21d512b07a273d',
 'PoorDS4-stop.elf':'bf9f1dec35edcffe3744fbc69cb7d4601f6df3cef72fab36c38fd249e736107a',
 'PoorDS4-0.1.0-rc38.zip':'5634b504b0eae5302a875346dc30449e05fd5932ef18baea8e046415a19ea41b',
 'SHA256SUMS.txt':'ec0533ec626a276d77bfc04325a2963fdd421c26549845c46607eb1227bf580a',
}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def ck(name, ok):
    checks.append((name,bool(ok)))
    print(f'{name}={"PASS" if ok else "FAIL"}')

for name,h in EXP.items():
    ck('FROZEN_'+name.replace('.','_').replace('-','_').upper(), (FROZEN/name).is_file() and sha(FROZEN/name)==h)

for name in ('PoorDS4rc38.elf','PoorDS4-status.elf','PoorDS4-stop.elf'):
    ck('DAEMON_ASSET_'+name.replace('.','_').replace('-','_').upper(),
       (SRC/'daemon/assets'/name).is_file() and sha(SRC/'daemon/assets'/name)==EXP[name])

ck('TOOLS_ENTRY', 'onclick="show(\'poords4\')"' in UI and '<span class="etaItemTitle">PoorDS4</span>' in UI)
ck('DEDICATED_PANEL', '<section id="poords4" class="panel">' in UI and "poords4:'PoorDS4'" in UI)
ck('MAIN_PATH', "const POORDS4_MAIN_PATH='/data/PIZZA_HEN/payloads/PoorDS4rc38.elf';" in UI)
ck('STATUS_PATH', "const POORDS4_STATUS_PATH='/data/PIZZA_HEN/payloads/PoorDS4-status.elf';" in UI)
ck('STOP_PATH', "const POORDS4_STOP_PATH='/data/PIZZA_HEN/payloads/PoorDS4-stop.elf';" in UI)
ck('START_DIRECT_ORIGINAL', 'await launchElfDirect(POORDS4_MAIN_PATH)' in UI)
ck('STATUS_DIRECT_ORIGINAL', 'await launchElfDirect(POORDS4_STATUS_PATH)' in UI)
ck('STATUS_READ_ONLY_REPORT', "/fs/data/poords4/game-pad-bridge-status.txt" in UI and 'out.textContent=raw' in UI)
ck('STOP_COOPERATIVE_ORIGINAL', 'await launchElfDirect(POORDS4_STOP_PATH)' in UI and 'plugin-stop '+ 'POORDS4_MAIN_PATH' not in UI)
ck('NO_AUTOSTART', 'PoorDS4rc38.elf.auto_start' not in UI+MAIN+BUILD and 'plugin-autostart '+ 'POORDS4_MAIN_PATH' not in UI)
ck('EMBED_MAIN', '.incbin \\"../../../daemon/assets/PoorDS4rc38.elf\\"' in EMBED)
ck('EMBED_STATUS', '.incbin \\"../../../daemon/assets/PoorDS4-status.elf\\"' in EMBED)
ck('EMBED_STOP', '.incbin \\"../../../daemon/assets/PoorDS4-stop.elf\\"' in EMBED)
ck('DEPLOY_MAIN', '"/data/PIZZA_HEN/payloads/PoorDS4rc38.elf", pizzahen_poords4_main_start' in MAIN)
ck('DEPLOY_STATUS', '"/data/PIZZA_HEN/payloads/PoorDS4-status.elf", pizzahen_poords4_status_start' in MAIN)
ck('DEPLOY_STOP', '"/data/PIZZA_HEN/payloads/PoorDS4-stop.elf", pizzahen_poords4_stop_start' in MAIN)
ck('UPSTREAM_FW_TEXT', '11.60' in UI and '8.60' in UI and '12.40' in UI and 'structural-admission only' in UI)
ck('UPSTREAM_REST_POLICY', 'reinject it after wake' in UI)
ck('UPSTREAM_ONE_INSTANCE', 'one automatic instance only' in UI)
ck('PROJECT_ATTRIBUTION_UI', 'PoorDS4 by ItsBlurf' in UI)
ck('PROJECT_ATTRIBUTION_DOC', 'PoorDS4' in THIRD)
ck('BUILD_GATE', 'verify_frozen_elf_source POORDS4_RC38' in BUILD and 'verify_frozen_elf_only POORDS4_STATUS' in BUILD and 'verify_frozen_elf_only POORDS4_STOP' in BUILD)
ck('BUILD_TEST_HOOK', 'test_r725216_poords4_tools_integration.py' in BUILD)
ck('BUILD_METADATA', 'R725216_POORDS4_BINARY_POLICY=BYTE_EXACT_USER_SUPPLIED_NO_PATCHING' in BUILD)
ck('SOURCE_ZIP_VALID', zipfile.is_zipfile(FROZEN/'PoorDS4-0.1.0-rc38.zip'))

fail=sum(1 for _,ok in checks if not ok)
print(f'R7_25_2_16_POORDS4_TOOLS_INTEGRATION={len(checks)-fail}/{len(checks)} {"PASS" if fail==0 else "FAIL"}')
sys.exit(1 if fail else 0)
