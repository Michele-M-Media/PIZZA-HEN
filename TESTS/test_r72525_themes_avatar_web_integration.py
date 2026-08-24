#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, re, sys

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'Source Code/bootstrapper/assets/toolbox_launcher.html').read_text(encoding='utf-8', errors='ignore')
MAIN = (ROOT / 'Source Code/bootstrapper/source/main.cpp').read_text(errors='ignore')
DAEMON = (ROOT / 'Source Code/bootstrapper/source/daemon.c').read_text(errors='ignore')
BUILD = (ROOT / 'build_v01_rebase_latest_toolbox.sh').read_text(errors='ignore')
GEN = (ROOT / 'TOOLS/build_themes_avatar_web_only_variants.py').read_text(errors='ignore')

CO = ROOT / 'ThirdParty/PS5-Custom-Tool-Manager-vCustom-USER-SUPPLIED-ORIGINAL/PS5-Custom-Tool-Manager-_vCustom.elf'
CD = ROOT / 'ThirdParty/THEMES-AVATAR-INTEGRATED-DERIVED/PS5-Custom-Tool-Manager-_vCustom-pizza-web-only.elf'
WO = ROOT / 'ThirdParty/ps5-wallpaper-modd-v1.0-USER-SUPPLIED-ORIGINAL/ps5-wallpaper-modd_v1.0.elf'
WD = ROOT / 'ThirdParty/THEMES-AVATAR-INTEGRATED-DERIVED/ps5-wallpaper-modd_v1.0-pizza-web-only.elf'
CA = ROOT / 'Source Code/bootstrapper/assets/PS5-Custom-Tool-Manager-_vCustom-pizza-web-only.elf'
WA = ROOT / 'Source Code/bootstrapper/assets/ps5-wallpaper-modd_v1.0-pizza-web-only.elf'

CO_SHA='297824ceaf6ea53fde57550adf9b5c2fc44c63ef60e8196ab92d351d1615d9cb'
CD_SHA='ecdf8a8eaa47f59bfe5b419dcb3f60bd3dc68deef9f36a5e36c125f3e71987b7'
WO_SHA='b18a866bac9deff45b921b7d3ea6143d541117b56c666d817ecdc81961829139'
WD_SHA='a2fa5e9c8ecb794fed189bcd204008ea446a12c2d1381fa601734b3d915d5360'

checks=[]
def ck(name, cond):
    ok=bool(cond); checks.append(ok); print(f'R72525_{name}={"PASS" if ok else "FAIL"}')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else ''

ck('CUSTOM_ORIGINAL_SHA', sha(CO)==CO_SHA)
ck('CUSTOM_DERIVED_SHA', sha(CD)==CD_SHA)
ck('WALLPAPER_ORIGINAL_SHA', sha(WO)==WO_SHA)
ck('WALLPAPER_DERIVED_SHA', sha(WD)==WD_SHA)
ck('CUSTOM_ASSET_EXACT_DERIVED', CA.is_file() and CA.read_bytes()==CD.read_bytes())
ck('WALLPAPER_ASSET_EXACT_DERIVED', WA.is_file() and WA.read_bytes()==WD.read_bytes())

# Deterministic source-grounded integration deltas.
cb=CD.read_bytes() if CD.is_file() else b''
wb=WD.read_bytes() if WD.is_file() else b''
ck('CUSTOM_STARTUP_INSTALLER_DISABLED', len(cb)>0xad00 and cb[0xacfb:0xad00]==bytes.fromhex('31c0909090'))
ck('CUSTOM_WEB_INSTALLER_DISABLED', len(cb)>0x16a96 and cb[0x16a91:0x16a96]==bytes.fromhex('31c0909090'))
ck('CUSTOM_INSTALL_ROUTE_REMOVED', b'/api/install-xmb' not in cb and b'/api/blocked-xmb' in cb)
ck('CUSTOM_TILE_BUTTON_REMOVED', b"<button onclick='uninstallLauncher()'>Retirer tuile</button>" not in cb)
ck('CUSTOM_CORE_WEB_FUNCTIONS_PRESERVED', all(x in cb for x in (b'/api/apps?ts=',b'/api/replace',b'/api/restore',b'/api/visibility',b'/api/system-apps')))
ck('CUSTOM_PORT_8089_PRESERVED', b'127.0.0.1:8089' in cb or b':8089' in cb)
ck('WALLPAPER_HOME_INSTALLER_DISABLED', len(wb)>0xd8e6 and wb[0xd8e1:0xd8e6]==bytes.fromhex('31c0909090'))
ck('WALLPAPER_AUTO_BROWSER_DISABLED', len(wb)>0xda16 and wb[0xda11:0xda16]==bytes.fromhex('31c0909090'))
ck('WALLPAPER_AUTO_BROWSER_CONTROL_HIDDEN_SAFE', b'id="autoBrowserToggle" style="display:none"' in wb)
ck('WALLPAPER_CORE_WEB_FUNCTIONS_PRESERVED', all(x in wb for x in (b'/api/list',b'/api/apply',b'/api/backup',b'/api/restore',b'/api/targets')))
ck('WALLPAPER_PORT_8095_PRESERVED', b':8095' in wb)

