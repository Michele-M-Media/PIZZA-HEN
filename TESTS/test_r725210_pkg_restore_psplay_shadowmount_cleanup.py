#!/usr/bin/env python3
from pathlib import Path
import hashlib, re, sys

ROOT=Path(__file__).resolve().parents[1]
UI=(ROOT/'Source Code/bootstrapper/assets/toolbox_launcher.html').read_text(encoding='utf-8',errors='ignore')
BOOT=(ROOT/'Source Code/bootstrapper/source/main.cpp').read_text(encoding='utf-8',errors='ignore')
BUILD=(ROOT/'build_v01_rebase_latest_toolbox.sh').read_text(encoding='utf-8',errors='ignore')
SM_PATHS=(ROOT/'ThirdParty/ShadowMountPlus-1.6beta16-UPSTREAM-FROZEN/source/ShadowMountPlus-1.6beta16/include/sm_paths.h').read_text(encoding='utf-8',errors='ignore')
SM_INSTALL=(ROOT/'ThirdParty/ShadowMountPlus-1.6beta16-UPSTREAM-FROZEN/source/ShadowMountPlus-1.6beta16/src/sm_install.c').read_text(encoding='utf-8',errors='ignore')
PSPLAY=ROOT/'ThirdParty/PS-Play-v2.1-USER-SUPPLIED-FROZEN/PS-Play_v2.1.elf'
SM_ELF=ROOT/'ThirdParty/ShadowMountPlus-1.6beta16-UPSTREAM-FROZEN/shadowmountplus.elf'
fail=0

def ck(name,cond):
    global fail
    print(f"R725210_{name}={'PASS' if cond else 'FAIL'}")
    if not cond: fail+=1

def sha_bytes(p):
    h=hashlib.sha256();
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
    return h.hexdigest()

def sha_text(s): return hashlib.sha256(s.encode()).hexdigest()

def fn(name):
    token=('async function ' if ('async function '+name) in UI else 'function ')+name
    st=UI.find(token)
    if st<0:return ''
    m=re.search(r'\n(?:async )?function [A-Za-z0-9_]+',UI[st+1:])
    en=st+1+m.start() if m else len(UI)
    return UI[st:en]

pkg=re.search(r'<section id="packages" class="panel">.*?</section>\n',UI,re.S)
ck('PKG_SECTION_R72528_EXACT', bool(pkg) and sha_text(pkg.group(0))=='36294cecebefdb8186e48a8f96d4c7df2b09feeae2d3dc476cf4f6d1331b9378')
ck('PKG_SCAN_R72528_EXACT', sha_text(fn('scanPkgs'))=='10d842aec854f6b1ffbc63b383023c28f30ddf70f87a0823fec8fc5f74c71c2b')
ck('PKG_CATALOG_R72528_EXACT', sha_text(fn('loadPkgCatalog'))=='86a25d4b7df94dd51ade747e4bea58ce4065e6ea7c09550929bfa0e40e372483')
ck('PKG_ARGS_R72528_EXACT', sha_text(fn('upstreamPkgArgs'))=='0bad7fd0b40e5d6b3b248c5c554bc3ecc02d185b6a04abb6482f706079fdbb1b')
ck('PKG_INSTALL_R72528_EXACT', sha_text(fn('installPkg'))=='c63da3c5e4dfa041c7743b30a252c4a99063b65286855536c9efa01b6aadef0d')
ck('PKG_HBLDR_R72528_EXACT', sha_text(fn('launchHardwarePassPkg'))=='c453b40df500d4359c8031387d0f3963fe499869bc93b663b100bea56d082b9f')
ck('STORAGE_SEPARATE_TOP_LEVEL', "show('storage');loadStorage()" in UI and pkg and "show('storage')" not in pkg.group(0))
ck('STORAGE_NO_NULLISH', '??' not in UI and 'function storageRank(kind)' in UI)
ck('STORAGE_SCREEN_PRESERVED', '<section id="storage" class="panel"><h2>Storage</h2>' in UI and "runAction('storage-scan')" in UI)

psb=PSPLAY.read_bytes() if PSPLAY.is_file() else b''
ck('PSPLAY_FROZEN_SHA', PSPLAY.is_file() and sha_bytes(PSPLAY)=='e3392379d5bc6ca4e44cb0d2a1d8921083b2c3ea480725f68378831874542d8d')
ck('PSPLAY_GENERATED_SOURCE_PROVEN', b'/data/homebrew/ProsperoPlayer/sce_sys/param.json' in psb and b'PRSP10001' in psb and b'PS Play' in psb)
ck('SHADOWMOUNT_SCANS_DATA_HOMEBREW', '"/data/homebrew"' in SM_PATHS)
ck('SHADOWMOUNT_INSTALL_NOTIFY_SOURCE', 'Installing: %s (%s)' in SM_INSTALL and 'notify_system_info' in SM_INSTALL)
ck('SHADOWMOUNT_FROZEN_SHA', SM_ELF.is_file() and sha_bytes(SM_ELF)=='a35246fb3bb6042b25653b51cdcbc33254b40339342bf1d2dd0d2eceee2ca526')
ck('CLEANUP_POSITIVE_ID', 'text_file_contains_two(param, "PRSP10001", "PS Play")' in BOOT)
ck('CLEANUP_KNOWN_FILES_ONLY', all(x in BOOT for x in (
    'unlink("/data/homebrew/ProsperoPlayer/eboot.elf")',
    'unlink("/data/homebrew/ProsperoPlayer/sce_sys/icon0.png")',
    'unlink(param)',
    'rmdir("/data/homebrew/ProsperoPlayer/sce_sys")')))
ck('CLEANUP_BEFORE_SHADOW_SELECTOR', BOOT.find('cleanup_shadowmount_psplay_generated_source();') < BOOT.find('start_browser_shadowmount_selector()'))
ck('PSPLAY_SERVICE_ELF_UNCHANGED', '/data/PIZZA_HEN/payloads/PS-Play_v2.1.elf' in BOOT and 'optional_psplay_start' in BOOT)
ck('NO_SHADOWMOUNT_SOURCE_PATCH', 'ShadowMountPlus-1.6beta16-UPSTREAM-FROZEN/source' not in BUILD or 'patch ' not in BUILD.lower())
ck('R72529_TEST_ALIGNED', 'STORAGE_ENTRY_SEPARATE' in (ROOT/'TESTS/test_r72529_storage_dashboard.py').read_text())
ck('BUILD_TEST_HOOK', 'test_r725210_pkg_restore_psplay_shadowmount_cleanup.py' in BUILD)
ck('BUILD_METADATA', all(x in BUILD for x in (
    'R725210_PACKAGE_INSTALLER=R72528_BYTE_EXACT_RESTORED',
    'R725210_STORAGE_ENTRY=SEPARATE_TOP_LEVEL_SCREEN',
    'R725210_PSPLAY_NOTIFICATION=STALE_DATA_HOMEBREW_SOURCE_CLEANED_BEFORE_SHADOWMOUNT',
    'R725210_SHADOWMOUNT=PRISTINE_UNCHANGED')))

total=22
print(f"R7_25_2_10_PKG_RESTORE_PSPLAY_SHADOWMOUNT_CLEANUP={total-fail}/{total} {'PASS' if fail==0 else 'FAIL'}")
sys.exit(1 if fail else 0)
