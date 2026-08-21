#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
msg=(SRC/'daemon/source/msg.cpp').read_text()
main=(SRC/'daemon/source/main.cpp').read_text()
prx=(SRC/'shellui/src/prx.cpp').read_text()
hook=(SRC/'shellui/src/HookFunctions.cpp').read_text()
html=(SRC/'bootstrapper/assets/toolbox_launcher.html').read_text()

def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ')+name)
    if not cond: raise SystemExit(1)

ok('R73_STARTUP_SERVICE_DECL', 'cmd_ensure_game_options_service_runtime();' in main)
ok('R73_STARTUP_SERVICE_CALL', 'cmd_ensure_game_options_service_runtime();' in main)
ok('R73_SERVICE_MODE_MARKER', '/system_tmp/pizzahen_game_options_service_mode' in msg and '/system_tmp/pizzahen_game_options_service_mode' in prx)
ok('R73_SERVICE_ONLINE_MARKER', '/system_tmp/pizzahen_game_options_service_online' in msg and '/system_tmp/pizzahen_game_options_service_online' in prx)
ok('R73_SERVICE_PID_GUARD', '/system_tmp/pizzahen_game_options_service_pid' in msg and '/system_tmp/pizzahen_game_options_service_pid' in prx)
ok('R73_SERVICE_INJECTS_EXISTING_SHELLUI', 'Inject_Toolbox(pid, shellui_elf_start)' in msg)
ok('R73_SERVICE_NO_DEBUG_URI', 'cmd_ensure_game_options_service_runtime' in msg and 'ItemzLaunchByUri' not in msg[msg.index('bool cmd_ensure_game_options_service_runtime()'):msg.index('static const char *pizzahen_debug_services_uri_for_current_firmware()')])
ok('R73_OPTIONMENU_EXACT_TARGET', '"OptionMenu", "createJson", 8' in prx)
ok('R73_CHEATS_HANDLER_PRESERVED', '★ PIZZA HEN Cheats' in hook and 'MENU_ID_CHEATS' in hook)
ok('R73_FULL_DEBUG_PATH_SKIPS_SECOND_CREATEJSON', 'createJson already owned by resident Game Options service' in prx)
ok('R73_GAME_MANAGER_BUTTON_HIDDEN', '<span class="etaItemTitle">Game Manager</span>' not in html)
ok('R73_GAME_MANAGER_PANEL_PRESERVED', '<section id="games" class="panel"><h2>Game Manager</h2>' in html)
ok('R73_GAME_MANAGER_FUNCTION_PRESERVED', 'async function loadGames()' in html and "runAction('games-list')" in html)
ok('R73_DEBUG_SERVICES_TOOLBOX_LINK_REMOVED', '<span class="etaItemTitle">Debug Services</span>' not in html)
ok('R73_DEBUG_SERVICES_FUNCTION_PRESERVED', 'async function openDebugServices' in html)
for label in ['System Options','Rest Mode Options','Extras / Firmware Backends','Controller Shortcuts','PS5 webMAN Games','Homebrew Store']:
    ok('R73_REMOVED_'+label.upper().replace(' ','_').replace('/','_'), f'<span class="etaItemTitle">{label}</span>' not in html and f'<h2>{label}</h2>' not in html)
ok('R73_KSTUFF_SELECTOR_UNTOUCHED', (SRC/'bootstrapper/assets/kstuff_selector.js').exists())
ok('R73_DEBUG_MEDIA_LAUNCHER_PRESERVED', (SRC/'bootstrapper/assets/debug_services_launcher.html').exists())
print('R7_3_CHEATS_SERVICE_TOOLBOX_CLEANUP=PASS')
