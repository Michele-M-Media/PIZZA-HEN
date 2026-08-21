from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=(root/'Source Code/toolbox_api/src/main.c').read_text()
checks={
 'DEAD_SHELL_SETTING_SET_REMOVED':'static int shell_setting_set(' not in s,
 'DEAD_IS_SHELL_KEY_REMOVED':'static int is_shell_key(' not in s,
 'DEAD_COPY_FILE_ATOMIC_REMOVED':'static int copy_file_atomic(' not in s,
 'DEAD_MIRROR_SHELL_CONFIG_REMOVED':'static int mirror_shell_config(' not in s,
 'R752_DIRECT_CONFIG_ROUTE_PRESERVED':'rc=config_set_numeric(key,value);if(!rc)reload_daemons();' in s,
 'TESTKIT_ENUM_FIX_PRESERVED':'#define BREW_TESTKIT_CHECK        0x09000010' in s,
}
for k,v in checks.items(): print(('PASS ' if v else 'FAIL ')+k)
raise SystemExit(0 if all(checks.values()) else 1)
