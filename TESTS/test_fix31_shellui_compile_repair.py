#!/usr/bin/env python3
from pathlib import Path
import re
root = Path(__file__).resolve().parents[1]
mono = (root/'Source Code/shellui/src/MonoUtils.cpp').read_text()
hook = (root/'Source Code/shellui/src/HookFunctions.cpp').read_text()
checks=[]
def ok(name, cond):
    checks.append((name,bool(cond)))
    print(f'{name}={"PASS" if cond else "FAIL"}')

# The label `(PS5 native only)` contains )" and therefore must not live inside a default R"(...)" literal.
ok('CHEAT_REPO_CUSTOM_RAW_DELIMITER', 'std::string dl_cheats = R"PIZZA(' in mono and ')PIZZA";' in mono)
ok('CHEAT_REPO_RDX_LABEL_PRESERVED', 'RDX HEN-PPSA-Cheats (PS5 native only)' in mono)
ok('RELOAD_CHEATS_DECLARED', 'std::string reload_cheats' in mono)

# OnPress must not reference OnPreCreate's local s_MonoText.
onpress_start = hook.find('int OnPress_Hook(')
onpre_start = hook.find('int OnPreCreate_Hook(')
onpress = hook[onpress_start:onpre_start] if onpress_start >= 0 and onpre_start > onpress_start else ''
ok('ONPRESS_NO_LOCAL_MONOTEXT_REFERENCE', 's_MonoText =' not in onpress)

# The value getter belongs in OnPreCreate where s_MonoText is declared.
onpre = hook[onpre_start:] if onpre_start >= 0 else ''
ok('DISCORD_VALUE_IN_ONPRECREATE', 'else if (id == "id_discord_rpc_service")' in onpre and 'global_conf.discord_rpc ? "1" : "0"' in onpre)
ok('ONPRECREATE_MONOTEXT_DECLARED', 'MonoString* s_MonoText = nullptr;' in onpre)

# Ensure only the intentional two handlers exist: one OnPress toggle + one OnPreCreate value provider.
ok('DISCORD_HANDLER_COUNT_TWO', hook.count('id == "id_discord_rpc_service"') == 2)

failed=[n for n,v in checks if not v]
if failed:
    raise SystemExit('FIX31_STATIC_FAIL='+','.join(failed))
print(f'FIX31_STATIC={len(checks)}/{len(checks)} PASS')
