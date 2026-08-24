#!/usr/bin/env python3
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]
UI=(ROOT/'Source Code/bootstrapper/assets/toolbox_launcher.html').read_text(encoding='utf-8')
README=(ROOT/'ThirdParty/websrv-0.34-UPSTREAM-FROZEN/README.md').read_text(encoding='utf-8')
BUILD=(ROOT/'build_v01_rebase_latest_toolbox.sh').read_text(encoding='utf-8')
checks=[]
def ck(name, ok):
    checks.append((name,bool(ok))); print(f"R716_{name}={'PASS' if ok else 'FAIL'}")
ck('UPSTREAM_INDEX_ROUTE', 'http://ps5:8080/index.html - Launch Homebrew' in README)
ck('UPSTREAM_BROWSER_OR_LAUNCHER', 'either install the [Launcher PKG][launcher]' in README and 'or point your browser' in README)
ck('UPSTREAM_DATA_HOME_ROOT', '/data/homebrew' in README)
ck('UPSTREAM_USB_HOME_ROOTS', '/mnt/usb%d/homebrew' in README and '/mnt/ext%d/homebrew' in README)
ck('TOPLEVEL_ENTRY', '>Homebrew Channel<' in UI and 'openHomebrewChannel(this)' in UI)
ck('SAME_ORIGIN_INDEX', "const HOMEBREW_CHANNEL_URL='/index.html';" in UI and 'location.href=HOMEBREW_CHANNEL_URL' in UI)
ck('WEBSRV_PREFLIGHT', "fetch(HOMEBREW_CHANNEL_URL,{cache:'no-store'})" in UI)
# PIZZA HEN still uses the direct /index.html browser transport; launcher installation is not manually dispatched by this handler.
m=re.search(r"async function openHomebrewChannel\(el\)\{.*?\}\n(?=const )", UI, re.S)
handler=m.group(0) if m else ''
ck('NO_DIRECT_PKG_DISPATCH', bool(handler) and '.pkg' not in handler.lower() and 'IV9999-FAKE00000' not in handler)
ck('NO_NEW_PAYLOAD', 'launchElfDirect' not in handler and '/hbldr?' not in handler)
ck('BUILD_GATE', 'test_r716_homebrew_channel.py' in BUILD)
ck('BUILD_METADATA', 'R716_HOMEBREW_CHANNEL=WEBSRV_0_34_INDEX_HTML_DIRECT_BROWSER' in BUILD and 'R716_HOMEBREW_CHANNEL_LAUNCHER=DISABLED_IN_PIZZA_INTEGRATED_WEBSRV' in BUILD and 'R716_HOMEBREW_CHANNEL_URL=/index.html' in BUILD)
passed=sum(x for _,x in checks)
print(f'R7_16_HOMEBREW_CHANNEL={passed}/{len(checks)} PASS' if passed==len(checks) else f'R7_16_HOMEBREW_CHANNEL={passed}/{len(checks)} FAIL')
sys.exit(0 if passed==len(checks) else 1)
