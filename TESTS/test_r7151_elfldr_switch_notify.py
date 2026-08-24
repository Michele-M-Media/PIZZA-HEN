#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
ui=(SRC/'bootstrapper/assets/toolbox_launcher.html').read_text()
msg=(SRC/'util/source/msg.cpp').read_text()
build=(ROOT/'build_v01_rebase_latest_toolbox.sh').read_text()
checks=[]
def ck(n,c):
 print(f"R7151_{n}={'PASS' if c else 'FAIL'}"); checks.append(bool(c))
ck('UI_SWITCH', 'id="svc_elfldr024"' in ui and 'toggleElfldrService(this.checked,this)' in ui and 'startElfldrService' not in ui)
ck('SYNC_STATE_R7152_INTENTIONAL_DELTA', 'syncElfldrControl()' in ui and 'elfldr024PortReady()' in ui)
ck('ON_ACTION', "if(on)await runAction('elfldr-start')" in ui)
ck('OFF_ACTION', "plugin-stop '+ELFLDR024_PATH+' elfldr-ps5-v0.24-148b71c.elf payload" in ui)
ck('DEPLOY_PATH', '/data/PIZZA_HEN/payloads/elfldr-ps5-v0.24-148b71c.elf' in msg)
ck('PID_TRACKED_LAUNCH', 'load_plugin(elfldr_path)' in msg and 'elfldr_spawn("/", STDOUT_FILENO, elfldr_start' not in msg)
ck('START_NOTIFY_R7181_I18N', 'ELF Loader 0.24 — %s\\nIP: %s • TCP 9021' in msg and 'nt->started' in msg)
ck('STOP_NOTIFY_R7181_I18N', 'ELF Loader 0.24 — %s' in msg and 'nt->stopped' in msg)
ck('BUILD_METADATA', 'R7151_ELFLDR_UI=SWITCH_ON_OFF' in build and 'R7151_ELFLDR_NOTIFY=START_STOP_PIZZA_HEN_NOTIFICATION' in build)
print(f"R7_15_1_ELFLDR_SWITCH_NOTIFY={sum(checks)}/{len(checks)} {'PASS' if all(checks) else 'FAIL'}")
sys.exit(0 if all(checks) else 1)
