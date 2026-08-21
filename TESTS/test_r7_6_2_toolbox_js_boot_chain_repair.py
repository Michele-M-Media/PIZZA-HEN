from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
ui=(ROOT/'Source Code/bootstrapper/assets/toolbox_launcher.html').read_text(errors='ignore')
checks=[]
def ck(n,v):
    ok=bool(v); checks.append(ok); print(f'{n}={"PASS" if ok else "FAIL"}')
# R7.3 intentionally removed these panels. Their old eager initializers must not abort the script.
ck('R762_REMOVED_SYSTEM_PANEL_STILL_REMOVED','id="systemChecks"' not in ui)
ck('R762_REMOVED_REST_PANEL_STILL_REMOVED','id="restChecks"' not in ui)
ck('R762_REMOVED_SHORTCUT_PANEL_STILL_REMOVED','id="shortcutControls"' not in ui)
ck('R762_ADDCHECKS_MISSING_HOST_GUARD',"function addChecks(id,defs){const box=document.getElementById(id);if(!box)return;" in ui)
ck('R762_SHORTCUT_MISSING_HOST_GUARD',"function shortcut(id,title,subtitle,options){const host=document.getElementById('shortcutControls');if(!host)return;" in ui)
ck('R762_NO_UNGUARDED_SHORTCUT_APPEND',"document.getElementById('shortcutControls').appendChild(row)" not in ui)
# These assignments were previously never reached on hardware because the script aborted above them.
for token in ["var KLOGSRV_PATH=","var PIZZA_OVERLAY_PATH=","var FAN_TARGET_PATHS=","var FAN_TARGET_TEMPS="]:
    ck('R762_RUNTIME_GLOBAL_'+token.split()[1].split('=')[0] if ' ' in token else 'R762_RUNTIME_GLOBAL', token in ui)
ck('R762_PLUGIN_SCAN_CHAIN_PRESENT',"async function scanPlugins()" in ui and "await runAction('plugin-scan')" in ui and 'await loadPluginCatalog()' in ui)
ck('R762_PLUGIN_CATALOG_FILTER_PRESENT','!isFanTargetPath(it.path)' in ui)
ck('R762_PAYLOAD_MANAGER_PRESERVED','payload-repo-refresh' in ui and 'payload-repo-install' in ui)
if not all(checks): sys.exit(1)
print('R7_6_2_TOOLBOX_JS_BOOT_CHAIN_REPAIR=PASS')
