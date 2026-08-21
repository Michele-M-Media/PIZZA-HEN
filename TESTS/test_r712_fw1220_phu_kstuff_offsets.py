from pathlib import Path
import hashlib, struct, sys, zipfile, re
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
HOOK=SRC/'shellui/src/HookFunctions.cpp'
EMBED=SRC/'daemon/source/embeddded_payloads.c'
PHU_ORIG=SRC/'daemon/assets/pizza_overlay_phu_original.elf'
PHU_PATCH=SRC/'daemon/assets/pizza_overlay_phu_fw1220plus.elf'
KZIP=ROOT/'ThirdParty/kstuff-lite-1.10-UPSTREAM-USER-SUPPLIED/kstuff-lite-1.10.zip'
DPI=SRC/'util/source/DirectPKGInstaller.cpp'
POL=SRC/'shellui/include/onion_debug_settings_route_policy.hpp'
DOC=ROOT/'READ_THIS_R7_12_FW1220_PHU_KSTUFF_OFFSETS_REPAIR.txt'
checks=[]
def ck(name,ok):
    checks.append((name,bool(ok))); print(f'R712_{name}={"PASS" if ok else "FAIL"}')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

hook=HOOK.read_text()
embed=EMBED.read_text()

# Exact resolver cases that were absent from pause_resume_kstuff().
for fw in ['0x11000000','0x11200000','0x11400000','0x11600000','0x12000000','0x12020000','0x12200000','0x12400000','0x12600000','0x12700000']:
    ck('HOOK_CASE_'+fw[2:], hook.count('case '+fw+':') >= 2)  # resolver + capability gate
ck('HOOK_11_00_20_SYSENT', '0xdcbc78' in hook and '0xdcbdf0' in hook)
ck('HOOK_11_40_60_SYSENT', '0xdcbc98' in hook and '0xdcbe10' in hook)
ck('HOOK_12X_SYSENT', '0xdcc978' in hook and '0xdccaf0' in hook)
ck('NO_UNSUPPORTED_FALLTHROUGH_BEFORE_12X', hook.find('case 0x12700000:', hook.find('void pause_resume_kstuff')) < hook.find('default:', hook.find('void pause_resume_kstuff')))

# KStuff Lite 1.10 is the authority for 12.x exact fields.
expected={'allproc':'0x2885e00','sysentvec':'0xdcc978','sysentvec_ps4':'0xdccaf0','p_sysent':'0xa08'}
try:
    with zipfile.ZipFile(KZIP) as z:
        for fw in ['12_00','12_02','12_20','12_40','12_60','12_70']:
            t=z.read(f'kstuff-lite-1.10/prosper0gdb/offsets/{fw}.h').decode(errors='replace').lower()
            ok=all(re.search(rf'def\(\s*{re.escape(k)}\s*,\s*{re.escape(v)}\s*\)',t) for k,v in expected.items())
            ck('KSTUFF110_'+fw,ok)
except Exception:
    for fw in ['12_00','12_02','12_20','12_40','12_60','12_70']: ck('KSTUFF110_'+fw,False)

# Preserve original PHU; derivative must be a four-byte range-only patch.
ck('PHU_ORIGINAL_SHA', PHU_ORIG.is_file() and sha(PHU_ORIG)=='8e20deefb9100705be8352dc6acb47241c6a044b93dc3f578f93c424789b2622')
ck('PHU_PATCH_SHA', PHU_PATCH.is_file() and sha(PHU_PATCH)=='af930375e1be960254ce2ac70fbd29230b9f67937cf69bca8b66520371bdbb3b')
if PHU_ORIG.is_file() and PHU_PATCH.is_file():
    a=PHU_ORIG.read_bytes(); b=PHU_PATCH.read_bytes()
    diffs=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y]
    ck('PHU_SAME_SIZE',len(a)==len(b))
    ck('PHU_ONLY_RANGE_FIELD_DELTA',diffs==[0x656c6])  # LE 0x1200ffff -> 0x1270ffff changes byte 2 only
    try:
        vals=struct.unpack_from('<26I',b,0x656b8)
        ck('PHU_12X_RANGE',vals[2]==0x12000000 and vals[3]==0x1270ffff)
        ck('PHU_12X_ALLPROC',vals[4]==0x2885e00)
        ck('PHU_12X_SYSENT',vals[6]==0xdcc978 and vals[8]==0xdccaf0)
    except Exception:
        ck('PHU_12X_RANGE',False); ck('PHU_12X_ALLPROC',False); ck('PHU_12X_SYSENT',False)
else:
    for n in ['PHU_SAME_SIZE','PHU_ONLY_RANGE_FIELD_DELTA','PHU_12X_RANGE','PHU_12X_ALLPROC','PHU_12X_SYSENT']: ck(n,False)
ck('PHU_PATCH_EMBEDDED','pizza_overlay_phu_fw1220plus.elf' in embed and 'pizzahen_phu_overlay_start' in embed)

# Freeze neighboring fixes/inputs.
ck('DPIV2_R711_FROZEN',DPI.is_file() and sha(DPI)=='5a14caa77e9e121eea5a5c3ebd2de40c6c4ad1736e79714b7c4a6b6bc2b54d69')
ck('ONION_POLICY_FROZEN',POL.is_file() and sha(POL)=='f227e28d3e6ebaf1483d042b2d01a15249a80b03c8997aae1ab1014b46536f1e')
ck('KSTUFF110_INPUT_FROZEN',KZIP.is_file() and sha(KZIP)=='f96e7ddea315be7e15cbbc18ea1b53b9bb42c0ee3f9aa656eb1c80bce4a993a4')
ck('DOC',DOC.is_file() and '0xDCC978' in DOC.read_text() and '12.70' in DOC.read_text())

passed=sum(ok for _,ok in checks)
print(f'R7_12_FW1220_PHU_KSTUFF_OFFSETS={passed}/{len(checks)} '+('PASS' if passed==len(checks) else 'FAIL'))
sys.exit(0 if passed==len(checks) else 1)
