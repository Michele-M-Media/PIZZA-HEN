from pathlib import Path
import hashlib

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
checks=[]
def ck(name, cond):
    ok=bool(cond); checks.append(ok); print(f'{name}=' + ('PASS' if ok else 'FAIL'))
    return ok

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

main=(SRC/'bootstrapper/source/main.cpp').read_text()
daemon=(SRC/'bootstrapper/source/daemon.c').read_text()
kh=(SRC/'bootstrapper/assets/kstuff_selector.html').read_text()
sh=(SRC/'bootstrapper/assets/shadowmount_selector.html').read_text()
top=(SRC/'CMakeLists.txt').read_text()
bcm=(SRC/'bootstrapper/CMakeLists.txt').read_text()
action=(SRC/'shadow_selector_action/src/main.c').read_text()
build=(ROOT/'build_v01_rebase_latest_toolbox.sh').read_text()

stable=ROOT/'ThirdParty/ShadowMountPlus-1.6beta16-UPSTREAM-FROZEN/shadowmountplus.elf'
exp=ROOT/'ThirdParty/ShadowMountPlus-1.7alpha8-EXPERIMENTAL-FROZEN/shadowmountplus.elf'
expzip=ROOT/'ThirdParty/ShadowMountPlus-1.7alpha8-EXPERIMENTAL-FROZEN/ShadowMountPlus-1.7alpha8.zip'

ck('R714_STABLE_FROZEN_SHA', stable.exists() and sha(stable)=='a35246fb3bb6042b25653b51cdcbc33254b40339342bf1d2dd0d2eceee2ca526')
ck('R714_EXPERIMENTAL_ELF_SHA', exp.exists() and sha(exp)=='f15653fe90d81e5f82841ca693c0599d307c384d6454c1b0cc18190ae1ef4812')
ck('R714_EXPERIMENTAL_SOURCE_SHA', expzip.exists() and sha(expzip)=='144d227956d1d28ad1740a05d620ecf990ee6cc50b47ab86a7b258d1cca6cb25')
ck('R714_EXPERIMENTAL_VERSION_STRING', b'1.7alpha8' in exp.read_bytes())
ck('R714_SOURCE_TREE_PRESERVED', (ROOT/'ThirdParty/ShadowMountPlus-1.7alpha8-EXPERIMENTAL-FROZEN/source/ShadowMountPlus-1.7alpha8/src/main.c').exists())

ck('R714_ACTION_STABLE_EXPERIMENTAL_PRESERVED', '"stable"' in action and '"experimental"' in action and 'shadowmount_request.txt' in action)
ck('R714_ACTION_CMAKE', 'add_subdirectory(shadow_selector_action)' in top and 'shadow_selector_action' in bcm)
ck('R714_SELECTOR_UI_STABLE_EXPERIMENTAL_PRESERVED', 'ShadowMountPlus 1.6beta16' in sh and 'ShadowMountPlus 1.7alpha8' in sh and "chooseShadow('stable')" in sh and "chooseShadow('experimental')" in sh)
ck('R714_SELECTOR_ACTION_PATH', '/data/PIZZA_HEN/bin/pizzahen-shadowmount-select.elf' in sh)
ck('R714_KSTUFF_HANDOFF', "window.location.replace('/fs/data/PIZZA_HEN/ui/shadowmount-selector.html')" in kh)
ck('R714_SELECTOR_DEPLOYED', '/data/PIZZA_HEN/ui/shadowmount-selector.html' in main and '/data/PIZZA_HEN/bin/pizzahen-shadowmount-select.elf' in main)

ck('R714_DUAL_ELF_EMBEDS', 'shadowmount_start' in daemon and 'shadowmount_experimental_start' in daemon and 'shadowmountplus-experimental.elf' in daemon)
ck('R714_SELECTOR_EMBEDS', 'shadow_selector_html_start' in daemon and 'shadow_selector_action_start' in daemon)
ck('R714_MAIN_DUAL_SELECTION', 'selected_shadow = shadowmount_start' in main and 'selected_shadow = shadowmount_experimental_start' in main)
ck('R714_NO_TIMEOUT_AUTOSTART', 'V2-TIMEOUT: no ShadowMount selected' in main and 'wait_for_web_shadowmount_request' in main)
ck('R714_ACTIVE_MARKER', '/data/PIZZA_HEN/runtime/shadowmount_active.txt' in main)

w=main.index('PIZZA HEN W5: %s ready')
v=main.index('PIZZA HEN V0: ShadowMount selector stage')
td=main.index('PIZZA HEN TDUAL: Media tiles ready')
s=main.index('PIZZA HEN S0: starting selected %s')
f=main.index('PIZZA HEN F0: starting ftpsrv')
d=main.index('PIZZA HEN D0: starting ps5debug-NG')
ck('R714_PIPELINE_ORDER', w < v < td < s < f < d)

ck('R714_BUILD_VERIFY_EXP', 'SM_EXP_EXPECTED_SHA="f15653fe90d81e5f82841ca693c0599d307c384d6454c1b0cc18190ae1ef4812"' in build and 'SHADOWMOUNT_EXPERIMENTAL' in build)
ck('R714_BUILD_STAGE_BOTH', 'shadowmountplus.elf' in build and 'shadowmountplus-experimental.elf' in build and 'cp -f "$SM_EXP_ELF" "$SHADOW_EXP_DST"' in build)

print(f'R7_14_SHADOWMOUNT_DUAL_SELECTOR={sum(checks)}/{len(checks)} ' + ('PASS' if all(checks) else 'FAIL'))
raise SystemExit(0 if all(checks) else 1)
