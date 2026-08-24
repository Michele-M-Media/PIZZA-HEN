#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
checks=[]
def ck(name, cond):
    print(f"R715_{name}={'PASS' if cond else 'FAIL'}")
    checks.append(bool(cond))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
shadow=(SRC/'shadow_selector_action/src/main.c').read_text()
shadowcm=(SRC/'shadow_selector_action/CMakeLists.txt').read_text()
ui=(SRC/'bootstrapper/assets/toolbox_launcher.html').read_text()
boot=(SRC/'bootstrapper/source/main.cpp').read_text()
emb=(SRC/'bootstrapper/source/daemon.c').read_text()
build=(ROOT/'build_v01_rebase_latest_toolbox.sh').read_text()
credits=(ROOT/'CREDITS.md').read_text()
ck('SHADOW_REQUEST_BEFORE_HOME', shadow.find('rename(REQUEST_TMP, REQUEST_FILE)') < shadow.find('(void)sceSystemServiceNavigateToGoHome()'))
ck('SHADOW_HOME_CALL', 'sceSystemServiceNavigateToGoHome' in shadow and 'SceSystemService' in shadowcm)
ck('ELFLDR024_HASH', sha(SRC/'lib/elfldr.bin')=='6bf3a5416c84305f4e62cc952861f810806eb6613a3d24c4b35f947f2650ba33')
ck('ELFLDR024_UI_SERVICES', 'ELF Loader 0.24' in ui and "runAction('elfldr-start')" in ui)
ck('APR_UPSTREAM_HASH', sha(ROOT/'ThirdParty/apr-emu-updater-1.4-USER-SUPPLIED-FROZEN/apr_emu_updater.elf')=='684a7e824e03f2402693641f347341a118fa0ac7a9573f212036a0a5337a8054')
ck('APR_INTEGRATED_NO_TILE_HASH', sha(SRC/'bootstrapper/assets/apr_emu_updater.elf')=='fcd9472ea50141a51e3d6663aee2eadbe99b9e6e0cedf1421b7c1d67f62727a9')
ck('APR_EMBED', 'apr_emu_updater_start' in emb and 'apr_emu_updater.elf' in emb)
ck('APR_DEPLOY', '/data/PIZZA_HEN/payloads/apr_emu_updater.elf' in boot)
ck('APR_UI_TOPLEVEL', '>Apr Emu Update<' in ui and 'openAprEmuUpdate(this)' in ui)
ck('APR_WEBUI_6971', "APR_EMU_UPDATER_URL='http://127.0.0.1:6971/'" in ui)
ck('APR_ON_DEMAND_ONLY', 'openAprEmuUpdate(this)' in ui and 'apr_emu_updater_start' not in boot[boot.find('int main(void)') if 'int main(void)' in boot else len(boot):])
ck('R714_PIPELINE_PRESERVED', 'starting selected %s' in boot and 'starting ftpsrv v0.21 on port 2121' in boot and 'starting ps5debug-NG v1.3.0 automatically' in boot)
ck('APR_INCBIN_ESCAPED', r'.incbin \"../../../bootstrapper/assets/apr_emu_updater.elf\"' in emb)
ck('BUILD_RESULT_METADATA', 'ELFLDR_SHA256=$ELFLDR_SHA' in build and 'APR_EMU_UPDATER_SHA256=$APR_SHA' in build and 'R715_SHADOW_SELECTOR_AUTO_CLOSE=' in build)
ck('APR_CREDIT', 'https://github.com/tsuramatsu1/apr-emu-updater' in credits)
print(f"R7_15_SHADOW_CLOSE_ELFLDR024_APR={sum(checks)}/{len(checks)} {'PASS' if all(checks) else 'FAIL'}")
sys.exit(0 if all(checks) else 1)
