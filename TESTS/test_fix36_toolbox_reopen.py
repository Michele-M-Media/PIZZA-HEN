#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
msg=(SRC/'daemon/source/msg.cpp').read_text(encoding='utf-8')
html=(SRC/'bootstrapper/assets/toolbox_launcher.html').read_text(encoding='utf-8')
unpacker=(SRC/'unpacker/CMakeLists.txt').read_text(encoding='utf-8')

def ok(name, cond):
    print(f"{name}={'PASS' if cond else 'FAIL'}")
    if not cond: raise SystemExit(1)

ok('RESIDENT_PID_MARKER', '/system_tmp/pizzahen_toolbox_resident' in msg)
ok('RESIDENT_PID_READ', 'read_toolbox_resident_pid' in msg)
ok('RESIDENT_PID_WRITE', 'write_toolbox_resident_pid(pid)' in msg)
ok('REOPEN_REUSES_RESIDENT', 'Toolbox already resident in ShellUI pid' in msg)
ok('STALE_PID_CLEAR', 'resident marker stale' in msg and 'unlink(PIZZAHEN_TOOLBOX_RESIDENT)' in msg)
ok('NATIVE_SETTINGS_URI', 'ItemzLaunchByUri("pssettings:play?mode=settings&function=debug_settings")' in msg)
ok('NO_BROWSER_PSSETTINGS', "location.href='pssettings:" not in html)
ok('HTML_SAFE_REOPEN', "Open Toolbox Again" in html)
ok('NO_TOOLBOX_FORCEKILL', 'PIZZA HEN Toolbox injection failed; ShellUI left running' in msg)
ok('MEDIA_TILE_PRESERVED', 'PZHN00001' in (SRC/'bootstrapper/assets/toolbox_shortcut_param.json').read_text())
ok('KSTUFF_LITE_PRESERVED', 'kstuff-lite-1.09' in (SRC/'bootstrapper/source/main.cpp').read_text())
ok('KSTUFF_DR_PRESERVED', 'kstuff-dr-1.2' in (SRC/'bootstrapper/source/main.cpp').read_text())
ok('FIX36_OUTPUT', 'PIZZA-HEN-v0.1-FIX45-PLUGIN-MANAGER-LIFECYCLE.elf' in unpacker)
print('FIX36_STATIC=13/13 PASS')
