from pathlib import Path
import hashlib,re,sys
R=Path(__file__).resolve().parents[1]
S=R/'Source Code'
def txt(p): return (S/p).read_text(errors='replace')
def ok(name,cond):
    print(f'{name}={"PASS" if cond else "FAIL"}')
    if not cond: raise SystemExit(1)

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

api=txt('toolbox_api/src/main.c')
msg=txt('daemon/source/msg.cpp')
dmain=txt('daemon/source/main.cpp')
inc=txt('include/msg.hpp')
prx=txt('shellui/src/prx.cpp')
hook=txt('shellui/src/HookFunctions.cpp')
ui=txt('bootstrapper/assets/toolbox_launcher.html')
emb=txt('daemon/source/embeddded_payloads.c')

ok('R753_SINGLE_SHELL_SERVICE_ID', inc.count('BREW_PIZZAHEN_SHELL_SERVICE = 0x9000016')==1 and 'BREW_PIZZAHEN_GAME_OPTIONS_SERVICE' not in inc+api+msg)
ok('R753_SHELL_SERVICE_DAEMON_HANDLER', 'case BREW_PIZZAHEN_SHELL_SERVICE' in msg and 'cmd_ensure_shell_service_runtime()' in msg)
ok('R753_NO_POST_KSTUFF_AUTO_INJECTION', dmain.count('cmd_ensure_shell_service_runtime();')==1) # declaration only
ok('R753_LAZY_TOOLBOX_SERVICE_START', 'game-options-ensure' in ui and 'BREW_PIZZAHEN_SHELL_SERVICE' in api)
ok('R753_WEB_CONTROL_RESTORED', 'void PizzahenServiceWebControl()' in hook and 'PizzahenServiceWebControl();' in prx)
ok('R753_LIVE_SET_ROUTE', 'is_shell_key(key)' in api and 'send_shell_control("set",key,value)' in api)
ok('R753_CHEATS_GAME_OPTIONS_ENTRY', '★ PIZZA HEN Cheats' in hook and 'view=cheats&tid=' in hook)
ok('R753_CHEATS_DIRECT_VIEW_PARSE', 'new URLSearchParams(location.search).get(\'view\')' in ui)
ok('R753_DEBUG_CREATEJSON_NO_STACK', '/system_tmp/pizzahen_shell_service_online' in prx and '/system_tmp/pizzahen_shell_service_pid' in prx)

assets=['klogsrv-ps5.elf','fan_target_65c.elf','fan_target_70c.elf','fan_target_75c.elf','fan_target_80c.elf','fan_target_85c.elf']
for a in assets:
    p=S/'daemon/assets'/a
    ok('R753_ASSET_'+a.replace('.','_').upper(), p.exists() and p.read_bytes()[:4]==b'\x7fELF')
    sym='pizzahen_'+a.replace('-','_').replace('.elf','')
    ok('R753_EMBED_'+a.replace('.','_').upper(), '.incbin' in emb and a in emb)
    ok('R753_DEPLOY_'+a.replace('.','_').upper(), f'/data/PIZZA_HEN/payloads/{a}' in dmain)

# All literal UI actions must have an API strcmp handler.
acts=set()
for m in re.finditer(r"runAction\((?:`|'|\")([^`'\"]+)",ui):
    first=m.group(1).split()[0]
    if re.fullmatch(r'[a-z0-9-]+',first): acts.add(first)
handlers=set(re.findall(r'!strcmp\(action,"([^"]+)"\)',api))
missing=sorted(acts-handlers)
ok('R753_ALL_LITERAL_UI_ACTIONS_HAVE_HANDLER', not missing)

# Avoid another -Werror unused-static regression in toolbox_api.
unused=[]
for m in re.finditer(r'^static\s+(?:[\w\s\*]+?)\s+(\w+)\s*\(',api,re.M):
    n=m.group(1)
    if len(re.findall(r'\b'+re.escape(n)+r'\s*\(',api))<=1: unused.append(n)
ok('R753_TOOLBOX_API_NO_UNUSED_STATIC', not unused)
print('R7_5_3_FULL_TOOLBOX_CHEATS_SERVICES_RESTORE=PASS')
