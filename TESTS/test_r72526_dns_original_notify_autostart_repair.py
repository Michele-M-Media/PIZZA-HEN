#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys
ROOT=Path(__file__).resolve().parents[1]
UI=(ROOT/'Source Code/bootstrapper/assets/toolbox_launcher.html').read_text(errors='ignore')
MSG=(ROOT/'Source Code/util/source/msg.cpp').read_text(errors='ignore')
BOOT=(ROOT/'Source Code/bootstrapper/source/main.cpp').read_text(errors='ignore')
PM=(ROOT/'Source Code/util/source/PluginManager.cpp').read_text(errors='ignore')
CH=ROOT/'Source Code/bootstrapper/assets/Chukei_DNS_v0.9.0.elf'
NA=ROOT/'Source Code/bootstrapper/assets/nanoDNS_v0.4.elf'
CHF=ROOT/'ThirdParty/Chukei-DNS-v0.9.0-USER-SUPPLIED-FROZEN/Chukei_DNS_v0.9.0.elf'
NAF=ROOT/'ThirdParty/nanoDNS-v0.4-USER-SUPPLIED-FROZEN/nanoDNS_v0.4.elf'
CH_SHA='0cf13e1ed87b57ffa4fdcfca5d9afe1572be29b4f632677cedf17657a972d750'
NA_SHA='18a93655c59ad32e371e14c86f32d14fbd1fbc47a0e907f3e0b6667efb3ad964'
fail=0
total=0
def ck(n,c):
 global fail,total
 total += 1
 print(f'R72526_{n}={"PASS" if c else "FAIL"}')
 fail += 0 if c else 1
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
ck('CHUKEI_RUNTIME_ORIGINAL_SHA',CH.is_file() and sha(CH)==CH_SHA)
ck('NANODNS_RUNTIME_ORIGINAL_SHA',NA.is_file() and sha(NA)==NA_SHA)
ck('CHUKEI_FROZEN_EQUALS_RUNTIME',CHF.is_file() and CHF.read_bytes()==CH.read_bytes())
ck('NANODNS_FROZEN_EQUALS_RUNTIME',NAF.is_file() and NAF.read_bytes()==NA.read_bytes())
ck('DNS_GENERIC_SUCCESS_RESTORED','[PIZZA DNS] Chukei DNS original ELF started' not in MSG and '[PIZZA DNS] nanoDNS original ELF started' not in MSG and 'Plugin or ELF launched successfully' in MSG)
ck('DNS_FAILURE_NOTIFICATIONS','Chukei DNS 0.9.0 — %s' in MSG and 'nanoDNS 0.4 — %s' in MSG)
ck('DNS_STOP_NOTIFICATIONS','Chukei DNS 0.9.0 — %s' in MSG and 'nanoDNS 0.4 — %s' in MSG)
ck('DNS_STANDARD_STOP','path=="/data/PIZZA_HEN/payloads/Chukei_DNS_v0.9.0.elf"' not in PM and 'path=="/data/PIZZA_HEN/payloads/nanoDNS_v0.4.elf"' not in PM)
for name in ['rp-get-pin.elf','ps5-linux-loader.elf','svtplay_v0.2.elf','ProsperoPlayer_v1.0.elf','PS-Play_v2.1.elf','BFplayer-standalone_v0.1.0-alpha.44.elf']:
 ck('CLEAR_'+name.upper().replace('.','_').replace('-','_'), f'/data/PIZZA_HEN/payloads/{name}.auto_start' in BOOT)
ck('AUTOSTART_CLEANUP_BEFORE_SCAN',BOOT.find('manual_only_autostart_markers') < BOOT.find('char **find_plugin_files()'))
ck('REMOTE_PLAY_TOOLBOX_STILL_REMOVED','<span class="etaItemTitle">Remote Play</span>' not in UI and "show('remoteplay')" not in UI)
ck('LINUX_TOOLBOX_STILL_REMOVED','>Linux Loader<' not in UI and 'openLinuxLoader(this)' not in UI)
ck('SVT_TOOLBOX_STILL_REMOVED','>SVT Play<' not in UI and "show('svtplay')" not in UI)
ck('DNS_SERVICES_PRESENT','Cambia DNS' not in UI and '<section id="dns"' not in UI and 'svc_chukei_dns' in UI and 'svc_nanodns' in UI)
ck('THEMES_AVATAR_PRESERVED','Themes Avatar' in UI and 'PS5 Custom Tool Manager' in UI and 'PS5 Wallpaper Modder' in UI)
print(f'R7_25_2_6_DNS_ORIGINAL_NOTIFY_AUTOSTART_REPAIR={total-fail}/{total} {"PASS" if fail==0 else "FAIL"}')
sys.exit(1 if fail else 0)
