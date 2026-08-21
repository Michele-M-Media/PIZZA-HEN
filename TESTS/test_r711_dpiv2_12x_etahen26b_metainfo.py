from pathlib import Path
import hashlib, re, sys
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'Source Code' / 'util' / 'source' / 'DirectPKGInstaller.cpp'
PRX = ROOT / 'Source Code' / 'shellui' / 'src' / 'prx.cpp'
POL = ROOT / 'Source Code' / 'shellui' / 'include' / 'onion_debug_settings_route_policy.hpp'
DOC = ROOT / 'DPIV2_12X_ETAHEN26B_METAINFO_REPAIR.md'
s = SRC.read_text()
checks=[]
def ck(name, ok):
    checks.append((name,bool(ok))); print(f'R711_{name}={"PASS" if ok else "FAIL"}')
ck('SOURCE_FINAL_SHA', hashlib.sha256(SRC.read_bytes()).hexdigest() == '5a14caa77e9e121eea5a5c3ebd2de40c6c4ad1736e79714b7c4a6b6bc2b54d69')
ck('FW_THRESHOLD_1220', 'fw >= 0x12200000u' in s)
ck('FW_RUNTIME_RESOLVER', 'kernel_get_fw_version() & 0xffff0000u' in s)
ck('ETAHEN26B_ZERO_METAINFO', 'arg1 = {};' in s and 'arg1.uri = url_value;' in s)
ck('LEGACY_METAINFO_PRESERVED', '.content_name = "etaHEN DPIv2"' in s and '.ex_uri = ""' in s)
ck('URL_INSTALL_CALL_PRESERVED', 'sceAppInstUtilInstallByPackage(&arg1, &pkg_info, &arg3)' in s)
ck('DPI_V2_PORT_PRESERVED', '12800' in s)
ck('APPINST_INIT_PRESERVED', 'sceAppInstUtilInitialize()' in s)
ck('UPLOAD_BRANCH_PRESERVED', 'etaHEN DPIv2 | ' in s and 'uploaded PKG' in s)
ck('NO_12X_ALT_BACKEND', 'DPIv2_12x_new' not in s and 'shellui_install_bridge' not in s)
ck('ONION_POLICY_PRESENT', 'old-route-11.x-plus' in POL.read_text())
ck('APPINST_DETOURS_STILL_DISABLED', '#if 0' in PRX.read_text() and 'AppInstUtilInstallByPackage_Hook' in PRX.read_text())
ck('DOC', DOC.exists() and 'ca60c615ba43d823bc5ccec86ef0b6b581aa8e79e73aaa4276cf92695049cbee' in DOC.read_text())
passed=sum(x for _,x in checks)
print(f'R7_11_DPIV2_12X_ETAHEN26B_METAINFO={passed}/{len(checks)} ' + ('PASS' if passed==len(checks) else 'FAIL'))
sys.exit(0 if passed==len(checks) else 1)
