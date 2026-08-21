#!/usr/bin/env python3
from pathlib import Path
import hashlib, subprocess, tempfile, gzip, ast, re, sys
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'Source Code'; CR=SRC/'third_party/CheatRunner-0.17'
checks=[]
def ok(n,c):
 print(f'{n}={"PASS" if c else "FAIL"}');
 if not c: raise SystemExit(1)
 checks.append(n)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
# Upstream archive source fidelity: every original file remains byte-identical.
manifest=CR/'PIZZA_UPSTREAM_SHA256_MANIFEST.txt'
rows=[ln.split('  ',1) for ln in manifest.read_text().splitlines() if ln.strip()]
ok('R710_UPSTREAM_MANIFEST_COUNT',len(rows)==136)
for h,rel in rows:
 p=CR/rel
 if not (p.is_file() and sha(p)==h):
  ok('R710_UPSTREAM_SOURCE_FIDELITY',False)
ok('R710_UPSTREAM_SOURCE_FIDELITY',True)
ok('R710_UPSTREAM_VERSION','set(CHEATRUNNER_VERSION "0.17")' in (CR/'CMakeLists.txt').read_text())
ok('R710_UPSTREAM_PORT_9999','#define CHEATRUNNER_HTTP_PORT 9999' in (CR/'src/cr_config.h').read_text())
paths=(CR/'src/cr_paths.h').read_text()+ (CR/'src/cr_paths.c').read_text()
ok('R710_UPSTREAM_DATA_PATH','/data/cheatrunner' in paths)
http=(CR/'src/cr_http.c').read_text()+ (CR/'src/cr_api.c').read_text()
ok('R710_UPSTREAM_CORS','Access-Control-Allow-Origin: *' in http)
api=(CR/'src/cr_api_games.c').read_text()
ok('R710_UPSTREAM_HEALTH_RUNNING','/api/health' in api and '/api/running' in api)
dash=(CR/'src/dashboard_js.inc').read_text()
ok('R710_UPSTREAM_TRAINER_DEEPLINK',"#trainer=" in dash and 'openCheatModal' in dash)
# Missing-source-package helper gap is filled only by documented build adapters.
for f in ('gen_gzip_header.py','gen_blob_header.py','PIZZA_HEN_INTEGRATION_NOTE.md'): ok('R710_ADAPTER_'+f.replace('.','_').upper(),(CR/'tools'/f).is_file())
# Validate gzip generator against the exact C-string asset.
with tempfile.TemporaryDirectory() as td:
 out=Path(td)/'a.h'
 subprocess.check_call([sys.executable,str(CR/'tools/gen_gzip_header.py'),str(CR/'src/dashboard_html.inc'),str(out),'g_dashboard_html_gz'])
 txt=out.read_text(); vals=bytes(int(x,16) for x in re.findall(r'0x([0-9a-f]{2})',txt))
 expected=''.join(ast.literal_eval(x.strip()) for x in (CR/'src/dashboard_html.inc').read_text().splitlines() if x.strip()).encode()
 ok('R710_ADAPTER_GZIP_ROUNDTRIP',gzip.decompress(vals)==expected)
# Build/runtime integration.
top=(SRC/'CMakeLists.txt').read_text(); dcm=(SRC/'daemon/CMakeLists.txt').read_text(); emb=(SRC/'daemon/source/embeddded_payloads.c').read_text(); dm=(SRC/'daemon/source/main.cpp').read_text()
ok('R710_BUILD_SOURCE_TARGET','add_subdirectory(third_party/CheatRunner-0.17)' in top and 'RUNTIME_OUTPUT_DIRECTORY "${PROJECT_ROOT}/bin"' in top)
ok('R710_DAEMON_DEPENDS_CHEATRUNNER','elfldr CheatRunner)' in dcm)
ok('R710_EMBED_SOURCE_BUILT_ELF','pizzahen_cheatrunner_start' in emb and '.incbin \\"../../../bin/CheatRunner.elf\\"' in emb)
ok('R710_DEPLOY_ON_DEMAND_ELF','/data/PIZZA_HEN/payloads/CheatRunner.elf' in dm and 'pizzahen_cheatrunner_start' in dm)
# Legacy PIZZA cheat route retired.
hf=(SRC/'shellui/src/HookFunctions.cpp').read_text(); xml=(SRC/'shellui/assets/etaHEN_toolbox.xml').read_text(); um=(SRC/'util/source/main.cpp').read_text(); tb=(SRC/'bootstrapper/assets/toolbox_launcher.html').read_text()
ok('R710_NO_GAME_OPTIONS_CHEAT_REPLACEMENT','MENU_ID_CHEATS' not in hf and '★ PIZZA HEN Cheats' not in hf)
ok('R710_NO_ETAHEN_CHEAT_URI','etaHEN?Cheats' not in hf)
ok('R710_NO_NATIVE_CHEATS_XML_LINK','id="id_cheats"' not in xml)
ok('R710_NO_LEGACY_CACHE_START','pthread_create(&cheat_cache, NULL, MakeInitialCheatCache' not in um)
ok('R710_NO_DEAD_CHEAT_CACHE_HANDLE','cheat_cache' not in um)
ok('R710_NO_OLD_WEB_CHEAT_BACKEND',all(x not in tb for x in ('updateCheatRepository()','reloadCheatCache()','loadGameCheats()','cheat-toggle ')))
api_src=(SRC/'toolbox_api/src/main.c').read_text()
ok('R710_NO_OLD_TOOLBOX_API_CHEAT_ACTIONS',all(x not in api_src for x in ('\"update-cheats\"','\"reload-cheats\"','\"cheats-load\"','\"cheat-toggle\"')))
# Toolbox owns orchestration; upstream owns cheat logic/UI.
ok('R710_TOOLBOX_CHEATRUNNER_PANEL','Cheats — CheatRunner 0.17' in tb and 'id="cheatRunnerFrame"' in tb)
ok('R710_TOOLBOX_ONDEMAND_HBLDR',"launchElfDirect('/data/PIZZA_HEN/payloads/CheatRunner.elf')" in tb)
ok('R710_TOOLBOX_API_HEALTH',"CHEATRUNNER_URL+'/api/health" in tb)
ok('R710_TOOLBOX_API_RUNNING',"CHEATRUNNER_URL+'/api/running" in tb)
ok('R710_TOOLBOX_TRAINER_DEEPLINK',"#trainer=" in tb)
ok('R710_TOOLBOX_PORT_9999',"http://127.0.0.1:9999" in tb)
ok('R710_SHORTCUT_DIRECT_TOOLBOX',hf.count('http://127.0.0.1:8080/fs/data/PIZZA_HEN/ui/toolbox-launcher.html#cheats')>=3)
ok('R710_DOC',(ROOT/'CHEATRUNNER_INTEGRATION.md').is_file())
print(f'R7_10_CHEATRUNNER_INTEGRATION={len(checks)}/{len(checks)} PASS')
