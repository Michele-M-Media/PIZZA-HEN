from pathlib import Path
import hashlib, re, sys
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
main=(SRC/'daemon/source/main.cpp').read_text(encoding='utf-8')
msg=(SRC/'daemon/source/msg.cpp').read_text(encoding='utf-8')
hook=(SRC/'shellui/src/HookFunctions.cpp').read_text(encoding='utf-8')
mono=(SRC/'shellui/src/MonoUtils.cpp').read_text(encoding='utf-8')
boot=(SRC/'bootstrapper/source/main.cpp').read_text(encoding='utf-8')
xml=(SRC/'shellui/assets/etaHEN_toolbox.xml').read_text(encoding='utf-8')
checks=[]
def ck(name, cond): checks.append((name,bool(cond)))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

# Toolbox-owned Cheats/Game Options hook must be present and enabled by default.
ck('CHEATS_MENU_HOOK_PRESENT', '★ PIZZA HEN Cheats' in hook and 'MENU_ID_CHEATS' in hook)
ck('GAME_OPTIONS_DEFAULT_ON', 'Settings.etaHEN_Game_Options", "1"' in mono)
ck('CREATEJSON_HOOK_FROZEN_R5', sha(SRC/'shellui/src/HookFunctions.cpp') == '34e0c82ae5a5c530b9a70a835ae9717db56843196e7b42befac585ac9386d247')

# R6 startup preload is the v0.1 injection + toolbox_online handshake, with no Debug Settings navigation.
ck('PRELOAD_FUNCTION_DECLARED', 'bool cmd_preload_toolbox_hooks();' in main)
ck('PRELOAD_CALLED_IN_MEDIA_MODE', 'if (!is_lite && !cmd_preload_toolbox_hooks())' in main)
ck('PRELOAD_USES_V01_INJECT', 'Inject_Toolbox(current_shellui_pid, shellui_elf_start)' in msg)
ck('PRELOAD_USES_V01_HANDSHAKE', 'while (!if_exists("/system_tmp/toolbox_online"))' in msg and 'if (++wait >= 15)' in msg)
ck('PRELOAD_MARKS_RESIDENT', 'write_toolbox_resident_pid(current_shellui_pid);' in msg and 'touch_file("/system_tmp/pizzahen_shellui_preloaded")' in msg)

m=re.search(r'bool cmd_preload_toolbox_hooks\(\)\{(.*?)\n\}\n\nbool cmd_enable_toolbox', msg, re.S)
pre=m.group(1) if m else ''
ck('PRELOAD_FUNCTION_FOUND', bool(pre))
ck('PRELOAD_NO_DEBUG_ROUTE', 'int uri_rc' not in pre and 'pizzahen_debug_services_uri_for_current_firmware' not in pre)
ck('PRELOAD_KSTUFF_PAUSE_GUARD', 'pause_resume_kstuff()' in pre and '/system_tmp/kstuff_paused' in pre)

# Debug Services remains its independent R3/R4 path and reuses preloaded ShellUI.
ck('DEBUG_SERVICES_PRELOAD_REUSE', '/system_tmp/pizzahen_shellui_preloaded' in msg and 'write_toolbox_resident_pid(current_shellui_pid);' in msg)
ck('DEBUG_SERVICES_ONION_ROUTE_PRESERVED', 'pizzahen_debug_services_uri_for_current_firmware' in msg and 'DebugSettingsRoutePolicy::for_system_version' in msg)
ck('DEBUG_SERVICES_LAUNCHER_FROZEN', sha(SRC/'bootstrapper/assets/debug_services_launcher.html') == '7f7134593eefa9628bc581eebe3a7fc66f40cba3bb8f9447ebd641bfe58eb399')
ck('V01_HELPER_FROZEN', sha(SRC/'toolbox_action/src/main.c') == '8155569ab893e23d365b054d8c3075fcdebb6792b75f0ccf21d2bff33f76faf6')

# R5 UI cleanup and two-tile architecture stay intact.
ck('R5_TITLE_PRESERVED', 'PIZZA HEN Debug Services' in xml)
ck('R5_XML_FROZEN', sha(SRC/'shellui/assets/etaHEN_toolbox.xml') == 'e40c6d30dd8270d8f4320e8e1b9bbd6f8efc94a6c8ab55093023d7079cab3d0e')
ck('DUAL_MEDIA_PRESERVED', 'PZHN00001' in boot and 'PZHN00002' in boot and 'install_pizzahen_debug_services_shortcut' in boot)
ck('KSTUFF_110_PRESERVED', 'kstuff-lite-1.10.elf' in boot and 'kstuff-lite-1.10' in boot)

failed=[n for n,v in checks if not v]
for n,v in checks: print(f'{n}={"PASS" if v else "FAIL"}')
if failed:
    print('R6_TOOLBOX_CHEATS_AUTOLINK_FAIL='+','.join(failed))
    sys.exit(1)
print(f'R6_TOOLBOX_CHEATS_AUTOLINK={sum(v for _,v in checks)}/{len(checks)} PASS')
