#!/usr/bin/env python3
from pathlib import Path
import hashlib, re, sys
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ck(name, cond):
    print(f'{name}={"PASS" if cond else "FAIL"}')
    if not cond: raise SystemExit(1)

# Frozen boot/KStuff selector/Debug Services bridge from the hardware-PASS lineage.
ck('R74_BOOTSTRAPPER_MAIN_EXACT_R3', sha(SRC/'bootstrapper/source/main.cpp')=='cf202070d73c50bcd5529c8895a93f9ef1132d07c397c51a5a560e91cd2b8419')
ck('R74_SELECTOR_ACTION_EXACT_R3', sha(SRC/'selector_action/src/main.c')=='950360ead9fb67d63f77f1977c4c16fc322ccca1726b1b802742a6cdd866c5c2')
ck('R74_KSTUFF_LITE_110_EXACT', sha(ROOT/'KSTUFF_INPUT/kstuff-v1.10-normal.elf')=='b1dfe57f367a35374f605127915eda38c76a6ed5d1c729e427955798bd78c66a')
ck('R74_DEBUG_SERVICES_LAUNCHER_FROZEN', sha(SRC/'bootstrapper/assets/debug_services_launcher.html')=='7f7134593eefa9628bc581eebe3a7fc66f40cba3bb8f9447ebd641bfe58eb399')
ck('R74_V01_HELPER_FROZEN', sha(SRC/'toolbox_action/src/main.c')=='8155569ab893e23d365b054d8c3075fcdebb6792b75f0ccf21d2bff33f76faf6')
ck('R74_ONION_POLICY_FROZEN', sha(SRC/'daemon/include/onion/debug_settings_route_policy.hpp')=='f227e28d3e6ebaf1483d042b2d01a15249a80b03c8997aae1ab1014b46536f1e')

# KStuff Toggle 0.6 exact uploaded prebuilt payloads.
expected_toggles={
    'kstuff-toggle-1.elf':'9009b96f36721a1b4c305735038d70cd72d596c553156bfa2a27e60a68ae2dee',
    'kstuff-toggle-2.elf':'ae8c39e79f731b5b0515b8487ff7986cf9a626e760881dacc107bd888f3694c6',
    'kstuff-toggle-3.elf':'0e87e92959791d9edf04c314802fcf18ccf37db74ae353d434a0062557f85093',
}
for fn,h in expected_toggles.items():
    p=SRC/'daemon/assets'/fn
    ck('R74_EXACT_'+fn.replace('-','_').replace('.','_').upper(), p.is_file() and sha(p)==h)

embed=(SRC/'daemon/source/embeddded_payloads.c').read_text(errors='ignore')
daemon=(SRC/'daemon/source/main.cpp').read_text(errors='ignore')
html=(SRC/'bootstrapper/assets/toolbox_launcher.html').read_text(errors='ignore')
api=(SRC/'toolbox_api/src/main.c').read_text(errors='ignore')
utilmsg=(SRC/'util/source/msg.cpp').read_text(errors='ignore')
utilmain=(SRC/'util/source/main.cpp').read_text(errors='ignore')
pm=(SRC/'util/source/PluginManager.cpp').read_text(errors='ignore')
repo=(SRC/'util/source/PayloadRepository.cpp').read_text(errors='ignore')
msg=(SRC/'include/msg.hpp').read_text(errors='ignore')

for i in (1,2,3):
    ck(f'R74_TOGGLE_{i}_EMBEDDED', f'kstuff-toggle-{i}.elf' in embed and f'pizzahen_kstuff_toggle_{i}_start' in embed)
    ck(f'R74_TOGGLE_{i}_DEPLOYED', f'/data/PIZZA_HEN/tools/kstuff-toggle-{i}.elf' in daemon)
    ck(f'R74_TOGGLE_{i}_UI_ACTION', f'runKstuffToggle({i})' in html)
ck('R74_KSTUFF_TOGGLE_MENU_PRESENT', 'KStuff Toggle 0.6' in html and 'TOGGLE PS5' in html and 'TOGGLE PS4' in html and 'TOGGLE BOTH' in html)
ck('R74_OLD_MANUAL_PAUSE_DROPDOWN_NOT_REINTRODUCED', 'id="cfg_pause_kstuff"' not in html)
ck('R74_KSTUFF_SELECTOR_STILL_PRESENT', 'KStuff Selector' in html and 'kstuff-selector.html' in html)

# PHU overlay: exact user binary, deployed at existing PIZZA HEN overlay path; no binary patching.
phu=SRC/'daemon/assets/pizza_overlay_phu_original.elf'
ck('R74_PHU_OVERLAY_EXACT', phu.is_file() and sha(phu)=='8e20deefb9100705be8352dc6acb47241c6a044b93dc3f578f93c424789b2622')
ck('R74_PHU_OVERLAY_EMBEDDED', 'pizza_overlay_phu_original.elf' in embed and 'pizzahen_phu_overlay_start' in embed)
ck('R74_PHU_OVERLAY_DEPLOY_PIZZA_PATH', '/data/PIZZA_HEN/payloads/pizza_overlay.elf' in daemon and 'pizzahen_phu_overlay_start' in daemon)
ck('R74_PHU_NATIVE_LOCK_UI', "const OVERLAY_RUNTIME_LOCK='/fs/data/phu_overlay.lock'" in html)
ck('R74_PHU_NATIVE_LOCK_API', 'unlink("/data/phu_overlay.lock")' in api)
ck('R74_OLD_OVERLAY_LOCK_GONE', '/data/pizza_overlay.on' not in api and '/fs/data/pizza_overlay.on' not in html)

