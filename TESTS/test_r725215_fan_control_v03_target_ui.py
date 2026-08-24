#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
ui=(SRC/'bootstrapper/assets/toolbox_launcher.html').read_text(encoding='utf-8')
api=(SRC/'toolbox_api/src/main.c').read_text(encoding='utf-8')
build=(ROOT/'build_v01_rebase_latest_toolbox.sh').read_text(encoding='utf-8')
elf=SRC/'daemon/assets/ps5-fan-control-v0.3.elf'
frozen=ROOT/'ThirdParty/ps5-fan-control-v0.3-USER-SUPPLIED-FROZEN/ps5-fan-control-v0.3.elf'
fail=0
def ck(name, ok):
    global fail
    print(f'R725215_{name}={"PASS" if ok else "FAIL"}')
    if not ok: fail+=1
ck('OPTION2_TARGET_INPUT','id="fan_control_v03_target"' in ui)
ck('OPTION2_TARGET_RANGE','type="number" min="30" max="90" step="1" value="70"' in ui)
ck('OPTION2_TARGET_CHANGE_HANDLER','onchange="applyFanControlV03Target(this,false)"' in ui)
ck('LOAD_ON_PANEL_OPEN','syncFanControlV03Control();loadFanControlV03Target()' in ui)
ck('UI_EXPLAINS_THRESHOLD_NOT_FIXED_SPEED','Non è una percentuale fissa della ventola' in ui)
ck('UI_USB_PRECEDENCE','fan_control.ini presente su USB mantiene la precedenza' in ui)
ck('ACTION_REGISTERED','"fan-control-set-target"' in api)
ck('ACTION_DISPATCH','fan_control_set_target(v)' in api and 'ok:fan-control-set-target' in api)
ck('CONFIG_PATH','#define FAN_CONTROL_CONFIG_FILE "/data/fan_control.ini"' in api)
ck('TARGET_MINMAX_BACKEND','n>=30&&n<=90' in api)
ck('TARGET_KEY_WRITTEN','target_temperature=%s' in api)
ck('CELSIUS_FOR_UI','use_fahrenheit=0' in api)
ck('DEFAULT_ENABLE','fputs("enable=1\\n",out);' in api)
ck('DEFAULT_STATUS','fputs("show_status=0\\n",out);' in api)
ck('DEFAULT_INTERVAL','fputs("interval=7\\n",out);' in api)
ck('DEFAULT_XMB','fputs("xmb_target_temperature=0\\n",out);' in api)
ck('ON_WRITES_TARGET_BEFORE_LAUNCH',ui.find('await applyFanControlV03Target(input,true)') < ui.find("await runAction('plugin-launch '+FAN_CONTROL_V03_PATH"))
ck('LIVE_CHANGE_NO_RESTART',"await runAction('fan-control-set-target '+n)" in ui)
ck('ELF_FROZEN_EXISTS',elf.exists() and frozen.exists())
ck('ELF_BYTE_EXACT',elf.read_bytes()==frozen.read_bytes())
ck('ELF_EXPECTED_SHA256',hashlib.sha256(elf.read_bytes()).hexdigest()=='b10b6b9b9c00efed8bf9202a83b6cb762345d1f84130a419eff7139250026b36')
ck('OPTION1_PATHS_UNCHANGED',"var FAN_TARGET_PATHS={65:'/data/PIZZA_HEN/payloads/fan_target_65c.elf',70:'/data/PIZZA_HEN/payloads/fan_target_70c.elf',75:'/data/PIZZA_HEN/payloads/fan_target_75c.elf',80:'/data/PIZZA_HEN/payloads/fan_target_80c.elf',85:'/data/PIZZA_HEN/payloads/fan_target_85c.elf'};" in ui)
ck('MUTUAL_EXCLUSION_UNCHANGED','await stopAllFanTargets();await runAction' in ui and 'await stopFanControlV03();const temp=sel.value' in ui)
ck('BUILD_TEST_HOOK','test_r725215_fan_control_v03_target_ui.py' in build)
ck('BUILD_METADATA','R725215_FAN_CONTROL_V03_TARGET_UI=TARGET_TEMPERATURE_30_90_C' in build)
print(f'R7_25_2_15_FAN_CONTROL_V03_TARGET_UI={25-fail}/25 {"PASS" if fail==0 else "FAIL"}')
sys.exit(1 if fail else 0)
