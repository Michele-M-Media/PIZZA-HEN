#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys
ROOT=Path(__file__).resolve().parents[1]
UI=(ROOT/'Source Code/bootstrapper/assets/toolbox_launcher.html').read_text(errors='ignore')
PM=(ROOT/'Source Code/util/source/PluginManager.cpp').read_text(errors='ignore')
BUILD=(ROOT/'build_v01_rebase_latest_toolbox.sh').read_text(errors='ignore')
CH=ROOT/'Source Code/bootstrapper/assets/Chukei_DNS_v0.9.0.elf'; NA=ROOT/'Source Code/bootstrapper/assets/nanoDNS_v0.4.elf'
CHF=ROOT/'ThirdParty/Chukei-DNS-v0.9.0-USER-SUPPLIED-FROZEN/Chukei_DNS_v0.9.0.elf'; NAF=ROOT/'ThirdParty/nanoDNS-v0.4-USER-SUPPLIED-FROZEN/nanoDNS_v0.4.elf'
fail=0
def ck(n,c):
 global fail; print(f'R72524_{n}={"PASS" if c else "FAIL"}'); fail += 0 if c else 1
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
ck('CHUKEI_FROZEN_SHA',CHF.is_file() and sha(CHF)=='0cf13e1ed87b57ffa4fdcfca5d9afe1572be29b4f632677cedf17657a972d750')
ck('NANODNS_FROZEN_SHA',NAF.is_file() and sha(NAF)=='18a93655c59ad32e371e14c86f32d14fbd1fbc47a0e907f3e0b6667efb3ad964')
ck('CHUKEI_BYTE_EXACT',CH.is_file() and CH.read_bytes()==CHF.read_bytes())
ck('NANODNS_BYTE_EXACT',NA.is_file() and NA.read_bytes()==NAF.read_bytes())
ck('CHUKEI_PLAIN_SWITCH',"toggleManagedTaskService(this.checked,this,CHUKEI_DNS_PATH,'Chukei DNS 0.9.0','task_finished')" in UI)
ck('NANODNS_PLAIN_SWITCH',"toggleManagedTaskService(this.checked,this,NANODNS_PATH,'nanoDNS 0.4','task_finished')" in UI)
ck('OLD_DEDICATED_SWITCH_GONE','toggleDnsService(' not in UI)
ck('NO_MUTUAL_EXCLUSION','otherPath' not in UI and 'otherId' not in UI)
ck('INDEPENDENT_STATE_SYNC',"syncManagedTaskControl('svc_chukei_dns',CHUKEI_DNS_PATH)" in UI and "syncManagedTaskControl('svc_nanodns',NANODNS_PATH)" in UI)
ck('STANDARD_START','plugin-launch '+"'+path+'" in UI)
ck('STANDARD_STOP','plugin-stop '+"'+path+'" in UI)
ck('NO_DNS_GRACEFUL_SPECIAL','path=="/data/PIZZA_HEN/payloads/Chukei_DNS_v0.9.0.elf"' not in PM and 'path=="/data/PIZZA_HEN/payloads/nanoDNS_v0.4.elf"' not in PM)
ck('NO_DNS_AUTOSTART',"plugin-autostart '+CHUKEI_DNS_PATH" not in UI and "plugin-autostart '+NANODNS_PATH" not in UI)
ck('TOOLBOX_REMOVALS_PRESERVED','<span class="etaItemTitle">Remote Play</span>' not in UI and '<span class="etaItemTitle">Linux Loader</span>' not in UI and '<span class="etaItemTitle">SVT Play</span>' not in UI)
ck('DNS_SCREEN_I18N_RETIRED','"change_dns"' not in UI and '"change_dns_desc"' not in UI)
ck('BUILD_BYTE_EXACT_POLICY','R72522_DNS_ELFS=BYTE_EXACT_USER_SUPPLIED' in BUILD)
ck('OLD_CONTROL_EXPLICITLY_SUPERSEDED','R72524_DNS_CONTROL=SUPERSEDED_BY_R725212_STANDARD_SERVICES_SWITCHES' in BUILD)
ck('OLD_EXCLUSION_EXPLICITLY_SUPERSEDED','R72524_DNS_MUTUAL_EXCLUSION=SUPERSEDED_NO_CROSS_PAYLOAD_CONTROL' in BUILD)
ck('OLD_STOP_EXPLICITLY_SUPERSEDED','R72524_DNS_STOP=SUPERSEDED_STANDARD_PAYLOAD_STOP' in BUILD)
print(f'R7_25_2_4_DNS_SERVICE_LIFECYCLE_REPAIR={19-fail}/19 {"PASS" if fail==0 else "FAIL"}')
sys.exit(1 if fail else 0)
