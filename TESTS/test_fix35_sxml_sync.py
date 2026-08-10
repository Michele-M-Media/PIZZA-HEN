#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
build=(ROOT/'build_pizzahen_multisdk.sh').read_text(encoding='utf-8')
key=b'U0lTVFIwX0lfU0VFX1lPVQ=='

def ok(name, cond):
    print(f"{name}={'PASS' if cond else 'FAIL'}")
    if not cond: raise SystemExit(1)

ok('BUILD_PRETEST_ENCRYPTXML', 'python3 shellui/assets/encryptxml.py' in build)
ok('BUILD_PRETEST_SYNC_MARKER', 'SXML_PRETEST_SYNC=PASS' in build)
for stem in ('etaHEN_toolbox','etaHEN_Lite'):
    plain=(SRC/f'shellui/assets/{stem}.xml').read_bytes()
    crypt=(SRC/f'shellui/assets/{stem}.sxml').read_bytes()
    decoded=bytes(b ^ key[i % len(key)] for i,b in enumerate(crypt))
    ok(f'{stem.upper()}_SXML_CURRENT', decoded==plain)
ok('FIX35_OUTPUT_NAME', 'PIZZA-HEN-v0.1-FIX45-PLUGIN-MANAGER-LIFECYCLE.elf' in build)
print('FIX35_STATIC=5/5 PASS')
