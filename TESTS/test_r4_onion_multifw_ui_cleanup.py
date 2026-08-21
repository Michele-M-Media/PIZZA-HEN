#!/usr/bin/env python3
from pathlib import Path
import hashlib, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ok(name, cond):
    print(f'{name}={"PASS" if cond else "FAIL"}')
    if not cond: raise SystemExit(1)
msg=(SRC/'daemon/source/msg.cpp').read_text(errors='ignore')
xmlp=SRC/'shellui/assets/etaHEN_toolbox.xml'
xml=xmlp.read_text(errors='ignore')
hook=(SRC/'shellui/src/HookFunctions.cpp').read_text(errors='ignore')
policy=SRC/'daemon/include/onion/debug_settings_route_policy.hpp'
ET.parse(xmlp)
# Exact Onion 0.0.10 policy source hash.
ok('R4_ONION_POLICY_EXACT', sha(policy)=='f227e28d3e6ebaf1483d042b2d01a15249a80b03c8997aae1ab1014b46536f1e')
ok('R4_ONION_STANDARD_URI', 'pssettings:play?mode=settings&function=debug_settings' in policy.read_text())
ok('R4_ONION_OLD_URI', 'pssettings:play?mode=settings&function=debug_settings_old' in policy.read_text())
ok('R4_ONION_STANDARD_THROUGH_10_6', '0x1006ffff' in policy.read_text())
ok('R4_ONION_OLD_FROM_11', '0x11000000' in policy.read_text())
ok('R4_DAEMON_USES_ONION_POLICY', 'DebugSettingsRoutePolicy::for_system_version' in msg and 'sys_ver.version' in msg)
ok('R4_V01_ROUTE_NOT_HARDCODED_IN_CMD', msg.count('ItemzLaunchByUri(pizzahen_debug_services_uri_for_current_firmware())')==3)
# The Game Manager UI node remains literally in source, but inside an XML comment.
ok('R4_GAME_MANAGER_HIDDEN_MARKERS', 'PIZZA_HEN_HIDDEN_GAME_MANAGER_BEGIN' in xml and 'PIZZA_HEN_HIDDEN_GAME_MANAGER_END' in xml)
ok('R4_GAME_MANAGER_XML_PRESERVED', 'id_open_game_manager' in xml and 'Backend: ITEM00001 compatibility layer' in xml)
ok('R4_ITEMFLOW_HANDLER_PRESERVED', 'launch_pizzahen_backend("ITEM00001", "Game Manager")' in hook)
# Legacy top-level rows remain source-preserved but are inside one cleanup comment.
clean=xml.split('PIZZA HEN R4 UI cleanup:',1)[1].split('-->',1)[0]
ok('R4_PLUGINS_ROW_HIDDEN', 'Plugins / Payload ELFs' in clean and '<link id="id_plugins"' in clean)
ok('R4_CHEATS_ROW_RETIRED', '<link id="id_cheats"' not in xml)
# Dual Media architecture is untouched.
main=(SRC/'bootstrapper/source/main.cpp').read_text(errors='ignore')
ok('R4_DUAL_MEDIA_IDS_PRESERVED', 'PZHN00001' in main and 'PZHN00002' in main)
ok('R4_KSTUFF_110_PRESERVED', 'kstuff-lite-1.10' in main)
print('R4_ONION_MULTIFW_UI_CLEANUP=PASS')
