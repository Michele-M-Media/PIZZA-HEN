#!/usr/bin/env python3
from pathlib import Path
R=Path(__file__).resolve().parents[1]; S=R/'Source Code'
def t(p): return (S/p).read_text(errors='replace')
def ck(n,c):
 print(f'{n}={"PASS" if c else "FAIL"}')
 if not c: raise SystemExit(1)
h=t('shellui/src/HookFunctions.cpp'); m=t('util/source/msg.cpp'); c=t('util/source/CheatManager.cpp')
block=h[h.index('if(id_str == "MENU_ID_CHECK_PATCH")'):h.index('if(id_str == "MENU_ID_INTELLECTUAL_PROPERTY_NOTICES")')]
ck('R79_CHEATS_R75_DIRECT_OWNED_ROUTE','toolbox-launcher.html?tid=' in block and 'cheats_uri += "#cheats"' in block)
ck('R79_CHEATS_NO_DEBUG_DEPENDENCY','etaHEN?Cheats_not_open' not in block)
ck('R79_CHEATS_TID_PID_CONTEXT','current_menu_tid' in block and 'find_pid(current_menu_tid.c_str(), false, true, true)' in block)
for path in ['/system_data/priv/appmeta/','/user/appmeta/','/system_data/priv/appmeta/external/','/user/app/','/system_ex/app/']:
 ck('R79_VERSION_ROOT_'+path.replace('/','_').strip('_').upper(),path in m)
ck('R79_VERSION_PARSE_FAILURE_IS_EMPTY','return "Error Opening Json"' not in m and 'return "Error getting version"' not in m)
ck('R79_CHEAT_MONITOR_JOINABLE','pthread_detach(pthreadMonitor)' not in c and 'monitorThreadJoinable' in c and 'pthread_join(pthreadMonitor' in c)
ck('R79_CACHE_CLEAR_STOPS_MONITOR','stopCheatMonitorAndJoin();\n  cache.clear();' in c)
ck('R79_CACHE_RELOAD_STOPS_MONITOR','stopCheatMonitorAndJoin();\n  update_cheat_caches();' in c)
ck('R79_PREVIEW_NOT_ACTIVE_STATE','Cheat preview only for %s version %s (game not running)' in c)
ck('R79_ACTIVE_STATE_BEFORE_MONITOR_CREATE',c.index('currentGameCheat = cheat;\n    currentGameTitleId = name;') < c.index('pthread_create(&pthreadMonitor'))
ck('R79_TOGGLE_TITLE_GUARD','currentGameTitleId != title_id' in c)
ck('R79_TOGGLE_BOUNDS_GE_SIZE','static_cast<size_t>(cheat_index) >= currentGameCheat->cheats.size()' in c)
print('R7_9_CHEATS_STABILITY_REPAIR=PASS')
