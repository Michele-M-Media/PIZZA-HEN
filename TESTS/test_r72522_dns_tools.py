#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, re, sys

ROOT = Path(__file__).resolve().parents[1]
UI = (ROOT / "Source Code/bootstrapper/assets/toolbox_launcher.html").read_text(errors="ignore")
MAIN = (ROOT / "Source Code/bootstrapper/source/main.cpp").read_text(errors="ignore")
DAEMON = (ROOT / "Source Code/bootstrapper/source/daemon.c").read_text(errors="ignore")
BUILD = (ROOT / "build_v01_rebase_latest_toolbox.sh").read_text(errors="ignore")

fail = 0
def ck(name, cond):
    global fail
    print(f"R72522_{name}={'PASS' if cond else 'FAIL'}")
    if not cond: fail += 1

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

ch_f = ROOT / "ThirdParty/Chukei-DNS-v0.9.0-USER-SUPPLIED-FROZEN/Chukei_DNS_v0.9.0.elf"
na_f = ROOT / "ThirdParty/nanoDNS-v0.4-USER-SUPPLIED-FROZEN/nanoDNS_v0.4.elf"
ch_a = ROOT / "Source Code/bootstrapper/assets/Chukei_DNS_v0.9.0.elf"
na_a = ROOT / "Source Code/bootstrapper/assets/nanoDNS_v0.4.elf"

ck("CHUKEI_FROZEN_SHA", ch_f.is_file() and sha(ch_f) == "0cf13e1ed87b57ffa4fdcfca5d9afe1572be29b4f632677cedf17657a972d750")
ck("NANODNS_FROZEN_SHA", na_f.is_file() and sha(na_f) == "18a93655c59ad32e371e14c86f32d14fbd1fbc47a0e907f3e0b6667efb3ad964")
ck("CHUKEI_ASSET_BYTE_EXACT", ch_a.is_file() and ch_a.read_bytes() == ch_f.read_bytes())
ck("NANODNS_ASSET_BYTE_EXACT", na_a.is_file() and na_a.read_bytes() == na_f.read_bytes())

ck("TOOLBOX_ITEM_SUPERSEDED", "show('dns')" not in UI and '<span class="etaItemTitle">Cambia DNS</span>' not in UI)
ck("DNS_PANEL_SUPERSEDED", '<section id="dns"' not in UI)
ck("CHUKEI_SWITCH", "toggleManagedTaskService(this.checked,this,CHUKEI_DNS_PATH,'Chukei DNS 0.9.0','task_finished')" in UI)
ck("NANODNS_SWITCH", "toggleManagedTaskService(this.checked,this,NANODNS_PATH,'nanoDNS 0.4','task_finished')" in UI)
ck("DNS_PATHS", "/data/PIZZA_HEN/payloads/Chukei_DNS_v0.9.0.elf" in UI and "/data/PIZZA_HEN/payloads/nanoDNS_v0.4.elf" in UI)
ck("SERVICES_SYNC", "syncManagedTaskControl('svc_chukei_dns',CHUKEI_DNS_PATH)" in UI and "syncManagedTaskControl('svc_nanodns',NANODNS_PATH)" in UI)
ck("PLUGIN_CATALOG_NO_DUPLICATES", "it.path!==CHUKEI_DNS_PATH" in UI and "it.path!==NANODNS_PATH" in UI)
ck("R72523_REMOVAL_PRESERVED", '<span class=\"etaItemTitle\">Remote Play</span>' not in UI and '<span class=\"etaItemTitle\">Linux Loader</span>' not in UI and '<span class=\"etaItemTitle\">SVT Play</span>' not in UI)

m = re.search(r"const PH_I18N=(\{.*?\});\nconst PH_BASE_MAP=", UI, re.S)
i18n = json.loads(m.group(1)) if m else {}
ck("I18N_31", len(i18n) == 31)
ck("CHANGE_DNS_I18N_RETIRED", all("change_dns" not in v and "change_dns_desc" not in v for v in i18n.values()))
ck("SERVICES_I18N_PRESERVED", all("services" in v and "services_hint" in v for v in i18n.values()))
ck("ORIGINAL_SERVICE_DESC_I18N", all("original_resident_elf_desc" in v for v in i18n.values()))

ck("MAIN_DEPLOY", "chukei_dns_start" in MAIN and 'write_blob_file("/data/PIZZA_HEN/payloads/Chukei_DNS_v0.9.0.elf"' in MAIN and "nanodns_start" in MAIN and 'write_blob_file("/data/PIZZA_HEN/payloads/nanoDNS_v0.4.elf"' in MAIN)
ck("DAEMON_INCBIN", '.incbin \\"../../../bootstrapper/assets/Chukei_DNS_v0.9.0.elf\\"' in DAEMON and '.incbin \\"../../../bootstrapper/assets/nanoDNS_v0.4.elf\\"' in DAEMON)
ck("BUILD_FROZEN_GATES", 'verify_frozen_elf_only CHUKEI_DNS' in BUILD and 'verify_frozen_elf_only NANODNS' in BUILD)
ck("BUILD_EXACT_COPY", 'cp -f "$CHUKEI_DNS_ELF" "$CHUKEI_DNS_DST"' in BUILD and 'cp -f "$NANODNS_ELF" "$NANODNS_DST"' in BUILD)
ck("NO_AUTOSTART_DNS", "plugin-autostart '+CHUKEI_DNS_PATH" not in UI and "plugin-autostart '+NANODNS_PATH" not in UI)
ck("BUILD_METADATA", "R72522_DNS_ELFS=BYTE_EXACT_USER_SUPPLIED" in BUILD and "R72522_DNS_I18N=31_LOCALES" in BUILD)

print(f"R7_25_2_2_DNS_TOOLS={22-fail}/22 {'PASS' if fail == 0 else 'FAIL'}")
sys.exit(1 if fail else 0)
