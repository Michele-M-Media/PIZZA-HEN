from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=(root/'Source Code/toolbox_api/src/main.c').read_text()
main=(root/'Source Code/daemon/source/main.cpp').read_text()
checks={
 'TESTKIT_ENUM_MATCH':'#define BREW_TESTKIT_CHECK        0x09000010' in s,
 'SET_DIRECT_CONFIG':'rc=config_set_numeric(key,value);if(!rc)reload_daemons();' in s,
 'SET_NOT_GATED_BY_FAKE_SHELL_SERVICE':'if(is_shell_key(key))rc=shell_setting_set(key,value)' not in s,
 'R751_FREEZE_ROLLBACK_PRESERVED':'startup Game Options ShellUI preload disabled (R7.2 hardware-PASS behavior)' in main,
}
for k,v in checks.items(): print(('PASS ' if v else 'FAIL ')+k)
raise SystemExit(0 if all(checks.values()) else 1)
