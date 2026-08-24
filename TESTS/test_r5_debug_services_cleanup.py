#!/usr/bin/env python3
from pathlib import Path
import hashlib, re, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ok(name, cond):
    print(f'{name}={"PASS" if cond else "FAIL"}')
    if not cond: raise SystemExit(1)
xmlp=SRC/'shellui/assets/etaHEN_toolbox.xml'
root=ET.parse(xmlp).getroot()
xml=xmlp.read_text(errors='ignore')
titles=[e.attrib.get('title','') for e in root.iter()]
all_active='\n'.join(titles)
# Requested Debug Services branding.
ok('R5_DEBUG_SERVICES_TITLE', any(t=='★ PIZZA HEN Debug Services' for t in titles))
ok('R5_OLD_ROOT_TITLE_GONE', not any(t=='★ PIZZA HEN Toolbox' for t in titles))
# Requested rows/menus are gone from the ACTIVE XML surface.
for name, text in [
    ('R5_OVERLAY_MENU_REMOVED','Game Overlay Menu'),
    ('R5_KSTUFF_CONTROL_REMOVED','Kstuff Control — Normal Test Baseline'),
    ('R5_MANUAL_FAN_ENABLE_REMOVED','Enable Manual Fan Speed Threshold'),
    ('R5_MANUAL_FAN_ADJUST_REMOVED','Adjust Fan Threshold'),
    ('R5_CONTROLLER_SHORTCUTS_REMOVED','Controller Shortcuts'),
]:
    ok(name, text not in all_active)
# Settings now focuses a row that still exists.
utils=next((e for e in root.iter('setting_list') if e.attrib.get('id')=='id_utils'),None)
ok('R5_SETTINGS_FOCUS_VALID', utils is not None and utils.attrib.get('initial_focus_to')=='id_disp_titleids')
# R4 hidden rows and Game Manager/ITEM00001 bridge remain preserved.
ok('R5_GAME_MANAGER_STILL_HIDDEN', 'PIZZA_HEN_HIDDEN_GAME_MANAGER_BEGIN' in xml and 'PIZZA_HEN_HIDDEN_GAME_MANAGER_END' in xml)
hook=(SRC/'shellui/src/HookFunctions.cpp').read_text(errors='ignore')
ok('R5_ITEMFLOW_HANDLER_PRESERVED', 'launch_pizzahen_backend("ITEM00001", "Game Manager")' in hook)
ok('R5_PLUGINS_STILL_HIDDEN', '<link id="id_plugins" title="Plugins / Payload ELFs"' in xml)
ok('R5_CHEATS_LEGACY_ROW_RETIRED', '<link id="id_cheats"' not in xml)
# Hardware-PASS R3 bridge and R4 Onion route code are frozen.
ok('R5_V01_HELPER_EXACT', sha(SRC/'toolbox_action/src/main.c')=='8155569ab893e23d365b054d8c3075fcdebb6792b75f0ccf21d2bff33f76faf6')
ok('R5_HOOKFUNCTIONS_R710_CHEATRUNNER_DELTA', 'MENU_ID_CHEATS' not in hook and '★ PIZZA HEN Cheats' not in hook and 'ITEM00001' in hook)
boot=(SRC/'bootstrapper/source/main.cpp').read_text(errors='ignore')
if 'PIZZA HEN V0: ShadowMount selector stage' in boot:
    ok('R5_BOOTSTRAPPER_R714_INTENTIONAL_SHADOW_SELECTOR_DELTA', 'PZHN00001' in boot and 'PZHN00002' in boot and 'kstuff-lite-1.10' in boot and 'PIZZA HEN F0: starting ftpsrv' in boot)
else:
    ok('R5_BOOTSTRAPPER_R4_FROZEN', sha(SRC/'bootstrapper/source/main.cpp')=='cf202070d73c50bcd5529c8895a93f9ef1132d07c397c51a5a560e91cd2b8419')
daemon_msg=(SRC/'daemon/source/msg.cpp').read_text(errors='ignore')
route_m=re.search(r'static const char \*pizzahen_debug_services_uri_for_current_firmware\(\) \{.*?\n\}',daemon_msg,re.S)
cmd_m=re.search(r'bool cmd_enable_toolbox\(\)\{.*?\n\}\nvoid handleIPC',daemon_msg,re.S)
route_hash=hashlib.sha256((route_m.group(0) if route_m else '').encode()).hexdigest()
cmd_hash=hashlib.sha256((cmd_m.group(0) if cmd_m else '').encode()).hexdigest()
ok('R5_DAEMON_ROUTE_R4_FROZEN', route_hash=='3d7f0018db98bb1dbc9e18805a15b9e0b845643766c401be5dd1f8459ebd341b' and cmd_hash=='1694dc9d1e2dcbd8e363a5480ec1c11695d606ed9dc7f1fb208f158a11e9114a')
ok('R5_ONION_POLICY_EXACT', sha(SRC/'daemon/include/onion/debug_settings_route_policy.hpp')=='f227e28d3e6ebaf1483d042b2d01a15249a80b03c8997aae1ab1014b46536f1e')
# Dual Media IDs and KStuff 1.10 still present.
main=(SRC/'bootstrapper/source/main.cpp').read_text(errors='ignore')
ok('R5_DUAL_MEDIA_IDS_PRESERVED', 'PZHN00001' in main and 'PZHN00002' in main)
ok('R5_KSTUFF_110_PRESERVED', 'kstuff-lite-1.10' in main)
print('R5_DEBUG_SERVICES_CLEANUP=PASS')
