#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, re, sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "Source Code"
HTML = SRC / "bootstrapper/assets/toolbox_launcher.html"
API = SRC / "toolbox_api/src/main.c"
MAIN = SRC / "bootstrapper/source/main.cpp"
DAEMON = SRC / "bootstrapper/source/daemon.c"
BUILD = ROOT / "build_v01_rebase_latest_toolbox.sh"
TP = ROOT / "ThirdParty/PS5-Game-Compressor-1.0.4-USER-SUPPLIED-FROZEN"
ELF = TP / "game-compressor.elf"
ZIP = TP / "PS5-Game-Compressor-1.0.4.zip"
ASSET = SRC / "bootstrapper/assets/game-compressor.elf"
META = TP / "source/payload-manager/game-compressor.elf.json"
EXPECTED_ELF = "e55e90aaade13b6e0d4316c1597ef90a21b67a06475c3e25de054224bc1e941b"
EXPECTED_ZIP = "daf2adaa586ab9234e984c7f2a9e706764f408fe0f714bba34f17347e99e66b2"
EXPECTED_INTEGRATED = "535aa4a8e951c04b98df33eb7d476dbcb6cbec080c00dfc8d574f1e61b233ac3"

checks=[]
def ck(name, ok):
    checks.append((name,bool(ok)))
    print(f"R720_{name}={'PASS' if ok else 'FAIL'}")
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else ""

html=HTML.read_text(encoding="utf-8")
api=API.read_text(encoding="utf-8")
main=MAIN.read_text(encoding="utf-8")
daemon=DAEMON.read_text(encoding="utf-8")
build=BUILD.read_text(encoding="utf-8")
ck("ELF_SHA", sha(ELF)==EXPECTED_ELF)
ck("SOURCE_ZIP_SHA", sha(ZIP)==EXPECTED_ZIP)
ck("UPSTREAM_FIDELITY", sha(ELF)==EXPECTED_ELF)
ck("INTEGRATED_NO_TILE_ASSET", sha(ASSET)==EXPECTED_INTEGRATED)
meta=json.loads(META.read_text(encoding="utf-8")) if META.is_file() else {}
ck("UPSTREAM_METADATA", meta.get("version")=="1.0.4" and meta.get("checksum")==EXPECTED_ELF and meta.get("name")=="Game Compressor")
ck("TOPLEVEL_ENTRY", 'onclick="openGameCompressor(this)"' in html and '>Game Compressor<' in html)
ck("NO_SERVICE_ROW", 'id="svc_game_compressor"' not in html)
ck("PATH", "const GAME_COMPRESSOR_PATH='/data/PIZZA_HEN/payloads/game-compressor.elf';" in html)
ck("WEBUI_5910", "const GAME_COMPRESSOR_URL='http://127.0.0.1:5910/';" in html)
ck("STATUS_BEFORE_LAUNCH", "serviceStatusAction('gamecompressor-status')" in html)
ck("LAUNCH_ON_DEMAND", "runAction('plugin-launch '+GAME_COMPRESSOR_PATH+' GameCompressor')" in html)
ck("WAIT_5910", "waitStatusAction('gamecompressor-status',true,80)" in html)
ck("OPEN_WEBUI", "location.href=GAME_COMPRESSOR_URL" in html)
ck("API_ACTION", '"gamecompressor-status"' in api and 'gamecompressor_port_ready()' in api)
ck("API_PORT_5910", 'sa.sin_port=htons(5910);' in api)
ck("EMBED", '.incbin \\\"../../../bootstrapper/assets/game-compressor.elf\\\"' in daemon and 'game_compressor_start' in daemon)
ck("DEPLOY", 'write_blob_file("/data/PIZZA_HEN/payloads/game-compressor.elf"' in main)
ck("NO_BOOT_AUTOSTART", 'plugin-launch /data/PIZZA_HEN/payloads/game-compressor.elf' not in main and 'launchElfDirect(GAME_COMPRESSOR_PATH)' not in html)
ck("NO_TILE_UI", 'no PSGC50001 tile' in html and 'game_compressor_desc' in html)
# Parse exact 31-locale object
try:
    a=html.index('const PH_I18N=')+len('const PH_I18N='); b=html.index(';\nconst PH_BASE_MAP=',a)
    i18n=json.loads(html[a:b])
except Exception:
    i18n={}
required=('game_compressor','game_compressor_desc','game_compressor_starting','game_compressor_not_ready')
ck("I18N_31", len(i18n)==31 and all(all(k in v and str(v[k]).strip() for k in required) for v in i18n.values()))
ck("I18N_NOT_ENGLISH_FALLBACK", len(i18n)==31 and len({v.get('game_compressor_desc') for v in i18n.values()})>=20)
ck("BASE_MAP", '"Game Compressor":"game_compressor"' in html and 'no PSGC50001 tile' in html and '":"game_compressor_desc"' in html)
ck("CREDIT", 'Game Compressor' in html[html.find('id="projects"'):html.find('id="about"')])
ck("BUILD_VERIFY", 'verify_frozen_elf_source GAME_COMPRESSOR' in build and 'GC_EXPECTED_SHA="'+EXPECTED_ELF+'"' in build)
ck("BUILD_STAGE", 'build_integrated_no_tile_variants.py' in build and 'cp -f "$GC_ELF" "$GC_DST"' not in build)
ck("BUILD_GATE", 'test_r720_game_compressor_full_i18n.py' in build)
ck("BUILD_METADATA", 'R720_GAME_COMPRESSOR_PORT=5910' in build and 'R720_GAME_COMPRESSOR_TILE=DISABLED_GC_LAUNCHER_START' in build)

ok=sum(v for _,v in checks)
print(f"R7_20_GAME_COMPRESSOR_FULL_I18N={ok}/{len(checks)} {'PASS' if ok==len(checks) else 'FAIL'}")
sys.exit(0 if ok==len(checks) else 1)
