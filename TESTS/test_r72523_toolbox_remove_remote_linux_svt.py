#!/usr/bin/env python3
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
UI=(ROOT/'Source Code/bootstrapper/assets/toolbox_launcher.html').read_text(errors='ignore')
fail=0
def ck(name,cond):
    global fail
    print(f"R72523_{name}={'PASS' if cond else 'FAIL'}")
    if not cond: fail+=1

# Physical UI removal: no hidden placeholders and no alternate Remote Play entry.
for label,key in [('Remote Play','REMOTE_PLAY'),('Linux Loader','LINUX_LOADER'),('SVT Play','SVT_PLAY')]:
    ck(key+'_MENU_ABSENT', f'<span class="etaItemTitle">{label}</span>' not in UI)
ck('REMOTE_PANEL_ABSENT','id="remoteplay"' not in UI and 'svc_remote_play' not in UI)
ck('REMOTE_ADVANCED_ABSENT','generateRemotePlayPin' not in UI)
ck('LINUX_ACTION_ABSENT','openLinuxLoader' not in UI and 'LINUX_FW_SUPPORTED' not in UI and 'LINUX_LOADER_PATH' not in UI)
ck('SVT_ACTION_ABSENT','openSvtPlay' not in UI and 'SVT_PLAY_URL' not in UI)
ck('REMOTE_ACTION_ABSENT','REMOTE_PLAY_PATH' not in UI)

# They must not reappear through the Toolbox local plugin scan or repository list.
ck('LOCAL_SCAN_FILTERS_RETIRED_TOOLS', all(x in UI for x in [
    "it.path!=='/data/PIZZA_HEN/payloads/rp-get-pin.elf'",
    "it.path!=='/data/PIZZA_HEN/payloads/ps5-linux-loader.elf'",
    "it.path!=='/data/PIZZA_HEN/payloads/svtplay_v0.2.elf'",
]))
ck('REPOSITORY_FILTERS_RETIRED_TOOLS', all(x in UI for x in [
    'ps5-remoteplay-get-pin_v0.1.1.elf','ps5-linux-loader_v2.4.elf','svtplay_v0.2.elf'
]))

# Current useful entries remain.
ck('DNS_MENU_SUPERSEDED','<span class="etaItemTitle">Cambia DNS</span>' not in UI and "show('dns')" not in UI and 'svc_chukei_dns' in UI and 'svc_nanodns' in UI)
ck('WEB_FILE_MANAGER_PRESENT','<span class="etaItemTitle">Web File Manager</span>' in UI)
ck('GAME_DOWNLOAD_PRESENT','<span class="etaItemTitle">Game Download</span>' in UI)
ck('SVT_NEIGHBOR_PLAYERS_UNTOUCHED','PROSPERO_PLAYER_PATH' in UI and 'PS_PLAY_PATH' in UI and 'BFPLAYER_PATH' in UI)

# Removed labels are also gone from the i18n surface; DNS remains 31-language.
m=re.search(r'const PH_I18N=(\{.*?\});\nconst PH_BASE_MAP=',UI,re.S)
i18n=json.loads(m.group(1)) if m else {}
retired={'remote_play','remote_play_desc','remote_play_starting','remote_play_ready','linux_loader','linux_loader_desc','linux_loader_unsupported','linux_loader_ready','svt_play','svt_play_desc','svt_play_opening'}
ck('I18N_31',len(i18n)==31)
ck('RETIRED_I18N_KEYS_ABSENT',all(not(retired & set(v)) for v in i18n.values()))
ck('DNS_I18N_RETIRED',all('change_dns' not in v and 'change_dns_desc' not in v for v in i18n.values()))

print(f"R7_25_2_3_TOOLBOX_CLEANUP={18-fail}/18 {'PASS' if fail==0 else 'FAIL'}")
sys.exit(1 if fail else 0)
