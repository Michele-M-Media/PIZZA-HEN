#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys
ROOT=Path(__file__).resolve().parents[1]
UI=(ROOT/'Source Code/bootstrapper/assets/toolbox_launcher.html').read_text(errors='ignore')
MSG=(ROOT/'Source Code/util/source/msg.cpp').read_text(errors='ignore')
PM=(ROOT/'Source Code/util/source/PluginManager.cpp').read_text(errors='ignore')
BUILD=(ROOT/'build_v01_rebase_latest_toolbox.sh').read_text(errors='ignore')
MAIN=(ROOT/'Source Code/bootstrapper/source/main.cpp').read_text(errors='ignore')
DAEMON=(ROOT/'Source Code/bootstrapper/source/daemon.c').read_text(errors='ignore')
CH=ROOT/'Source Code/bootstrapper/assets/Chukei_DNS_v0.9.0.elf'; NA=ROOT/'Source Code/bootstrapper/assets/nanoDNS_v0.4.elf'
CHF=ROOT/'ThirdParty/Chukei-DNS-v0.9.0-USER-SUPPLIED-FROZEN/Chukei_DNS_v0.9.0.elf'; NAF=ROOT/'ThirdParty/nanoDNS-v0.4-USER-SUPPLIED-FROZEN/nanoDNS_v0.4.elf'
fail=0; total=0
def ck(n,c):
 global fail,total; total+=1; print(f'R725211_{n}={"PASS" if c else "FAIL"}'); fail += 0 if c else 1
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
ck('CHUKEI_ORIGINAL_SHA',CH.is_file() and sha(CH)=='0cf13e1ed87b57ffa4fdcfca5d9afe1572be29b4f632677cedf17657a972d750')
ck('NANODNS_ORIGINAL_SHA',NA.is_file() and sha(NA)=='18a93655c59ad32e371e14c86f32d14fbd1fbc47a0e907f3e0b6667efb3ad964')
ck('CHUKEI_RUNTIME_EQUALS_FROZEN',CHF.is_file() and CH.read_bytes()==CHF.read_bytes())
ck('NANODNS_RUNTIME_EQUALS_FROZEN',NAF.is_file() and NA.read_bytes()==NAF.read_bytes())
ck('TWO_SEPARATE_SWITCHES',"toggleManagedTaskService(this.checked,this,CHUKEI_DNS_PATH,'Chukei DNS 0.9.0','task_finished')" in UI and "toggleManagedTaskService(this.checked,this,NANODNS_PATH,'nanoDNS 0.4','task_finished')" in UI)
ck('NO_CROSS_PAYLOAD_ARGUMENTS','toggleDnsService(' not in UI and 'otherPath' not in UI and 'otherId' not in UI)
ck('PLAIN_START_STOP',"async function togglePlainDnsPayload(on,el,path,title)" not in UI and "async function toggleManagedTaskService(on,el,path,title,doneKey)" in UI and "runAction('plugin-launch '+path" in UI and "runAction('plugin-stop '+path" in UI)
ck('INDEPENDENT_STATUS',"syncManagedTaskControl('svc_chukei_dns',CHUKEI_DNS_PATH)" in UI and "syncManagedTaskControl('svc_nanodns',NANODNS_PATH)" in UI)
ck('NO_DNS_SPECIAL_STOP','path=="/data/PIZZA_HEN/payloads/Chukei_DNS_v0.9.0.elf"' not in PM and 'path=="/data/PIZZA_HEN/payloads/nanoDNS_v0.4.elf"' not in PM)
ck('GENERIC_SUCCESS_NOTIFY_ACTIVE','Plugin or ELF launched successfully' in MSG and '[PIZZA DNS]' not in MSG)
ck('DNS_FAILURE_NOTIFY','Chukei DNS 0.9.0 — %s' in MSG and 'nanoDNS 0.4 — %s' in MSG)
ck('DNS_STOP_NOTIFY','strcmp(p, "/data/PIZZA_HEN/payloads/Chukei_DNS_v0.9.0.elf")' in MSG and 'strcmp(p, "/data/PIZZA_HEN/payloads/nanoDNS_v0.4.elf")' in MSG)
ck('EMBED_EXACT_FILES','Chukei_DNS_v0.9.0.elf' in DAEMON and 'nanoDNS_v0.4.elf' in DAEMON)
ck('DEPLOY_SEPARATE_FILES','write_blob_file("/data/PIZZA_HEN/payloads/Chukei_DNS_v0.9.0.elf"' in MAIN and 'write_blob_file("/data/PIZZA_HEN/payloads/nanoDNS_v0.4.elf"' in MAIN)
ck('BUILD_COPIES_FROZEN_ORIGINALS','cp -f "$CHUKEI_DNS_ELF" "$CHUKEI_DNS_DST"' in BUILD and 'cp -f "$NANODNS_ELF" "$NANODNS_DST"' in BUILD)
ck('NO_AUTOSTART',"plugin-autostart '+CHUKEI_DNS_PATH" not in UI and "plugin-autostart '+NANODNS_PATH" not in UI)
ck('METADATA','R725211_DNS_MODE=SUPERSEDED_BY_R725212_SERVICES' in BUILD and 'R725211_DNS_ELFS=ORIGINAL_USER_SUPPLIED_BYTE_EXACT' in BUILD and 'R725211_DNS_CROSS_CONTROL=NONE' in BUILD)
print(f'R7_25_2_11_DNS_PLAIN_SEPARATE_PAYLOADS={total-fail}/{total} {"PASS" if fail==0 else "FAIL"}')
sys.exit(1 if fail else 0)
