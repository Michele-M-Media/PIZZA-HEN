#!/usr/bin/env python3
from pathlib import Path
import hashlib, re
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
checks=[]
def ck(n,c):
    c=bool(c); checks.append(c); print(f'{n}=' + ('PASS' if c else 'FAIL'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
base=ROOT/'ThirdParty/kstuff-1.6.7-BASE-USER-SUPPLIED-FROZEN/kstuff-base-1.6.7.elf'
basezip=ROOT/'ThirdParty/kstuff-1.6.7-BASE-USER-SUPPLIED-FROZEN/kstuff-1.6.7.zip'
kh=(SRC/'bootstrapper/assets/kstuff_selector.html').read_text()
kjs=(SRC/'bootstrapper/assets/kstuff_selector.js').read_text()
ka=(SRC/'selector_action/src/main.c').read_text()
sh=(SRC/'bootstrapper/assets/shadowmount_selector.html').read_text()
sa=(SRC/'shadow_selector_action/src/main.c').read_text()
main=(SRC/'bootstrapper/source/main.cpp').read_text()
daemon=(SRC/'bootstrapper/source/daemon.c').read_text()
build=(ROOT/'build_v01_rebase_latest_toolbox.sh').read_text()
ck('R718_KSTUFF_BASE_ELF_SHA', base.exists() and sha(base)=='f1c1f4b2b6395644af04cbe9828aba58586acf7aacb9e01113cac92ce16e3569')
ck('R718_KSTUFF_BASE_SOURCE_SHA', basezip.exists() and sha(basezip)=='9319f790b2be45e1de3e201a008f0f9a8ad9c2f3dac268c55bb82691daa6bbe4')
ck('R718_KSTUFF_BASE_VERSION', b'Welcome To Kstuff 1.6.7' in base.read_bytes())
ck('R718_KSTUFF_BASE_SELECTOR_HTML', "chooseEngine('base')" in kh and 'KStuff 1.6.7' in kh and '3.xx' in kh and '10.01' in kh)
ck('R718_KSTUFF_BASE_SELECTOR_JS', 'args: ["base"]' in kjs and 'KStuff 1.6.7' in kjs)
ck('R718_KSTUFF_ACTION_BASE', '"base"' in ka)
ck('R718_KSTUFF_BASE_EMBED', 'kstuff_base_start' in daemon and 'kstuff-base-1.6.7.elf' in daemon)
ck('R718_KSTUFF_BASE_RUNTIME', 'chosen = kstuff_base_start' in main and 'chosen_name = "kstuff-base-1.6.7"' in main)
ck('R718_KSTUFF_BASE_DEPLOY', '/data/PIZZA_HEN/engines/kstuff-base-1.6.7.elf' in main)
ck('R718_SHADOW_SKIP_BUTTON', "chooseShadow('skip')" in sh and 'Do not launch ShadowMountPlus' in sh and 'dump_installer' in sh)
ck('R718_SHADOW_ACTION_SKIP', '"skip"' in sa)
ck('R718_SHADOW_RUNTIME_SKIP', 'ShadowMountPlus intentionally not launched' in main and 'selected_shadow_choice = "skip"' in main)
ck('R718_SKIP_NO_SHADOW_SPAWN', 'if (!strcmp(selected_shadow_choice, "skip"))' in main and 'elfldr_spawn("/", STDOUT_FILENO, selected_shadow' in main)
ck('R718_SKIP_CONTINUES_FTP', main.index('PIZZA HEN S0-SKIP') < main.index('PIZZA HEN F0: starting ftpsrv'))
ck('R718_SKIP_ACTIVE_MARKER', 'shadowmount_active.txt' in main and "v==='stable'||v==='experimental'||v==='skip'" in sh)
ck('R718_BUILD_BASE_VERIFY', 'KSTUFF_BASE_EXPECTED_SHA' in build and 'KSTUFF_BASE_SOURCE_EXPECTED_SHA' in build)
ck('R718_NO_BOOT_SHELLUI_PRELOAD', 'cmd_preload_toolbox_hooks' not in main)
print(f'R7_18_KSTUFF_BASE_SHADOW_SKIP_DUMP_INSTALLER={sum(checks)}/{len(checks)} '+('PASS' if all(checks) else 'FAIL'))
raise SystemExit(0 if all(checks) else 1)
