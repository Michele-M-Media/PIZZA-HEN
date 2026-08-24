#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
ui=(SRC/'bootstrapper/assets/toolbox_launcher.html').read_text()
api=(SRC/'toolbox_api/src/main.c').read_text()
build=(ROOT/'build_v01_rebase_latest_toolbox.sh').read_text()
checks=[]
def ck(n,c):
 print(f"R7152_{n}={'PASS' if c else 'FAIL'}"); checks.append(bool(c))
ck('STATUS_ACTION_DECLARED', '"elfldr-status"' in api and 'ok:elfldr-status' in api and 'fail:elfldr-status' in api)
ck('LOOPBACK_PROBE', 'elfldr024_port_ready' in api and 'htonl(INADDR_LOOPBACK)' in api and 'htons(9021)' in api and 'connect(fd,(struct sockaddr*)&sa,sizeof(sa))' in api)
ck('UI_PORT_STATE', 'async function elfldr024PortReady()' in ui and "apiLaunch('elfldr-status',tx)" in ui)
ck('POLL_STABILIZATION', 'async function waitElfldr024State(want)' in ui and 'for(let i=0;i<24;i++)' in ui and 'setTimeout(r,250)' in ui)
ck('SYNC_USES_PORT', 'async function syncElfldrControl()' in ui and 'el.checked=await elfldr024PortReady()' in ui)
ck('NO_CATALOG_STATE_FOR_ELFLDR', "items[i].path===ELFLDR024_PATH" not in ui)
ck('ON_REAL_START', "if(on)await runAction('elfldr-start')" in ui)
ck('OFF_REAL_STOP', "plugin-stop '+ELFLDR024_PATH+' elfldr-ps5-v0.24-148b71c.elf payload" in ui)
ck('NO_FORCED_ON_R7181_I18N', "if(!(await waitElfldr024State(on)))throw new Error(phText('tcp_state_mismatch')+' — TCP 9021')" in ui and 'el.checked=on' in ui)
ck('BUILD_GATE', 'test_r7152_elfldr_port_state_repair.py' in build)
ck('BUILD_METADATA', 'R7152_ELFLDR_STATE=TCP_127_0_0_1_9021' in build and 'R7152_ELFLDR_STABILIZATION=POLL_24X250MS' in build)
print(f"R7_15_2_ELFLDR_PORT_STATE_REPAIR={sum(checks)}/{len(checks)} {'PASS' if all(checks) else 'FAIL'}")
sys.exit(0 if all(checks) else 1)
