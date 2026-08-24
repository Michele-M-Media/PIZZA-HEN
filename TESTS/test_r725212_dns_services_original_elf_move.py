#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, re, sys
ROOT=Path(__file__).resolve().parents[1]
UI=(ROOT/'Source Code/bootstrapper/assets/toolbox_launcher.html').read_text(errors='ignore')
BUILD=(ROOT/'build_v01_rebase_latest_toolbox.sh').read_text(errors='ignore')
MAIN=(ROOT/'Source Code/bootstrapper/source/main.cpp').read_text(errors='ignore')
DAEMON=(ROOT/'Source Code/bootstrapper/source/daemon.c').read_text(errors='ignore')
PM=(ROOT/'Source Code/util/source/PluginManager.cpp').read_text(errors='ignore')
CH=ROOT/'Source Code/bootstrapper/assets/Chukei_DNS_v0.9.0.elf'
NA=ROOT/'Source Code/bootstrapper/assets/nanoDNS_v0.4.elf'
CHF=ROOT/'ThirdParty/Chukei-DNS-v0.9.0-USER-SUPPLIED-FROZEN/Chukei_DNS_v0.9.0.elf'
NAF=ROOT/'ThirdParty/nanoDNS-v0.4-USER-SUPPLIED-FROZEN/nanoDNS_v0.4.elf'
CH_SHA='0cf13e1ed87b57ffa4fdcfca5d9afe1572be29b4f632677cedf17657a972d750'
NA_SHA='18a93655c59ad32e371e14c86f32d14fbd1fbc47a0e907f3e0b6667efb3ad964'
fail=0; total=0
def ck(n,c):
 global fail,total; total+=1; print(f'R725212_{n}={"PASS" if c else "FAIL"}'); fail += 0 if c else 1
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
ck('CHUKEI_EXACT_SHA',CH.is_file() and sha(CH)==CH_SHA)
ck('NANODNS_EXACT_SHA',NA.is_file() and sha(NA)==NA_SHA)
ck('CHUKEI_RUNTIME_EQUALS_FROZEN',CHF.is_file() and CH.read_bytes()==CHF.read_bytes())
ck('NANODNS_RUNTIME_EQUALS_FROZEN',NAF.is_file() and NA.read_bytes()==NAF.read_bytes())
ck('CHANGE_DNS_TOPLEVEL_GONE','Cambia DNS' not in UI and "show('dns')" not in UI)
ck('CHANGE_DNS_PANEL_GONE','<section id="dns"' not in UI)
ck('CHANGE_DNS_FUNCTIONS_GONE','loadDnsTools' not in UI and 'togglePlainDnsPayload' not in UI)
ck('CHANGE_DNS_PAGE_TITLE_GONE',"dns:phText('change_dns')" not in UI)
m=re.search(r'const PH_I18N=(\{.*?\});\nconst PH_BASE_MAP=',UI,re.S)
i18n=json.loads(m.group(1)) if m else {}
ck('I18N_31_PRESERVED',len(i18n)==31)
ck('CHANGE_DNS_I18N_GONE',len(i18n)==31 and all('change_dns' not in v and 'change_dns_desc' not in v for v in i18n.values()))
ck('CHUKEI_STANDARD_SERVICE_ROW',"toggleManagedTaskService(this.checked,this,CHUKEI_DNS_PATH,'Chukei DNS 0.9.0','task_finished')" in UI)
ck('NANODNS_STANDARD_SERVICE_ROW',"toggleManagedTaskService(this.checked,this,NANODNS_PATH,'nanoDNS 0.4','task_finished')" in UI)
ck('CHUKEI_STANDARD_SERVICE_SYNC',"syncManagedTaskControl('svc_chukei_dns',CHUKEI_DNS_PATH)" in UI)
ck('NANODNS_STANDARD_SERVICE_SYNC',"syncManagedTaskControl('svc_nanodns',NANODNS_PATH)" in UI)
ck('GENERIC_HANDLER_ONLY','async function toggleManagedTaskService(on,el,path,title,doneKey)' in UI)
ck('NO_DNS_SPECIAL_PLUGIN_MANAGER','path=="/data/PIZZA_HEN/payloads/Chukei_DNS_v0.9.0.elf"' not in PM and 'path=="/data/PIZZA_HEN/payloads/nanoDNS_v0.4.elf"' not in PM)
ck('EMBED_ORIGINALS','Chukei_DNS_v0.9.0.elf' in DAEMON and 'nanoDNS_v0.4.elf' in DAEMON)
ck('DEPLOY_ORIGINALS','write_blob_file("/data/PIZZA_HEN/payloads/Chukei_DNS_v0.9.0.elf"' in MAIN and 'write_blob_file("/data/PIZZA_HEN/payloads/nanoDNS_v0.4.elf"' in MAIN)
ck('BUILD_FROZEN_VERIFY','verify_frozen_elf_only CHUKEI_DNS' in BUILD and 'verify_frozen_elf_only NANODNS' in BUILD)
ck('BUILD_EXACT_COPY','cp -f "$CHUKEI_DNS_ELF" "$CHUKEI_DNS_DST"' in BUILD and 'cp -f "$NANODNS_ELF" "$NANODNS_DST"' in BUILD)
ck('NO_DNS_AUTOSTART',"plugin-autostart '+CHUKEI_DNS_PATH" not in UI and "plugin-autostart '+NANODNS_PATH" not in UI)
ck('PLUGIN_CATALOG_FILTERED','it.path!==CHUKEI_DNS_PATH' in UI and 'it.path!==NANODNS_PATH' in UI)
ck('METADATA','R725212_DNS_UI=DEDICATED_CHANGE_DNS_SCREEN_REMOVED' in BUILD and 'R725212_DNS_CONTROL=STANDARD_SERVICES_TOGGLE_MANAGED_TASK' in BUILD and 'R725212_DNS_ELFS=RECOPIED_FROM_CURRENT_USER_UPLOADS_BYTE_EXACT' in BUILD)
print(f'R7_25_2_12_DNS_SERVICES_ORIGINAL_ELF_MOVE={total-fail}/{total} {"PASS" if fail==0 else "FAIL"}')
sys.exit(1 if fail else 0)
