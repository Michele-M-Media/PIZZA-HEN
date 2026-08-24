#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(__file__).resolve().parents[1]
UI=(ROOT/'Source Code/bootstrapper/assets/toolbox_launcher.html').read_text(errors='ignore')
MAIN=(ROOT/'Source Code/bootstrapper/source/main.cpp').read_text(errors='ignore')
DAEMON=(ROOT/'Source Code/bootstrapper/source/daemon.c').read_text(errors='ignore')
MSG=(ROOT/'Source Code/util/source/msg.cpp').read_text(errors='ignore')
BUILD=(ROOT/'build_v01_rebase_latest_toolbox.sh').read_text(errors='ignore')
fail=0; total=0
def ck(name,cond):
    global fail,total
    total+=1
    print(f"R72528_{name}={'PASS' if cond else 'FAIL'}")
    if not cond: fail+=1

# PS-Play remains manually launchable in Services, but must never boot-autostart from any scanned root.
ck('PSPLAY_SERVICE_PRESERVED','<span class="etaServiceTitle">PS-Play 2.1</span>' in UI and 'PS_PLAY_PATH' in UI)
ck('AUTOSTART_NAME_GATE','static bool pizzahen_manual_only_payload_name' in MAIN and '"PS-Play_v2.1.elf"' in MAIN)
ck('AUTOSTART_SCAN_CALL','if (pizzahen_manual_only_payload_name(entry->d_name))' in MAIN)
ck('AUTOSTART_SCAN_BEFORE_MARKER',MAIN.find('if (pizzahen_manual_only_payload_name(entry->d_name))') < MAIN.find('if (!if_exists(auto_start_path))'))
ck('SCANNED_ROOTS_INCLUDE_USB','/mnt/usb0/PIZZA_HEN/payloads' in MAIN and '/mnt/usb3/PIZZA_HEN/payloads' in MAIN)
ck('SCANNED_ROOTS_INCLUDE_LEGACY','/user/data/etahen/payloads' in MAIN)

# Remote_Play and garlic-worker are fully retired from Services and embedding/deployment.
for name,sid,const,asset,sym in [
 ('Remote Play','svc_rp_original','RP_ORIGINAL_SERVICE','Remote_Play.elf','remote_play_service_start'),
 ('Garlic Worker 1.1.6','svc_garlic_worker','GARLIC_WORKER_SERVICE','garlic-worker_v1.1.6.elf','garlic_worker_start')]:
    ck(asset.upper().replace('.','_').replace('-','_')+'_NO_SERVICE_ROW',f'<span class="etaServiceTitle">{name}</span>' not in UI and sid not in UI and const not in UI)
    ck(asset.upper().replace('.','_').replace('-','_')+'_NO_EMBED',sym not in DAEMON and sym not in MAIN)
    ck(asset.upper().replace('.','_').replace('-','_')+'_NO_ASSET',not (ROOT/'Source Code/bootstrapper/assets'/asset).exists())

ck('REMOTE_FROZEN_REMOVED',not (ROOT/'ThirdParty/Remote-Play-USER-SUPPLIED-FROZEN').exists())
ck('GARLIC_FROZEN_REMOVED',not (ROOT/'ThirdParty/garlic-worker-v1.1.6-USER-SUPPLIED-FROZEN').exists())
ck('STALE_REMOTE_PURGE','unlink("/data/PIZZA_HEN/payloads/Remote_Play.elf")' in MAIN and 'unlink("/user/data/PIZZA_HEN/payloads/Remote_Play.elf")' in MAIN)
ck('STALE_GARLIC_PURGE','unlink("/data/PIZZA_HEN/payloads/garlic-worker_v1.1.6.elf")' in MAIN and 'unlink("/user/data/PIZZA_HEN/payloads/garlic-worker_v1.1.6.elf")' in MAIN)
ck('RETIRED_AUTOSTART_NAME_GATE','"Remote_Play.elf"' in MAIN and '"garlic-worker_v1.1.6.elf"' in MAIN)
ck('BUILD_GATES_REMOVED','REMOTE_PLAY_SERVICE_ELF=' not in BUILD and 'GARLIC_WORKER_ELF=' not in BUILD and 'verify_frozen_elf_only REMOTE_PLAY_SERVICE' not in BUILD and 'verify_frozen_elf_only GARLIC_WORKER' not in BUILD)
ck('BUILD_METADATA','R72528_PSPLAY_AUTOSTART=HARD_FILENAME_BLOCK_ALL_SCANNED_ROOTS' in BUILD and 'R72528_REMOTE_PLAY_SERVICE=RETIRED_PURGED' in BUILD and 'R72528_GARLIC_WORKER_SERVICE=RETIRED_PURGED' in BUILD)
ck('BUILD_HOOK','test_r72528_psplay_autostart_remove_remote_garlic.py' in BUILD)

print(f"R7_25_2_8_PSPLAY_AUTOSTART_REMOVE_REMOTE_GARLIC={total-fail}/{total} {'PASS' if fail==0 else 'FAIL'}")
sys.exit(1 if fail else 0)
