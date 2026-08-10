#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
build=(ROOT/'build_pizzahen_multisdk.sh').read_text(errors='ignore')
cm=(ROOT/'Source Code/CMakeLists.txt').read_text(errors='ignore')
sdkdoc=(ROOT/'SDK_COMPATIBILITY.txt').read_text(errors='ignore')
test_text='\n'.join(q.read_text(errors='ignore') for q in (ROOT/'TESTS').glob('*.py') if q.name != Path(__file__).name)
checks=[]
def ok(name, cond):
    if not cond: raise SystemExit(f'{name}=FAIL')
    checks.append(name); print(f'{name}=PASS')
ok('FIX39_NO_PIL_DEPENDENCY', 'from PIL' not in test_text and 'import PIL' not in test_text)
ok('FIX39_NO_V042_PIN', 'PAYLOAD_SDK_V042' not in build and 'PAYLOAD_SDK_V042' not in cm)
ok('FIX39_ENV_ALIASES', all(x in build for x in ['PIZZA_HEN_SDK','PS5_PAYLOAD_SDK','PS5SDK','PAYLOAD_SDK']))
ok('FIX39_CURRENT_TOOLCHAIN', 'toolchain/prospero.cmake' in build)
ok('FIX39_LEGACY_TOOLCHAIN', 'cmake/toolchain-ps5.cmake' in build)
ok('FIX39_COMPAT_WRAPPER', 'bin/prospero-cmake' in build)
ok('FIX39_FUTURE_TOOLCHAIN_OVERRIDE', 'PIZZA_HEN_TOOLCHAIN_FILE' in build and 'CUSTOM_TOOLCHAIN' in build)
ok('FIX39_FUTURE_WRAPPER_OVERRIDE', 'PIZZA_HEN_CMAKE_WRAPPER' in build and 'CUSTOM_CMAKE_WRAPPER' in build)
ok('FIX39_SOURCE_SDK_ALIAS_LAYER', all(x in cm for x in ['PIZZA_HEN_SDK_ROOT','PS5_PAYLOAD_SDK','PS5SDK']))
ok('FIX39_PREBUILT_SHADOW_SDK_NEUTRAL', 'SHADOWMOUNT_SDK_DEPENDENCY=NONE_PREBUILT_RUNTIME' in build)
ok('FIX39_POLICY_DOCUMENTED', 'capability' in sdkdoc.lower() or 'release-neutral' in sdkdoc.lower())
ok('FIX39_TARGET', 'PIZZA-HEN-v0.1-FIX45-PLUGIN-MANAGER-LIFECYCLE.elf' in (ROOT/'Source Code/unpacker/CMakeLists.txt').read_text(errors='ignore'))
print(f'FIX39_STATIC={len(checks)}/{len(checks)} PASS')
