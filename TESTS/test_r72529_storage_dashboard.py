#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, re, sys
ROOT=Path(__file__).resolve().parents[1]
UI=(ROOT/'Source Code/bootstrapper/assets/toolbox_launcher.html').read_text(encoding='utf-8',errors='ignore')
API=(ROOT/'Source Code/toolbox_api/src/main.c').read_text(encoding='utf-8',errors='ignore')
BUILD=(ROOT/'build_v01_rebase_latest_toolbox.sh').read_text(encoding='utf-8',errors='ignore')
fail=0

def ck(name,cond):
    global fail
    print(f"R72529_{name}={'PASS' if cond else 'FAIL'}")
    if not cond: fail+=1

def fn(name):
    m=re.search(rf'async function {name}\(.*?(?=\nasync function |\nfunction |\nconst |\nlet |\nvar |</script>)',UI,re.S)
    return m.group(0) if m else ''

def sha(s): return hashlib.sha256(s.encode()).hexdigest()

ck('STORAGE_SCREEN', '<section id="storage" class="panel"><h2>Storage</h2>' in UI)
pkg=re.search(r'<section id="packages" class="panel">.*?</section>',UI,re.S).group(0)
ck('STORAGE_ENTRY_SEPARATE', "show('storage');loadStorage()" in UI and "show('storage')" not in pkg)
ck('STORAGE_LOAD_ACTION', "await runAction('storage-scan')" in UI)
ck('STORAGE_JSON_READ', '/fs/data/PIZZA_HEN/runtime/storage_status.json' in UI)
ck('STORAGE_CARDS', all(x in UI for x in ('storageCard','storageMeterFill','storage_total','storage_used','storage_free')))
ck('INTERNAL_RENDER', "v.kind==='internal'" in UI and "storage_internal" in UI)
ck('NVME_RENDER', "v.kind==='nvme'" in UI and "storage_nvme" in UI)
ck('USB_RENDER', "storage_usb" in UI and "v.kind==='usb'" in UI)

ck('API_ACTION_REGISTERED', '"pkg-scan","storage-scan","games-list"' in API)
ck('API_ACTION_DISPATCH', 'if(!strcmp(action,"storage-scan"))' in API and 'write_storage_snapshot()' in API)
ck('MOUNT_TABLE_SOURCE', '#include <sys/mount.h>' in API and 'getfsstat(NULL,0,MNT_NOWAIT)' in API)
ck('INTERNAL_MOUNT', 'storage_find_mount(fs,got,"/user")' in API)
ck('EXT_MOUNTS', '"/mnt/ext%d"' in API and 'for(int i=0;i<2;i++)' in API)
ck('USB_MOUNTS_0_7', '"/mnt/usb%d"' in API and 'for(int i=0;i<8;i++)' in API)
segment=API[API.find('write_storage_snapshot'):API.find('static int is_action_name')]
ck('READ_ONLY_STORAGE', 'nmount(' not in segment and 'unmount(' not in segment and not re.search(r'(?<!find_)\bmount\s*\(',segment))

ck('PKG_SCAN_FROZEN', sha(fn('scanPkgs'))=='10d842aec854f6b1ffbc63b383023c28f30ddf70f87a0823fec8fc5f74c71c2b')
ck('PKG_CATALOG_FROZEN', sha(fn('loadPkgCatalog'))=='86a25d4b7df94dd51ade747e4bea58ce4065e6ea7c09550929bfa0e40e372483')
ck('PKG_INSTALL_FROZEN', sha(fn('installPkg'))=='c63da3c5e4dfa041c7743b30a252c4a99063b65286855536c9efa01b6aadef0d')
ck('PKG_UPSTREAM_ROUTE_PRESERVED', "fetch('/hbldr?'" in UI and 'PKGInstall' in UI)

m=re.search(r'const PH_I18N=(\{.*?\});\nconst PH_BASE_MAP=',UI,re.S)
i18n=json.loads(m.group(1)) if m else {}
keys=('storage','storage_hint','storage_internal','storage_nvme','storage_usb','storage_total','storage_used','storage_free','storage_not_detected','storage_loading','storage_volumes')
ck('I18N_31', len(i18n)==31 and all(all(k in v for k in keys) for v in i18n.values()))
ck('ITALIAN_STORAGE', i18n.get('it-IT',{}).get('storage')=='Memoria')
ck('JAPANESE_STORAGE', bool(i18n.get('ja-JP',{}).get('storage_hint')))
ck('ARABIC_STORAGE', bool(i18n.get('ar-SA',{}).get('storage_hint')))
ck('BUILD_TEST_HOOK', 'test_r72529_storage_dashboard.py' in BUILD)
ck('BUILD_METADATA', 'R72529_STORAGE_DASHBOARD=INTERNAL_NVME_USB_READ_ONLY' in BUILD)

print(f"R7_25_2_9_STORAGE_DASHBOARD={25-fail}/25 {'PASS' if fail==0 else 'FAIL'}")
sys.exit(1 if fail else 0)
