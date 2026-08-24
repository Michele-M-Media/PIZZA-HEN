#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,re,sys
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
    print(f"R72527_{name}={'PASS' if cond else 'FAIL'}")
    if not cond: fail+=1
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

items=[
 ('UNRAR','ThirdParty/unrar-ps5-v1.4.0-USER-SUPPLIED-FROZEN/unrar-ps5_v1.4.0.elf','Source Code/bootstrapper/assets/unrar-ps5_v1.4.0.elf','2ef04b0bc8fc1932b29da1a53336c40ed0a3f6a945a0746bef2e5dde52149701','UnRAR PS5 1.4.0','svc_unrar_ps5','UNRAR_SERVICE_PATH','/data/PIZZA_HEN/payloads/unrar-ps5_v1.4.0.elf'),
 ('GAME_STATE','ThirdParty/PS-Game-State-Lib-v0.1-USER-SUPPLIED-FROZEN/PS_Game_State_Lib_v0.1.elf','Source Code/bootstrapper/assets/PS_Game_State_Lib_v0.1.elf','a550e1494b0f8be3b244f8820ee8d899442d33a936f9ded6203a0318c7afdba8','PS Game State Lib 0.1','svc_ps_game_state','PS_GAME_STATE_SERVICE','/data/PIZZA_HEN/payloads/PS_Game_State_Lib_v0.1.elf'),
 ('GHOSTPAD','ThirdParty/Ghostpad-v1.0.0-USER-SUPPLIED-FROZEN/Ghostpad_v1.0.0.elf','Source Code/bootstrapper/assets/Ghostpad_v1.0.0.elf','94d43a8db7ec9df6e18f0a0da25aac0f60e1a0b14d35bfff261f6f5cdeabdba1','Ghostpad 1.0.0','svc_ghostpad','GHOSTPAD_SERVICE','/data/PIZZA_HEN/payloads/Ghostpad_v1.0.0.elf'),
 ('GHOSTCONTROL','ThirdParty/Ghostcontrol-v1.0.5-USER-SUPPLIED-FROZEN/Ghostcontrol-PS5-USB-Controller-Patcher_v1.0.5.elf','Source Code/bootstrapper/assets/Ghostcontrol-PS5-USB-Controller-Patcher_v1.0.5.elf','69271d91f27397c9ad42150129639ce452ecb405021108f42c6c87926123a6f1','Ghostcontrol 1.0.5','svc_ghostcontrol','GHOSTCONTROL_SERVICE','/data/PIZZA_HEN/payloads/Ghostcontrol-PS5-USB-Controller-Patcher_v1.0.5.elf'),
 ('PS_DISCORD','ThirdParty/PS-DiscordPresence-v0.01-USER-SUPPLIED-FROZEN/PS-DiscordPresence_v0.01.elf','Source Code/bootstrapper/assets/PS-DiscordPresence_v0.01.elf','375cf619ea6f6c594ea2b79ecbb98704723522d07e51c877687876d5fe589afb','PS-DiscordPresence 0.01','svc_ps_discord','PS_DISCORD_SERVICE','/data/PIZZA_HEN/payloads/PS-DiscordPresence_v0.01.elf'),
 ('LINUX24','ThirdParty/ps5-linux-loader-v2.4-USER-SUPPLIED-FROZEN/ps5-linux-loader_v2.4.elf','Source Code/bootstrapper/assets/ps5-linux-loader.elf','51382795b486f7c5a3681648d457d129088311fc3f9601aeaff78dc72fafcf1d','PS5 Linux Loader 2.4','svc_linux24','LINUX24_SERVICE','/data/PIZZA_HEN/payloads/ps5-linux-loader.elf'),
]
for key,frozen,asset,expected,title,sid,const,path in items:
    fp=ROOT/frozen; ap=ROOT/asset
    ck(key+'_FROZEN_SHA',fp.is_file() and sha(fp)==expected)
    ck(key+'_ASSET_BYTE_EXACT',ap.is_file() and ap.read_bytes()==fp.read_bytes())
    ck(key+'_SERVICES_ROW',f'<span class="etaServiceTitle">{title}</span>' in UI and f'id="{sid}"' in UI)
    ck(key+'_STANDARD_SWITCH',f'toggleManagedTaskService(this.checked,this,{const}' in UI)
    ck(key+'_PATH',f"const {const}='{path}';" in UI)
    ck(key+'_SYNC',f"syncManagedTaskControl('{sid}',{const})" in UI)
    ck(key+'_LOCAL_SCAN_EXCLUDED',f'it.path!=={const}' in UI or (key=='LINUX24' and "it.path!=='/data/PIZZA_HEN/payloads/ps5-linux-loader.elf'" in UI))
    ck(key+'_NO_AUTOSTART_UI',f"plugin-autostart '+{const}" not in UI)
    ck(key+'_ORIGINAL_NOTIFY_SURFACE',path in MSG)

