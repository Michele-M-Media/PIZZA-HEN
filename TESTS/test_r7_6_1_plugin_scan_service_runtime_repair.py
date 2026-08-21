from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
ui=(SRC/'bootstrapper/assets/toolbox_launcher.html').read_text(errors='ignore')
pm=(SRC/'util/source/PluginManager.cpp').read_text(errors='ignore')
um=(SRC/'util/source/main.cpp').read_text(errors='ignore')
ph=(SRC/'util/include/plugin_manager.hpp').read_text(errors='ignore')
checks=[]
def ck(n,v):
    ok=bool(v); checks.append(ok); print(f'{n}={"PASS" if ok else "FAIL"}')
ck('R761_PRE_PAYLOAD_MANAGER_UTIL_STARTUP', 'pizzahen_autostart_owned_payloads' not in um and 'pizzahen_autostart_owned_payloads' not in ph and 'pizzahen_autostart_owned_payloads' not in pm)
ck('R761_CANONICAL_CATALOG', '/data/PIZZA_HEN/runtime/plugin_catalog.json' in pm)
ck('R761_USER_CATALOG_ALIAS', '/user/data/PIZZA_HEN/runtime/plugin_catalog.json' in pm)
ck('R761_DUAL_CATALOG_PUBLISH', 'canonical_ok=write_catalog' in pm and 'user_ok=write_catalog' in pm and 'canonical_ok || user_ok' in pm)
ck('R761_WEB_DUAL_CATALOG_READ', '/fs/data/PIZZA_HEN/runtime/plugin_catalog.json' in ui and '/fs/user/data/PIZZA_HEN/runtime/plugin_catalog.json' in ui and 'readPluginCatalog' in ui)
ck('R761_DIRECT_ELF_NO_URLSEARCHPARAMS', "async function launchElfDirect(elfPath)" in ui and "encodeURIComponent(elfPath)" in ui)
ck('R761_SERVICE_GLOBALS_WEBKIT_SAFE', all(x in ui for x in ["var KLOGSRV_PATH=","var PIZZA_OVERLAY_PATH=","var OVERLAY_RUNTIME_LOCK=","var FAN_TARGET_PATHS=","var FAN_TARGET_TEMPS="]))
ck('R761_PIZZA_ROOTS', all(x in pm for x in ['/data/PIZZA_HEN/plugins','/data/PIZZA_HEN/payloads','/user/data/PIZZA_HEN/plugins','/user/data/PIZZA_HEN/payloads']))
ck('R761_LEGACY_SOURCE_ROOTS', all(x in pm for x in ['/data/etaHEN/plugins','/user/data/etaHEN/plugins','/mnt/usb%d/etaHEN/plugins','/mnt/ext%d/etaHEN/payloads']))
ck('R761_PAYLOAD_REPO_STILL_PRESENT', 'payload-repo-refresh' in ui and 'payload-repo-install' in ui)
if not all(checks): sys.exit(1)
print('R7_6_1_PLUGIN_SCAN_SERVICE_RUNTIME_REPAIR=PASS')
