#!/usr/bin/env python3
from pathlib import Path
import hashlib,sys
root=Path(__file__).resolve().parents[1]
h=root/'Source Code/shellui/include/HookedFuncs.hpp'; p=root/'Source Code/shellui/src/prx.cpp'; f=root/'Source Code/shellui/src/HookFunctions.cpp'
checks=[]
def ck(n,c): print(f'{n}={"PASS" if c else "FAIL"}'); checks.append(bool(c))
ht=h.read_text(errors='ignore')
onion_delta=[
    'extern void (*ReactNavigatorManager_UpdateNavigationState_Orig)(MonoObject* instance, MonoObject* state);\n',
    'extern void (*DebugSettings_GetModel_Orig)(MonoObject* instance, MonoObject* param, MonoObject* promise);\n',
    'void ReactNavigatorManager_UpdateNavigationState_Hook(MonoObject* instance, MonoObject* state);\n',
    'void DebugSettings_GetModel_Hook(MonoObject* instance, MonoObject* param, MonoObject* promise);\n',
]
normalized=ht
for line in onion_delta:
    ck('R7531_ONION_HEADER_DELTA_'+str(onion_delta.index(line)+1), normalized.count(line)==1)
    normalized=normalized.replace(line,'',1)
ck('R7531_FROZEN_HOOKEDFUNCS_PLUS_ONION_DELTA',hashlib.sha256(normalized.encode()).hexdigest()=='4ad0f7d38557ec0c80fb1959a46f66d893ce781078d92e783165de87c0cb73bc')
ck('R7531_NO_SERVICE_DECL_IN_FROZEN_HEADER','PizzahenServiceWebControl' not in h.read_text(errors='ignore'))
ck('R7531_LOCAL_SERVICE_FORWARD_DECL','void PizzahenServiceWebControl();' in p.read_text(errors='ignore'))
ck('R7531_SERVICE_IMPL_PRESERVED','void PizzahenServiceWebControl()' in f.read_text(errors='ignore'))
print('R7_5_3_1_STATIC_GATE_COMPILE_REPAIR='+('PASS' if all(checks) else 'FAIL'))
sys.exit(0 if all(checks) else 1)