# Toolbox/iframe integration: on-demand like CheatRunner, never generic install/autostart.
ck('TOOLBOX_TOPLEVEL_ENTRY', "show('themesavatar')" in HTML and '<span class="etaItemTitle">Themes Avatar</span>' in HTML)
ck('THEMES_PANEL', '<section id="themesavatar" class="panel"><h2>Themes Avatar</h2>' in HTML)
ck('CUSTOM_START_RELOAD_OPEN', "startThemesAvatarTool('custom',false)" in HTML and "startThemesAvatarTool('custom',true)" in HTML and "openThemesAvatarFull('custom')" in HTML)
ck('WALLPAPER_START_RELOAD_OPEN', "startThemesAvatarTool('wallpaper',false)" in HTML and "startThemesAvatarTool('wallpaper',true)" in HTML and "openThemesAvatarFull('wallpaper')" in HTML)
ck('SHARED_IFRAME', 'id="themesAvatarFrame"' in HTML and 'startThemesAvatarTool' in HTML)
ck('CUSTOM_RUNTIME_PATH', "/data/PIZZA_HEN/payloads/PS5-Custom-Tool-Manager-pizza-web-only.elf" in HTML)
ck('WALLPAPER_RUNTIME_PATH', "/data/PIZZA_HEN/payloads/ps5-wallpaper-modd-pizza-web-only.elf" in HTML)
ck('WEB_PORTS', 'http://127.0.0.1:8089/' in HTML and 'http://127.0.0.1:8095/' in HTML)
ck('ON_DEMAND_HBLDR', 'await launchElfDirect(tool.path)' in HTML)
ck('NO_THEME_AUTOSTART', 'plugin-autostart '+"'+CUSTOM_TOOL_MANAGER_PATH" not in HTML and 'plugin-autostart '+"'+WALLPAPER_MODDER_PATH" not in HTML)
ck('LOCAL_PLUGIN_DUPLICATES_FILTERED', 'it.path!==CUSTOM_TOOL_MANAGER_PATH' in HTML and 'it.path!==WALLPAPER_MODDER_PATH' in HTML)
ck('ORIGINAL_REPOSITORY_INSTALLS_FILTERED', "'PS5-Custom-Tool-Manager-_vCustom.elf'" in HTML and "'ps5-wallpaper-modd_v1.0.elf'" in HTML)

# 31-locale rule for the new visible surface.
m=re.search(r'const PH_I18N=(\{.*?\});\nconst PH_BASE_MAP=',HTML,re.S)
i18n=json.loads(m.group(1)) if m else {}
need=('themes_avatar','themes_avatar_desc','themes_avatar_custom_desc','themes_avatar_wallpaper_desc','themes_avatar_idle','open')
ck('I18N_31', len(i18n)==31)
ck('I18N_KEYS_ALL_31', len(i18n)==31 and all(all(k in d and str(d[k]).strip() for k in need) for d in i18n.values()))
ck('ITALIAN_THEMES_AVATAR', i18n.get('it-IT',{}).get('themes_avatar')=='Themes Avatar' and 'Non viene installata' in i18n.get('it-IT',{}).get('themes_avatar_desc',''))
ck('ARABIC_THEMES_AVATAR', bool(i18n.get('ar-SA',{}).get('themes_avatar_desc')))
ck('JAPANESE_THEMES_AVATAR', bool(i18n.get('ja-JP',{}).get('themes_avatar_desc')))
ck('RTL_POLICY_UNCHANGED', "'ar-SA'" in HTML and 'dir' in HTML)

# Embed/deploy and reproducible build gates.
ck('MAIN_DEPLOY_CUSTOM', 'custom_tool_manager_start' in MAIN and 'PS5-Custom-Tool-Manager-pizza-web-only.elf' in MAIN)
ck('MAIN_DEPLOY_WALLPAPER', 'wallpaper_modder_start' in MAIN and 'ps5-wallpaper-modd-pizza-web-only.elf' in MAIN)
ck('DAEMON_INCBIN_CUSTOM', 'PS5-Custom-Tool-Manager-_vCustom-pizza-web-only.elf' in DAEMON)
ck('DAEMON_INCBIN_WALLPAPER', 'ps5-wallpaper-modd_v1.0-pizza-web-only.elf' in DAEMON)
ck('GENERATOR_PRESENT', 'startup XMB installer call' in GEN and 'home-screen installer call' in GEN and 'automatic browser decision' in GEN)
ck('BUILD_RUNS_GENERATOR', 'build_themes_avatar_web_only_variants.py' in BUILD)
ck('BUILD_VERIFIES_ORIGINALS', 'CUSTOM_TOOL_ORIGINAL' in BUILD and 'WALLPAPER_MODDER_ORIGINAL' in BUILD)
ck('BUILD_VERIFIES_DERIVED', 'CUSTOM_TOOL_WEB_ONLY' in BUILD and 'WALLPAPER_MODDER_WEB_ONLY' in BUILD)
ck('BUILD_METADATA', 'R72525_INSTALLER_POLICY=NO_HOME_TILE_NO_LAUNCHER_ICON_NO_PKG' in BUILD and 'R72525_I18N=31_LOCALES' in BUILD)

passed=sum(checks); total=len(checks)
print(f'R7_25_2_5_THEMES_AVATAR_WEB_INTEGRATION={passed}/{total} {"PASS" if passed==total else "FAIL"}')
sys.exit(0 if passed==total else 1)
