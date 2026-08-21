from pathlib import Path
root = Path(__file__).resolve().parents[1]
main = (root / 'Source Code/daemon/source/main.cpp').read_text()
msg = (root / 'Source Code/daemon/source/msg.cpp').read_text()
boot = (root / 'Source Code/bootstrapper/source/main.cpp').read_bytes()
assert 'startup Game Options ShellUI preload disabled' in main
assert 'const bool game_options_ready = cmd_ensure_game_options_service_runtime();' not in main
assert 'bool cmd_ensure_game_options_service_runtime()' in msg
assert b'PIZZA HEN W0: KStuff selector stage' in boot
assert b'PIZZA HEN TDUAL: Media tiles ready' in boot
assert b'PIZZA HEN S0: starting pristine ShadowMountPlus 1.6beta16' in boot
print('R7.5.1 static isolation checks: PASS')
