#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
fail=0
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ck(n,c):
 global fail
 print(f'R725214_{n}={"PASS" if c else "FAIL"}')
 if not c: fail+=1
html=(SRC/'bootstrapper/assets/toolbox_launcher.html').read_text(errors='ignore')
embed=(SRC/'daemon/source/embeddded_payloads.c').read_text(errors='ignore')
daemon=(SRC/'daemon/source/main.cpp').read_text(errors='ignore')
msg=(SRC/'util/source/msg.cpp').read_text(errors='ignore')
build=(ROOT/'build_v01_rebase_latest_toolbox.sh').read_text(errors='ignore')
frozen=ROOT/'ThirdParty/ps5-fan-control-v0.3-USER-SUPPLIED-FROZEN'
elf=frozen/'ps5-fan-control-v0.3.elf'
dst=SRC/'daemon/assets/ps5-fan-control-v0.3.elf'
ini=frozen/'fan_control.ini'
source=frozen/'ps5-fan-control-0.3.zip'
ck('OPTION1_LABEL','Opzione 1 — fan_target 0.1' in html)
ck('OPTION2_LABEL','Opzione 2 — ps5-fan-control v0.3' in html)
ck('OPTION2_SWITCH','id="svc_fan_control_v03"' in html and 'toggleFanControlV03' in html)
ck('OPTION2_RUNTIME_PATH',"/data/PIZZA_HEN/payloads/ps5-fan-control-v0.3.elf" in html)
ck('OPTION2_USB_CONFIG','/mnt/usb0…usb7/fan_control.ini' in html and '/data/fan_control.ini' in html)
ck('OPTION2_DEFAULT_70','senza config usa 70 °C' in html)
ck('MUTUAL_EXCLUSION_NEW_STOPS_OLD','await stopAllFanTargets();await runAction(\'plugin-launch \'+FAN_CONTROL_V03_PATH' in html)
ck('MUTUAL_EXCLUSION_OLD_STOPS_NEW','if(on){await stopFanControlV03();const temp=sel.value' in html)
ck('ELF_FROZEN_SHA',sha(elf)=='b10b6b9b9c00efed8bf9202a83b6cb762345d1f84130a419eff7139250026b36')
ck('ELF_RUNTIME_ASSET_SHA',sha(dst)==sha(elf))
ck('SOURCE_ZIP_SHA',sha(source)=='c85639057b5218445f3f5526c49b3df334d5f5ab99bbdfe8c4c9bf957b89e2e6')
ck('INI_SHA',sha(ini)=='71496515fde36be968623c7cda317b0ebd142c83c06343836ae2274184e9b266')
ck('INI_TEMPLATE_BYTE_EXACT',sha(ROOT/'CONFIG_TEMPLATES/fan_control_v0.3.ini')==sha(ini))
ck('EMBED_EXACT_ASSET','pizzahen_fan_control_v03_start' in embed and 'ps5-fan-control-v0.3.elf' in embed)
ck('DAEMON_DEPLOY','pizzahen_fan_control_v03_start' in daemon and '/data/PIZZA_HEN/payloads/ps5-fan-control-v0.3.elf' in daemon)
ck('UPSTREAM_NOTIFY_OWNED','ps5-fan-control-v0.3.elf' in msg and 'payload owns its original notification/runtime surface' in msg)
ck('NO_AUTOSTART_MARKER','ps5-fan-control-v0.3.elf.auto_start' not in html+daemon+msg)
fan_expected={
'fan_target_65c.elf':'0bedeb564947530d09d1dfb27df63c2a09eaa7f51faf3ddcc90b3fb2870e6312',
'fan_target_70c.elf':'a9ad8502123799d58f8ddd9882d842f524c4ecc3ea6743a73c6dcdffd0bf30e0',
'fan_target_75c.elf':'4b52e09c48ebed1f369221c290e8ec4a9fdb2a477b7b7f44a1b8646958d9f69b',
'fan_target_80c.elf':'ccf2e709218f31cd9e6a0705c99646b8f030b877687df8377982a2f6ca10216e',
'fan_target_85c.elf':'c37019c351c1c5b05b43adbac29d85bfd25f8c0ab9d94371cacab1945d8e0fd0'}
ck('OPTION1_FIVE_ELFS_UNCHANGED',all(sha(SRC/'daemon/assets'/n)==h for n,h in fan_expected.items()))
ck('DEBUG_SERVICES_FROZEN',sha(SRC/'bootstrapper/assets/debug_services_launcher.html')=='7f7134593eefa9628bc581eebe3a7fc66f40cba3bb8f9447ebd641bfe58eb399')
ck('BUILD_HOOK','test_r725214_fan_target_dual_option.py' in build)
ck('BUILD_VERIFY','verify_frozen_elf_source PS5_FAN_CONTROL_V03' in build and 'FAN03_INI_EXPECTED_SHA' in build)
ck('BUILD_METADATA','R725214_FAN_TARGET_OPTION2=PS5_FAN_CONTROL_V0.3_ORIGINAL_ELF' in build)
print(f'R7_25_2_14_FAN_TARGET_DUAL_OPTION={22-fail}/22 {"PASS" if fail==0 else "FAIL"}')
sys.exit(1 if fail else 0)
