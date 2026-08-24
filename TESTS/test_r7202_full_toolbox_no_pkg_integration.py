#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, re, sys, zipfile

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
UI=SRC/'bootstrapper/assets/toolbox_launcher.html'
BUILD=ROOT/'build_v01_rebase_latest_toolbox.sh'
PATCH=ROOT/'TOOLS/build_integrated_no_tile_variants.py'
DAEMON=SRC/'bootstrapper/source/daemon.c'
MAIN=SRC/'bootstrapper/source/main.cpp'

WEB_UP=ROOT/'ThirdParty/websrv-0.34-UPSTREAM-FROZEN/websrv-ps5.elf'
APR_UP=ROOT/'ThirdParty/apr-emu-updater-1.4-USER-SUPPLIED-FROZEN/apr_emu_updater.elf'
GC_UP=ROOT/'ThirdParty/PS5-Game-Compressor-1.0.4-USER-SUPPLIED-FROZEN/game-compressor.elf'
WEB=SRC/'bootstrapper/assets/websrv-ps5.elf'
APR=SRC/'bootstrapper/assets/apr_emu_updater.elf'
GC=SRC/'bootstrapper/assets/game-compressor.elf'

SHA={
 'web_up':'54730c867c6e1148536fdcb370e63a7762d989ea87b62488ad4caff64d43f263',
 'web':'16a18de9df60b4d726409121a2f24ea92616db03e1cc45fab49c8d05ae8b480c',
 'apr_up':'684a7e824e03f2402693641f347341a118fa0ac7a9573f212036a0a5337a8054',
 'apr':'fcd9472ea50141a51e3d6663aee2eadbe99b9e6e0cedf1421b7c1d67f62727a9',
 'gc_up':'e55e90aaade13b6e0d4316c1597ef90a21b67a06475c3e25de054224bc1e941b',
 'gc':'535aa4a8e951c04b98df33eb7d476dbcb6cbec080c00dfc8d574f1e61b233ac3',
}
checks=[]
def ck(n,x):
    x=bool(x); checks.append((n,x)); print(f'R7202_{n}={"PASS" if x else "FAIL"}')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else ''

def bytes_at(p,off,n):
    d=p.read_bytes(); return d[off:off+n]

ui=UI.read_text(encoding='utf-8')
build=BUILD.read_text(encoding='utf-8')
patch=PATCH.read_text(encoding='utf-8')
daemon=DAEMON.read_text(encoding='utf-8')
main=MAIN.read_text(encoding='utf-8')

# Frozen inputs remain pristine.
ck('WEBSRV_UPSTREAM_SHA',sha(WEB_UP)==SHA['web_up'])
ck('APR_UPSTREAM_SHA',sha(APR_UP)==SHA['apr_up'])
ck('GC_UPSTREAM_SHA',sha(GC_UP)==SHA['gc_up'])
# Runtime assets are deterministic derivatives.
ck('WEBSRV_INTEGRATED_SHA',sha(WEB)==SHA['web'])
ck('APR_INTEGRATED_SHA',sha(APR)==SHA['apr'])
ck('GC_INTEGRATED_SHA',sha(GC)==SHA['gc'])

# Exact no-tile byte deltas.
ck('WEBSRV_INSTALL_LAUNCHER_NOP',bytes_at(WEB,0x9C67,5)==bytes.fromhex('9090909090'))
ck('WEBSRV_UPSTREAM_CALL_PRESERVED',bytes_at(WEB_UP,0x9C67,5)==bytes.fromhex('e874020000'))
ck('APR_AUTO_TILE_BYPASS',bytes_at(APR,0x45CF,7)==bytes.fromhex('e9300000009090'))
ck('APR_MANUAL_TILE_ROUTE_DISABLED',bytes_at(APR,0x9D78,6)==bytes.fromhex('909090909090'))
ck('APR_INSTALL_TILE_BUTTON_DISABLED',b'<button id="installTile" hidden></button>' in APR.read_bytes())
ck('APR_LAUNCHER_BANNER_HIDDEN',b"banner.className = 'msg';" in APR.read_bytes())
ck('GC_LAUNCHER_START_NOP',bytes_at(GC,0x11944,5)==bytes.fromhex('9090909090'))
ck('GC_UPSTREAM_CALL_PRESERVED',bytes_at(GC_UP,0x11944,5)==bytes.fromhex('e850580200'))

# Build derivation is hash/preimage gated, not an opaque edited binary.
ck('PATCH_TOOL_HASH_GATED',all(x in patch for x in (SHA['web_up'],SHA['apr_up'],SHA['gc_up'],SHA['web'],SHA['apr'],SHA['gc'],'patch preimage mismatch')))
ck('BUILD_RUNS_DERIVER','python3 "$SCRIPT_DIR/TOOLS/build_integrated_no_tile_variants.py"' in build)
ck('BUILD_NO_DIRECT_COPY',all(x not in build for x in ('cp -f "$WEB_ELF" "$WEB_DST"','cp -f "$APR_ELF" "$APR_DST"','cp -f "$GC_ELF" "$GC_DST"')))
ck('BUILD_DISTINCT_HASHES',all(x in build for x in ('WEB_UPSTREAM_SHA="$($HASHCMD "$WEB_ELF"','WEB_SHA="$($HASHCMD "$WEB_DST"','APR_UPSTREAM_SHA="$($HASHCMD "$APR_ELF"','APR_SHA="$($HASHCMD "$APR_DST"','GC_UPSTREAM_SHA="$($HASHCMD "$GC_ELF"','GC_SHA="$($HASHCMD "$GC_DST"')))