# Physical top-level removal remains: Remote Play/Linux are SERVICES only; SVT stays retired.
ck('NO_TOPLEVEL_REMOTE_PLAY','<span class="etaItemTitle">Remote Play</span>' not in UI)
ck('NO_TOPLEVEL_LINUX','<span class="etaItemTitle">Linux Loader</span>' not in UI and '<span class="etaItemTitle">PS5 Linux Loader 2.4</span>' not in UI)
ck('NO_TOPLEVEL_SVT','<span class="etaItemTitle">SVT Play</span>' not in UI)
ck('NO_LEGACY_REMOTE_PANEL','id="remoteplay"' not in UI and 'svc_remote_play' not in UI and 'REMOTE_PLAY_PATH' not in UI)
ck('NO_LEGACY_LINUX_ACTION','openLinuxLoader' not in UI and 'LINUX_LOADER_PATH' not in UI)

# All newly supplied payloads are deployed as embedded exact assets; no source rebuild/patch path.
for token in ['unrar_ps5_start','ps_game_state_start','ghostpad_start','ghostcontrol_start','ps_discord_start']:
    ck('DAEMON_'+token.upper(), token in DAEMON)
for path in [x[7] for x in items[:-1]]:
    ck('MAIN_DEPLOY_'+Path(path).name.upper().replace('.','_').replace('-','_'),f'write_blob_file("{path}"' in MAIN)
ck('LINUX_EXISTING_DEPLOY', 'write_blob_file("/data/PIZZA_HEN/payloads/ps5-linux-loader.elf"' in MAIN)

# Manual-only markers are removed at PIZZA startup (data + user/data aliases).
for path in [x[7] for x in items]:
    rel=path.removeprefix('/data/')
    ck('STALE_AUTOSTART_'+Path(path).name.upper().replace('.','_').replace('-','_'),path+'.auto_start' in MAIN and '/user/data/'+rel+'.auto_start' in MAIN)

# Build provenance must verify originals and copy, never compile/patch the six active user-supplied binaries.
for label in ['UNRAR_PS5','PS_GAME_STATE_LIB','GHOSTPAD','GHOSTCONTROL','PS_DISCORD_PRESENCE']:
    ck('BUILD_GATE_'+label,('verify_frozen_elf_only '+label) in BUILD)
ck('LINUX_FROZEN_GATE','verify_frozen_elf_only LINUX_LOADER' in BUILD)
for var in ['UNRAR','PS_GAME_STATE','GHOSTPAD','GHOSTCONTROL','PS_DISCORD']:
    ck('BUILD_COPY_'+var,f'cp -f "${var}_ELF" "${var}_DST"' in BUILD)
ck('BUILD_COPY_LINUX','cp -f "$LINUX_LOADER_ELF" "$LINUX_LOADER_DST"' in BUILD)
ck('NO_NEW_BINARY_PATCHER',not any(x in BUILD for x in ['patch_r72527_elf','rebuild_r72527_service','objcopy_r72527_service']))

# Existing 31-locale architecture is extended using two generic service descriptions.
m=re.search(r'const PH_I18N=(\{.*?\});\nconst PH_BASE_MAP=',UI,re.S)
i18n=json.loads(m.group(1)) if m else {}
ck('I18N_31',len(i18n)==31)
ck('I18N_SERVICE_DESCS_31',all('original_resident_elf_desc' in v and 'original_ondemand_elf_desc' in v for v in i18n.values()))
ck('I18N_ITALIAN',i18n.get('it-IT',{}).get('original_resident_elf_desc','').startswith('ELF residente originale'))
ck('I18N_JAPANESE',bool(i18n.get('ja-JP',{}).get('original_ondemand_elf_desc')))
ck('I18N_ARABIC',bool(i18n.get('ar-SA',{}).get('original_resident_elf_desc')))
ck('BASE_MAP_SERVICE_DESCS','Original resident ELF — PIZZA HEN only starts/stops it; payload functions stay unchanged.' in UI and 'Original on-demand ELF — PIZZA HEN only starts/stops it; payload functions stay unchanged.' in UI)

# Preserve upstream/original startup notification surfaces: success popup is log-only for these exact service paths.
ck('NOTIFY_LOG_ONLY_BLOCK','[PIZZA Services] original ELF started; payload owns its original notification/runtime surface' in MSG)
ck('NOTIFY_ALL_ACTIVE_PATHS',all(x[7] in MSG for x in items))

ck('REMOTE_PLAY_RETIRED', 'Remote_Play.elf' not in UI and 'RP_ORIGINAL_SERVICE' not in UI and 'remote_play_service_start' not in MAIN and 'remote_play_service_start' not in DAEMON)
ck('GARLIC_WORKER_RETIRED', 'garlic-worker_v1.1.6.elf' not in UI and 'GARLIC_WORKER_SERVICE' not in UI and 'garlic_worker_start' not in MAIN and 'garlic_worker_start' not in DAEMON)

ck('BUILD_METADATA',all(x in BUILD for x in [
 'R72527_SERVICE_UI=STANDARD_SERVICES_SWITCHES',
 'R72527_ELF_POLICY=BYTE_EXACT_USER_SUPPLIED_NO_BINARY_PATCHING',
 'R72527_AUTOSTART=NONE_MANUAL_ONLY',
 'R72527_I18N=31_LOCALES']))
ck('BUILD_TEST_HOOK','test_r72527_services_original_elf_integration.py' in BUILD)

print(f"R7_25_2_7_SERVICES_ORIGINAL_ELF_INTEGRATION={total-fail}/{total} {'PASS' if fail==0 else 'FAIL'}")
sys.exit(1 if fail else 0)