# Payload Manager: only repository/download/checksum subset integrated into existing PIZZA manager.
ck('R74_PAYLOAD_REPO_URL_EXACT', 'https://itsplk.github.io/ps5-payloads-mirror/payloads.json' in repo)
ck('R74_PAYLOAD_INSTALL_DIR_EXACT', 'constexpr const char *kPayloadDir = "/data/PIZZA_HEN/payloads"' in repo)
ck('R74_PAYLOAD_REPO_REFRESH_IPC', 'BREW_UTIL_REFRESH_PAYLOAD_REPO = 0x8000017' in msg and 'case BREW_UTIL_REFRESH_PAYLOAD_REPO:' in utilmsg)
ck('R74_PAYLOAD_REPO_INSTALL_IPC', 'BREW_UTIL_INSTALL_PAYLOAD_REPO = 0x8000018' in msg and 'case BREW_UTIL_INSTALL_PAYLOAD_REPO:' in utilmsg)
ck('R74_PAYLOAD_REPO_API_ACTIONS', 'payload-repo-refresh' in api and 'payload-repo-install' in api)
ck('R74_PAYLOAD_REPO_UI_ACTIONS', 'AGGIORNA REPOSITORY' in html and 'SCARICA' in html and 'payload_repository.json' in html)
ck('R74_PAYLOAD_REPO_SHA256_VERIFY', 'compute_sha256_file' in repo and 'strcasecmp(got,pick->checksum)' in repo)
ck('R74_PAYLOAD_REPO_ELF_VALIDATION', "m[0]==0x7f&&m[1]=='E'&&m[2]=='L'&&m[3]=='F'" in repo)
ck('R74_PAYLOAD_REPO_FILENAME_GUARD', "name.find('/')" in repo and 'name.find("..")' in repo and 'ends_with_ci(name,".elf")' in repo)
ck('R74_PAYLOAD_REPO_RESCANS_PIZZA_MANAGER', 'pizzahen_scan_plugin_catalog()' in repo)

# Autostart: only canonical PIZZA payload folder and the existing .auto_start contract.
ck('R74_PAYLOAD_AUTOSTART_DECL', 'pizzahen_autostart_owned_payloads' in (SRC/'util/include/plugin_manager.hpp').read_text(errors='ignore'))
start=pm.find('bool pizzahen_autostart_owned_payloads()')
block=pm[start:] if start>=0 else ''
ck('R74_PAYLOAD_AUTOSTART_CANONICAL_ONLY', '/data/PIZZA_HEN/payloads' in block and '/mnt/usb' not in block and '/user/data/PIZZA_HEN' not in block)
ck('R74_PAYLOAD_AUTOSTART_MARKER', '.auto_start' in block)
ck('R74_PAYLOAD_AUTOSTART_EXISTING_LOADER', 'load_plugin(path.c_str())' in block)
ck('R74_PAYLOAD_AUTOSTART_AT_UTIL_BOOT', 'pizzahen_autostart_owned_payloads()' in utilmain and utilmain.find('IniliatizeHTTP()') < utilmain.find('pizzahen_autostart_owned_payloads()'))

# Explicitly ensure the full Payload Manager app/server was not integrated.
runtime_text='\n'.join([repo,utilmain,utilmsg,api,html])
ck('R74_NO_PLDMGR_8084_SERVER', 'MENU_PORT 8084' not in runtime_text and '8084' not in repo)
ck('R74_NO_PLDMGR_HTTP_ROUTES', '/list_payloads' not in runtime_text and '/repository_push' not in runtime_text and '/process_kill' not in runtime_text)
ck('R74_NO_PLDMGR_APP_PATHS', '/data/pldmgr' not in runtime_text)
ck('R74_NO_PLDMGR_FRONTEND', 'assets_index_html' not in runtime_text and 'pldmgr_server' not in runtime_text)

# Version notification requested by the project.
ck('R74_STARTUP_NOTIFICATION_V1', 'PIZZA HEN v1.0 | Michele Media' in daemon)
ck('R74_STARTUP_NOTIFICATION_OLD_GONE', 'PIZZA HEN v0.1 | Michele Media' not in daemon)

# Preserve R7.3 Cheats service and Itemflow bridge logic; R7.4 does not alter ShellUI source.
ck('R74_CHEATS_RESIDENT_SERVICE_PRESERVED', 'cmd_ensure_game_options_service_runtime()' in daemon)
hook=SRC/'shellui/src/HookFunctions.cpp'
ck('R74_SHELLUI_HOOKS_R73_FROZEN', sha(hook)=='34e0c82ae5a5c530b9a70a835ae9717db56843196e7b42befac585ac9386d247')
ck('R74_ITEMFLOW_HANDLER_PRESERVED', 'ITEM00001' in hook.read_text(errors='ignore'))

# Reference sources shipped for traceability; runtime is the PIZZA integration, not the full PLDMGR tree.
ref=ROOT/'REFERENCES_R7_4'
ck('R74_KSTUFF_SOURCE_REFERENCE_PRESENT', (ref/'kstuff-toggle-0.6/main.c').is_file() and (ref/'kstuff-toggle-0.6/README.md').is_file())
ck('R74_PAYLOAD_MANAGER_SOURCE_REFERENCE_PRESENT', (ref/'ps5-payload-manager-0.5.1/repository.c').is_file() and (ref/'ps5-payload-manager-0.5.1/sha256.c').is_file() and (ref/'ps5-payload-manager-0.5.1/LICENSE').is_file())

print('R7_4_KSTUFF_TOGGLE_PHU_OVERLAY_PAYLOAD_REPO=PASS')