# Existing bootstrap embedding/deployment stays intact.
ck('WEBSRV_EMBED','websrv-ps5.elf' in daemon)
ck('APR_EMBED','apr_emu_updater.elf' in daemon and 'apr_emu_updater_start' in daemon)
ck('GC_EMBED','game-compressor.elf' in daemon and 'game_compressor_start' in daemon)
ck('APR_DEPLOY','/data/PIZZA_HEN/payloads/apr_emu_updater.elf' in main)
ck('GC_DEPLOY','/data/PIZZA_HEN/payloads/game-compressor.elf' in main)

# Toolbox transports remain the same, only launcher creation is neutralized.
ck('HOME_DIRECT_WEBUI',"const HOMEBREW_CHANNEL_URL='/index.html';" in ui and 'location.href=HOMEBREW_CHANNEL_URL' in ui)
ck('APR_WEBUI_6971',"APR_EMU_UPDATER_URL='http://127.0.0.1:6971/'" in ui and 'openAprEmuUpdate(this)' in ui)
ck('GC_WEBUI_5910',"GAME_COMPRESSOR_URL='http://127.0.0.1:5910/'" in ui and 'openGameCompressor(this)' in ui)
ck('NO_PIZZA_BOOT_AUTOSTART','plugin-launch /data/PIZZA_HEN/payloads/apr_emu_updater.elf' not in main and 'plugin-launch /data/PIZZA_HEN/payloads/game-compressor.elf' not in main)
ck('ANTI_SHELLUI_PRELOAD','cmd_preload_toolbox_hooks();' not in main[main.find('int main('):] if 'int main(' in main else True)

# 31-language same-changeset policy for all three user-visible integrations.
try:
    a=ui.index('const PH_I18N=')+len('const PH_I18N='); b=ui.index(';\nconst PH_BASE_MAP=',a)
    i18n=json.loads(ui[a:b])
except Exception:
    i18n={}
req=('homebrew_channel_desc','homebrew_channel_opening','apr_emu_desc','apr_emu_starting','game_compressor_desc','game_compressor_starting')
ck('I18N_31',len(i18n)==31 and all(all(k in v and str(v[k]).strip() for k in req) for v in i18n.values()))
ck('I18N_HOME_NO_TILE','no launcher PKG or home-screen tile' in i18n.get('en-US',{}).get('homebrew_channel_desc',''))
ck('I18N_APR_NO_TILE','launcher PKG/tile disabled' in i18n.get('en-US',{}).get('apr_emu_desc',''))
ck('I18N_GC_NO_TILE','no PSGC50001 tile' in i18n.get('en-US',{}).get('game_compressor_desc',''))

# Source grounding: upstreams really contain the launcher behavior we neutralize.
webzip=ROOT/'ThirdParty/websrv-0.34-UPSTREAM-FROZEN/websrv-0.34.zip'
with zipfile.ZipFile(webzip) as z:
    n=next(n for n in z.namelist() if n.endswith('/src/ps5/sys.c'))
    ws=z.read(n).decode('utf-8','ignore')
ck('WEBSRV_SOURCE_INSTALL_LAUNCHER','install_launcher();' in ws and 'sceAppInstUtilInitialize' in ws)
gcsrc=ROOT/'ThirdParty/PS5-Game-Compressor-1.0.4-USER-SUPPLIED-FROZEN/source/src/gc_main.c'
ck('GC_SOURCE_LAUNCHER_START',gcsrc.is_file() and 'gc_launcher_start();' in gcsrc.read_text(encoding='utf-8'))

ck('METADATA_POLICY',all(x in build for x in ('WEBSRV_LAUNCHER=DISABLED_NO_PKG_NO_TILE','APR_EMU_UPDATER_LAUNCHER=DISABLED_AUTO_THREAD_AND_TILE_ENDPOINT','R720_GAME_COMPRESSOR_TILE=DISABLED_GC_LAUNCHER_START','R7202_PKG_POLICY=NO_PKG_NO_HOME_TILE')))
ck('DOC',(ROOT/'R7_20_2_FULL_TOOLBOX_NO_PKG_INTEGRATION.md').is_file())

ok=sum(v for _,v in checks)
print(f'R7_20_2_FULL_TOOLBOX_NO_PKG_INTEGRATION={ok}/{len(checks)} {"PASS" if ok==len(checks) else "FAIL"}')
sys.exit(0 if ok==len(checks) else 1)
