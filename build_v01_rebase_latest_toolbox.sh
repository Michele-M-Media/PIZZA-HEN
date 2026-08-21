#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$SCRIPT_DIR/Source Code"
SM_DIR="$SCRIPT_DIR/ThirdParty/ShadowMountPlus-1.6beta16-UPSTREAM-FROZEN"
SM_ELF="$SM_DIR/shadowmountplus.elf"
SM_SOURCE_ZIP="$SM_DIR/ShadowMountPlus-1.6beta16.zip"
SM_EXPECTED_SHA="a35246fb3bb6042b25653b51cdcbc33254b40339342bf1d2dd0d2eceee2ca526"
SM_SOURCE_EXPECTED_SHA="5af04b9481545a869660aa1942d3396d890757660f29a702a2244823fa28ec23"
WEB_DIR="$SCRIPT_DIR/ThirdParty/websrv-0.34-UPSTREAM-FROZEN"
WEB_ELF="$WEB_DIR/websrv-ps5.elf"
WEB_SOURCE_ZIP="$WEB_DIR/websrv-0.34.zip"
WEB_EXPECTED_SHA="54730c867c6e1148536fdcb370e63a7762d989ea87b62488ad4caff64d43f263"
WEB_SOURCE_EXPECTED_SHA="cf89f500848d68a266655c5cea63831a32f5e489ddb93d898bb0b8699da8d5d0"
DR_DIR="$SCRIPT_DIR/ThirdParty/kstuff-dr-1.2-test1-UPSTREAM-FROZEN"
DR_ELF="$DR_DIR/kstuff-dr-1.2-test1.elf"
DR_SOURCE_ZIP="$DR_DIR/kstuff-lite-1.2-dr-test1.zip"
DR_EXPECTED_SHA="9c1b242eaed3704ef18be45d001a2c4ebf2d9222cfe3cbb0f0c3db33309abac9"
DR_SOURCE_EXPECTED_SHA="56f2a64fec342d6f5f8c9d29bbbbebae53dd1dea6836f1879347d5a4a16924ac"
FTP_DIR="$SCRIPT_DIR/ThirdParty/ftpsrv-0.21-UPSTREAM-FROZEN"
FTP_ELF="$FTP_DIR/ftpsrv-ps5.elf"
FTP_SOURCE_ZIP="$FTP_DIR/ftpsrv-0.21.zip"
FTP_EXPECTED_SHA="c580f0534ac6349dc5a4a5c656eaced537b4c2b18da51886d943cea6393436c8"
FTP_SOURCE_EXPECTED_SHA="b8e95cccf97ee46be320fede8662404de4f27a5f8f99770d151ddd3fbfc124f8"
DBG_DIR="$SCRIPT_DIR/ThirdParty/ps5debug-NG-1.3.0-UPSTREAM-FROZEN"
DBG_ELF="$DBG_DIR/ps5debug-NG_v1.3.0.elf"
DBG_SOURCE_ZIP="$DBG_DIR/ps5debug-NG-1.3.0.zip"
DBG_EXPECTED_SHA="8f75fb90b45d7cc4d59147e3323577d7264cf572c78a27f76722202f492ad16a"
DBG_SOURCE_EXPECTED_SHA="d2a115d907eb876a12d1335068eb874e7a8bb5b3d149db048b8acbe905a38701"
WEB_DST="$SRC_DIR/bootstrapper/assets/websrv-ps5.elf"
DR_DST="$SRC_DIR/bootstrapper/assets/kstuff-dr-1.2-test1.elf"
FTP_DST="$SRC_DIR/bootstrapper/assets/ftpsrv-ps5.elf"
DBG_DST="$SRC_DIR/bootstrapper/assets/ps5debug-NG_v1.3.0.elf"
BUILD_DIR="$SRC_DIR/build/pizza-hen-v01-rebase-latest-toolbox"
OUT_DIR="$SCRIPT_DIR/OUTPUT"
LOG_DIR="$SCRIPT_DIR/BUILD_LOGS"
STAMP="$(date +%Y%m%d-%H%M%S)"
LOG_FILE="$LOG_DIR/PIZZA_HEN_BUILD_${STAMP}.log"
RESULT_FILE="$LOG_DIR/PIZZA_HEN_BUILD_RESULT.txt"
KSTUFF_DST="$SRC_DIR/bootstrapper/assets/kstuff.elf"
SHADOW_DST="$SRC_DIR/bootstrapper/assets/shadowmountplus.elf"
KSTUFF_EXPECTED_SHA="b1dfe57f367a35374f605127915eda38c76a6ed5d1c729e427955798bd78c66a"
KSTUFF_SOURCE_ZIP="$SCRIPT_DIR/ThirdParty/kstuff-lite-1.10-UPSTREAM-USER-SUPPLIED/kstuff-lite-1.10.zip"
KSTUFF_SOURCE_EXPECTED_SHA="f96e7ddea315be7e15cbbc18ea1b53b9bb42c0ee3f9aa656eb1c80bce4a993a4"
FW_DEFINE="${PIZZA_HEN_FW_DEFINE:-0x1001}"
DOCTOR=0
[[ "${1:-}" == "--doctor" ]] && DOCTOR=1
CUSTOM_TOOLCHAIN="${PIZZA_HEN_TOOLCHAIN_FILE:-}"
CUSTOM_CMAKE_WRAPPER="${PIZZA_HEN_CMAKE_WRAPPER:-}"

mkdir -p "$LOG_DIR" "$OUT_DIR" "$SCRIPT_DIR/KSTUFF_INPUT"
exec > >(tee -a "$LOG_FILE") 2>&1
trap 'rc=$?; { echo "PIZZA_HEN_BUILD=FAIL"; echo "EXIT_CODE=$rc"; echo "LOG_FILE=$LOG_FILE"; } > "$RESULT_FILE"; exit $rc' ERR

echo "============================================================"
echo " PIZZA HEN v1.0 - MULTILANGUAGE + ONION + CHEATRUNNER 0.17 + DPIv2 12.x etaHEN 2.6B + FW12.20 offsets"
echo " Firmware runtime target: PS5 retail 10.01"
echo " SDK policy: capability-based, no release pinned"
echo "============================================================"
echo "DATE=$(date -Is 2>/dev/null || date)"
echo "SOURCE=$SRC_DIR"

auth_sdk() {
  local p="${1:-}"; [[ -n "$p" ]] || return 1
  # Capability-based acceptance: known current/legacy layouts OR an explicit
  # toolchain/wrapper override for future/alternate PS5 Payload SDK layouts.
  if [[ -n "$CUSTOM_TOOLCHAIN" && -f "$CUSTOM_TOOLCHAIN" ]]; then return 0; fi
  if [[ -n "$CUSTOM_CMAKE_WRAPPER" && -x "$CUSTOM_CMAKE_WRAPPER" ]]; then return 0; fi
  [[ -f "$p/toolchain/prospero.mk" || -f "$p/toolchain/prospero.cmake" || -f "$p/cmake/toolchain-ps5.cmake" || -x "$p/bin/prospero-cmake" ]]
}

SDK=""
SDK_SOURCE=""
for var in PIZZA_HEN_SDK PS5_PAYLOAD_SDK PS5SDK PAYLOAD_SDK; do
  val="${!var:-}"
  if [[ -n "$val" ]]; then
    if auth_sdk "$val"; then SDK="${val%/}"; SDK_SOURCE="ENV:$var"; break
    else echo "WARNING=$var points to an unsupported SDK layout: $val"; fi
  fi
done

if [[ -z "$SDK" ]]; then
  for p in /opt/ps5-payload-sdk "$HOME/ps5-payload-sdk" "$HOME/PS5_PAYLOAD_SDK"; do
    if auth_sdk "$p"; then SDK="$p"; SDK_SOURCE="AUTO_STANDARD"; break; fi
  done
fi

if [[ -z "$SDK" && -d /mnt/c/Users ]]; then
  mapfile -t roots < <(
    find /mnt/c/Users -maxdepth 9 -type f \
      \( -path '*/toolchain/prospero.cmake' -o -path '*/toolchain/prospero.mk' -o -path '*/cmake/toolchain-ps5.cmake' -o -path '*/bin/prospero-cmake' \) \
      -print 2>/dev/null | sed -E 's#/(toolchain/prospero\.(cmake|mk)|cmake/toolchain-ps5\.cmake|bin/prospero-cmake)$##' \
      | awk '!seen[$0]++' | sort -V
  )
  if ((${#roots[@]})); then SDK="${roots[-1]}"; SDK_SOURCE="AUTO_DISCOVERY_WSL"; fi
fi

if [[ -z "$SDK" ]]; then
  echo "ERROR=PS5_PAYLOAD_SDK_NOT_FOUND"
  echo "Set PIZZA_HEN_SDK or PS5_PAYLOAD_SDK to the SDK root."
  exit 21
fi

export PIZZA_HEN_SDK="$SDK"
export PS5_PAYLOAD_SDK="$SDK"
export PS5SDK="$SDK"
export PAYLOAD_SDK="$SDK"
echo "SDK_SOURCE=$SDK_SOURCE"
echo "SDK_ROOT=$SDK"
[[ -f "$SDK/toolchain/prospero.cmake" ]] && echo "SDK_CMAKE=current:toolchain/prospero.cmake"
[[ -f "$SDK/cmake/toolchain-ps5.cmake" ]] && echo "SDK_CMAKE_LEGACY=cmake/toolchain-ps5.cmake"
[[ -x "$SDK/bin/prospero-cmake" ]] && echo "SDK_CMAKE_COMPAT=bin/prospero-cmake"
[[ -f "$SDK/toolchain/prospero.mk" ]] && echo "SDK_MAKE=toolchain/prospero.mk"
[[ -n "$CUSTOM_TOOLCHAIN" && -f "$CUSTOM_TOOLCHAIN" ]] && echo "SDK_CMAKE_OVERRIDE=$CUSTOM_TOOLCHAIN"
[[ -n "$CUSTOM_CMAKE_WRAPPER" && -x "$CUSTOM_CMAKE_WRAPPER" ]] && echo "SDK_CMAKE_WRAPPER_OVERRIDE=$CUSTOM_CMAKE_WRAPPER"

for cmd in cmake python3 make file cp find; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "MISSING_TOOL=$cmd"; exit 23; }
done
if command -v sha256sum >/dev/null 2>&1; then HASHCMD=sha256sum; else HASHCMD='shasum -a 256'; fi
if command -v ninja >/dev/null 2>&1; then CMAKE_GENERATOR=Ninja; elif command -v make >/dev/null 2>&1; then CMAKE_GENERATOR='Unix Makefiles'; else echo MISSING_BUILD_TOOL; exit 23; fi

echo "CMAKE_GENERATOR=$CMAKE_GENERATOR"

# V0.1 source-grounded compile preflight: embedded_payloads.c uses this exact
# historical asset path. Do not enter CMake if the byte-exact v0.1 ELF is absent.
V01_PS5DEBUG_ELF="$SRC_DIR/daemon/assets/ps5debug.elf"
V01_PS5DEBUG_EXPECTED_SHA="dae56bf7a30caa5f4eee929ec6a3dd0051e6da1a3651d9b20c299f339f36e43f"
[[ -s "$V01_PS5DEBUG_ELF" ]] || { echo "V01_PS5DEBUG_PRECHECK=FAIL_MISSING"; echo "V01_PS5DEBUG_PATH=$V01_PS5DEBUG_ELF"; exit 31; }
V01_PS5DEBUG_SHA="$($HASHCMD "$V01_PS5DEBUG_ELF" | awk '{print $1}')"
[[ "$V01_PS5DEBUG_SHA" == "$V01_PS5DEBUG_EXPECTED_SHA" ]] || { echo "V01_PS5DEBUG_PRECHECK=FAIL_SHA"; echo "EXPECTED=$V01_PS5DEBUG_EXPECTED_SHA"; echo "ACTUAL=$V01_PS5DEBUG_SHA"; exit 32; }
echo "V01_PS5DEBUG_PRECHECK=PASS"
echo "V01_PS5DEBUG_PATH=$V01_PS5DEBUG_ELF"
echo "V01_PS5DEBUG_SHA256=$V01_PS5DEBUG_SHA"

verify_upstream_shadowmount() {
  [[ -s "$SM_ELF" ]] || { echo "SHADOWMOUNT_ERROR=UPSTREAM_ELF_MISSING"; return 1; }
  [[ -s "$SM_SOURCE_ZIP" ]] || { echo "SHADOWMOUNT_ERROR=UPSTREAM_SOURCE_ZIP_MISSING"; return 1; }
  local magic elf_sha src_sha
  magic="$(od -An -tx1 -N4 "$SM_ELF" | tr -d ' \n')"
  [[ "$magic" == "7f454c46" ]] || { echo "SHADOWMOUNT_ERROR=UPSTREAM_ELF_BAD_MAGIC"; return 1; }
  elf_sha="$($HASHCMD "$SM_ELF" | awk '{print $1}')"
  src_sha="$($HASHCMD "$SM_SOURCE_ZIP" | awk '{print $1}')"
  [[ "$elf_sha" == "$SM_EXPECTED_SHA" ]] || { echo "SHADOWMOUNT_ERROR=UPSTREAM_ELF_SHA256_MISMATCH"; echo "EXPECTED=$SM_EXPECTED_SHA"; echo "ACTUAL=$elf_sha"; return 1; }
  [[ "$src_sha" == "$SM_SOURCE_EXPECTED_SHA" ]] || { echo "SHADOWMOUNT_ERROR=UPSTREAM_SOURCE_SHA256_MISMATCH"; echo "EXPECTED=$SM_SOURCE_EXPECTED_SHA"; echo "ACTUAL=$src_sha"; return 1; }
  echo "SHADOWMOUNT_MODE=PRISTINE_UPSTREAM_PREBUILT"
  echo "SHADOWMOUNT_ELF_SHA256=$elf_sha"
  echo "SHADOWMOUNT_SOURCE_SHA256=$src_sha"
  echo "SHADOWMOUNT_SDK_DEPENDENCY=NONE_PREBUILT_RUNTIME"
}

verify_frozen_elf_source() {
  local label="$1" elf="$2" elf_expected="$3" srczip="$4" src_expected="$5"
  [[ -s "$elf" ]] || { echo "${label}_ERROR=ELF_MISSING"; return 1; }
  [[ -s "$srczip" ]] || { echo "${label}_ERROR=SOURCE_ZIP_MISSING"; return 1; }
  local magic elf_sha src_sha
  magic="$(od -An -tx1 -N4 "$elf" | tr -d ' \n')"
  [[ "$magic" == "7f454c46" ]] || { echo "${label}_ERROR=BAD_ELF_MAGIC"; return 1; }
  elf_sha="$($HASHCMD "$elf" | awk '{print $1}')"
  src_sha="$($HASHCMD "$srczip" | awk '{print $1}')"
  [[ "$elf_sha" == "$elf_expected" ]] || { echo "${label}_ERROR=ELF_SHA256_MISMATCH"; return 1; }
  [[ "$src_sha" == "$src_expected" ]] || { echo "${label}_ERROR=SOURCE_SHA256_MISMATCH"; return 1; }
  echo "${label}_ELF_SHA256=$elf_sha"
  echo "${label}_SOURCE_SHA256=$src_sha"
}

if ((DOCTOR)); then
  echo "[doctor] verifying pristine upstream ShadowMount artifacts..."
  verify_upstream_shadowmount
  echo "[doctor] verifying frozen websrv 0.34..."
  verify_frozen_elf_source WEBSRV "$WEB_ELF" "$WEB_EXPECTED_SHA" "$WEB_SOURCE_ZIP" "$WEB_SOURCE_EXPECTED_SHA"
  echo "[doctor] verifying frozen KStuff DR 1.2 test1..."
  verify_frozen_elf_source KSTUFF_DR "$DR_ELF" "$DR_EXPECTED_SHA" "$DR_SOURCE_ZIP" "$DR_SOURCE_EXPECTED_SHA"
  echo "[doctor] verifying frozen ftpsrv 0.21..."
  verify_frozen_elf_source FTPSRV "$FTP_ELF" "$FTP_EXPECTED_SHA" "$FTP_SOURCE_ZIP" "$FTP_SOURCE_EXPECTED_SHA"
  echo "[doctor] verifying frozen ps5debug-NG v1.3.0..."
  verify_frozen_elf_source PS5DEBUG_NG "$DBG_ELF" "$DBG_EXPECTED_SHA" "$DBG_SOURCE_ZIP" "$DBG_SOURCE_EXPECTED_SHA"
  grep -q 'KStuff Lite 1.10' "$SRC_DIR/bootstrapper/assets/kstuff_selector.js"
  grep -q 'KStuff DR 1.2' "$SRC_DIR/bootstrapper/assets/kstuff_selector.js"
  if grep -qi 'AUTO' "$SRC_DIR/bootstrapper/assets/kstuff_selector.js"; then echo "SELECTOR_ERROR=AUTO_MODE_PRESENT"; exit 30; fi
  echo "SELECTOR_MODE=TWO_CHOICES_NO_AUTO"
  echo "PIZZA_HEN_DOCTOR=PASS"
  exit 0
fi

# Current KStuff Lite 1.10 input preserved from the latest branch.
# This rebase does not alter the v0.1 etaHEN/ShellUI implementation.
KSTUFF_SRC="$SCRIPT_DIR/KSTUFF_INPUT/kstuff-v1.10-normal.elf"
[[ -s "$KSTUFF_SRC" ]] || { echo "KSTUFF_ERROR=USER_SUPPLIED_1_10_ELF_MISSING"; exit 24; }
MAGIC="$(od -An -tx1 -N4 "$KSTUFF_SRC" | tr -d ' \n')"
[[ "$MAGIC" == "7f454c46" ]] || { echo "KSTUFF_ERROR=INVALID_ELF_MAGIC"; exit 25; }
KSTUFF_SHA="$($HASHCMD "$KSTUFF_SRC" | awk '{print $1}')"
[[ "$KSTUFF_SHA" == "$KSTUFF_EXPECTED_SHA" ]] || { echo "KSTUFF_ERROR=SHA256_MISMATCH"; exit 26; }
[[ -s "$KSTUFF_SOURCE_ZIP" ]] || { echo "KSTUFF_ERROR=SOURCE_ZIP_MISSING"; exit 26; }
KSTUFF_SOURCE_SHA="$($HASHCMD "$KSTUFF_SOURCE_ZIP" | awk '{print $1}')"
[[ "$KSTUFF_SOURCE_SHA" == "$KSTUFF_SOURCE_EXPECTED_SHA" ]] || { echo "KSTUFF_ERROR=SOURCE_ZIP_SHA256_MISMATCH"; exit 26; }
cp -f "$KSTUFF_SRC" "$KSTUFF_DST"
echo "KSTUFF_BASELINE=UPSTREAM_LITE_1.10_CURRENT_INPUT"
echo "KSTUFF_SHA256=$KSTUFF_SHA"
echo "KSTUFF_SOURCE_SHA256=$KSTUFF_SOURCE_SHA"

echo "[selector] Verifying websrv 0.34 and KStuff DR 1.2 frozen inputs..."
verify_frozen_elf_source WEBSRV "$WEB_ELF" "$WEB_EXPECTED_SHA" "$WEB_SOURCE_ZIP" "$WEB_SOURCE_EXPECTED_SHA"
verify_frozen_elf_source KSTUFF_DR "$DR_ELF" "$DR_EXPECTED_SHA" "$DR_SOURCE_ZIP" "$DR_SOURCE_EXPECTED_SHA"
verify_frozen_elf_source FTPSRV "$FTP_ELF" "$FTP_EXPECTED_SHA" "$FTP_SOURCE_ZIP" "$FTP_SOURCE_EXPECTED_SHA"
verify_frozen_elf_source PS5DEBUG_NG "$DBG_ELF" "$DBG_EXPECTED_SHA" "$DBG_SOURCE_ZIP" "$DBG_SOURCE_EXPECTED_SHA"
cp -f "$WEB_ELF" "$WEB_DST"
cp -f "$DR_ELF" "$DR_DST"
cp -f "$FTP_ELF" "$FTP_DST"
cp -f "$DBG_ELF" "$DBG_DST"
WEB_SHA="$($HASHCMD "$WEB_ELF" | awk '{print $1}')"
DR_SHA="$($HASHCMD "$DR_ELF" | awk '{print $1}')"
FTP_SHA="$($HASHCMD "$FTP_ELF" | awk '{print $1}')"
DBG_SHA="$($HASHCMD "$DBG_ELF" | awk '{print $1}')"
echo "WEBSRV_MODE=UPSTREAM_0.34_PREBUILT_FROZEN"
echo "KSTUFF_SELECTOR=LITE_1.10_OR_DR_1.2_NO_AUTO"

# FIX20: ShadowMount runtime is the exact upstream 1.6beta16 ELF supplied by the user.
# It is intentionally NOT rebuilt or patched by the local SDK. This prevents SDK
# layout differences (for example source-vs-installed libkernel stubs) from
# changing upstream runtime behavior.
echo "[1/4] Verifying pristine upstream ShadowMountPlus..."
verify_upstream_shadowmount
SHADOW_ELF="$SM_ELF"
cp -f "$SHADOW_ELF" "$SHADOW_DST"
SHADOW_SHA="$($HASHCMD "$SHADOW_ELF" | awk '{print $1}')"
echo "SHADOWMOUNT_SHA256=$SHADOW_SHA"

echo "[sxml] Synchronizing encrypted ShellUI resources before static validation..."
(
  cd "$SRC_DIR"
  python3 shellui/assets/encryptxml.py
)
echo "SXML_PRETEST_SYNC=PASS"

echo "[2/4] Static source tests..."
python3 "$SCRIPT_DIR/TESTS/test_r3_dual_media_after_kstuff.py"
python3 "$SCRIPT_DIR/TESTS/test_r4_onion_multifw_ui_cleanup.py"
python3 "$SCRIPT_DIR/TESTS/test_r5_debug_services_cleanup.py"
python3 "$SCRIPT_DIR/TESTS/test_r7_1_modern_util_dependency_repair.py"
python3 "$SCRIPT_DIR/TESTS/test_r7_2_ce108262_preload_rollback.py"
python3 "$SCRIPT_DIR/TESTS/test_r7_6_1_plugin_scan_service_runtime_repair.py"
python3 "$SCRIPT_DIR/TESTS/test_r7_6_3_hidden_legacy_toolbox_hosts_restore.py"
python3 "$SCRIPT_DIR/TESTS/test_r7_7_v1_multilanguage.py"
python3 "$SCRIPT_DIR/TESTS/test_r78_kstuff_selector_i18n.py"
python3 "$SCRIPT_DIR/TESTS/test_r710_cheatrunner_integration.py"
python3 "$SCRIPT_DIR/TESTS/test_r711_dpiv2_12x_etahen26b_metainfo.py"
python3 "$SCRIPT_DIR/TESTS/test_r712_fw1220_phu_kstuff_offsets.py"
python3 "$SCRIPT_DIR/TESTS/test_r713_cheatrunner_game_options_shortcut.py"
python3 "$SCRIPT_DIR/TESTS/test_r7_6_2_1_ce108262_toolbox_autoinject_rollback.py"
python3 "$SCRIPT_DIR/TESTS/test_r7_5_3_1_static_gate_compile_repair.py"
python3 "$SCRIPT_DIR/TESTS/test_v01_rebase_latest_toolbox_debug_services_raw_bridge.py"
python3 "$SCRIPT_DIR/TESTS/test_fix26_ftp_after_shadowmount.py"
python3 "$SCRIPT_DIR/TESTS/test_fix27_ps5debug_ng_auto.py"
python3 "$SCRIPT_DIR/TESTS/test_fix28_ui_branding.py"
python3 "$SCRIPT_DIR/TESTS/test_fix29_cheat_repository.py"
python3 "$SCRIPT_DIR/TESTS/test_fix31_shellui_compile_repair.py"
python3 "$SCRIPT_DIR/TESTS/test_fix35_sxml_sync.py"
python3 "$SCRIPT_DIR/TESTS/test_fix37_menu_branding_margherita.py"
python3 "$SCRIPT_DIR/TESTS/test_fix39_multisdk_portability.py"
python3 "$SCRIPT_DIR/TESTS/test_fix41_direct_itemzflow.py"
python3 "$SCRIPT_DIR/TESTS/test_fix42_itemzflow_compile_repair.py"
python3 "$SCRIPT_DIR/TESTS/test_onion_shellcore_multifw_repair.py"
python3 "$SCRIPT_DIR/TESTS/test_onion_deep_audit_repair.py"

echo "[3/4] Configure PIZZA HEN..."
rm -rf "$BUILD_DIR"
CMAKE_ARGS=( -S "$SRC_DIR" -B "$BUILD_DIR" -G "$CMAKE_GENERATOR" -DV_FW="$FW_DEFINE" -DCMAKE_BUILD_TYPE=Debug -DPIZZA_HEN_SDK_ROOT="$SDK" )
if [[ -n "$CUSTOM_TOOLCHAIN" && -f "$CUSTOM_TOOLCHAIN" ]]; then
  CMAKE_ARGS+=( -DCMAKE_TOOLCHAIN_FILE="$CUSTOM_TOOLCHAIN" )
  cmake "${CMAKE_ARGS[@]}"
elif [[ -n "$CUSTOM_CMAKE_WRAPPER" && -x "$CUSTOM_CMAKE_WRAPPER" ]]; then
  "$CUSTOM_CMAKE_WRAPPER" "${CMAKE_ARGS[@]}"
elif [[ -f "$SDK/toolchain/prospero.cmake" ]]; then
  CMAKE_ARGS+=( -DCMAKE_TOOLCHAIN_FILE="$SDK/toolchain/prospero.cmake" )
  cmake "${CMAKE_ARGS[@]}"
elif [[ -f "$SDK/cmake/toolchain-ps5.cmake" ]]; then
  CMAKE_ARGS+=( -DCMAKE_TOOLCHAIN_FILE="$SDK/cmake/toolchain-ps5.cmake" )
  cmake "${CMAKE_ARGS[@]}"
elif [[ -x "$SDK/bin/prospero-cmake" ]]; then
  "$SDK/bin/prospero-cmake" "${CMAKE_ARGS[@]}"
else
  echo "ERROR=NO_CMAKE_TOOLCHAIN_FOR_SELECTED_SDK"; exit 28
fi

# Verify the exact .incbin path from the daemon build working directory.
# embedded_payloads.c contains: .incbin "../../../daemon/assets/ps5debug.elf"
mkdir -p "$BUILD_DIR/daemon"
V01_PS5DEBUG_ASM_PATH="$BUILD_DIR/daemon/../../../daemon/assets/ps5debug.elf"
[[ -s "$V01_PS5DEBUG_ASM_PATH" ]] || { echo "V01_PS5DEBUG_ASM_PATH=FAIL"; echo "EXPECTED_PATH=$V01_PS5DEBUG_ASM_PATH"; exit 33; }
V01_PS5DEBUG_ASM_SHA="$($HASHCMD "$V01_PS5DEBUG_ASM_PATH" | awk '{print $1}')"
[[ "$V01_PS5DEBUG_ASM_SHA" == "$V01_PS5DEBUG_EXPECTED_SHA" ]] || { echo "V01_PS5DEBUG_ASM_PATH=FAIL_SHA"; exit 34; }
echo "V01_PS5DEBUG_ASM_PATH=PASS"
echo "V01_PS5DEBUG_ASM_RESOLVED=$(readlink -f "$V01_PS5DEBUG_ASM_PATH" 2>/dev/null || printf '%s' "$V01_PS5DEBUG_ASM_PATH")"

echo "[4/4] Build PIZZA HEN..."
JOBS="${PIZZA_HEN_JOBS:-2}"
cmake --build "$BUILD_DIR" --target pizza_hen --parallel "$JOBS"

CHEATRUNNER_BUILT="$SRC_DIR/bin/CheatRunner.elf"
[[ -s "$CHEATRUNNER_BUILT" ]] || { echo "BUILD_ERROR=CHEATRUNNER_ELF_NOT_FOUND"; exit 35; }
CHEATRUNNER_SHA="$($HASHCMD "$CHEATRUNNER_BUILT" | awk '{print $1}')"
CHEATRUNNER_SIZE="$(wc -c < "$CHEATRUNNER_BUILT" | tr -d ' ')"
echo "CHEATRUNNER_BUILD=PASS"
echo "CHEATRUNNER_ELF=$CHEATRUNNER_BUILT"
echo "CHEATRUNNER_SIZE=$CHEATRUNNER_SIZE"
echo "CHEATRUNNER_SHA256=$CHEATRUNNER_SHA"

BUILT_ELF=""
for candidate in "$SRC_DIR/bin/PIZZA-HEN-v0.1-FIX45-PLUGIN-MANAGER-LIFECYCLE.elf" "$BUILD_DIR/bin/PIZZA-HEN-v0.1-FIX45-PLUGIN-MANAGER-LIFECYCLE.elf"; do
  [[ -s "$candidate" ]] && { BUILT_ELF="$candidate"; break; }
done
if [[ -z "$BUILT_ELF" ]]; then
  BUILT_ELF="$(find "$SRC_DIR" "$BUILD_DIR" -type f -name 'PIZZA-HEN-v0.1-FIX45-PLUGIN-MANAGER-LIFECYCLE.elf' -size +1k -print -quit || true)"
fi
[[ -n "$BUILT_ELF" && -s "$BUILT_ELF" ]] || { echo "BUILD_ERROR=FINAL_ELF_NOT_FOUND"; exit 29; }

FINAL_ELF="$OUT_DIR/PIZZA-HEN-v1.0.elf"
FINAL_BIN="$OUT_DIR/PIZZA-HEN-v1.0.bin"
cp -f "$BUILT_ELF" "$FINAL_ELF"
cp -f "$BUILT_ELF" "$FINAL_BIN"
PAYLOAD_SHA="$($HASHCMD "$FINAL_BIN" | awk '{print $1}')"
PAYLOAD_SIZE="$(wc -c < "$FINAL_BIN" | tr -d ' ')"

cat > "$RESULT_FILE" <<RESULT
PIZZA_HEN_BUILD=PASS
PIZZA_HEN_VERSION=1.0-MULTILANGUAGE-CHEATRUNNER-DPIV2-12X-ETAHEN26B-R712-FW1220
FIRMWARE_TARGET=10.01
FW_DEFINE=$FW_DEFINE
SDK_ROOT=$SDK
SDK_SOURCE=$SDK_SOURCE
SDK_POLICY=CAPABILITY_BASED_NO_RELEASE_PIN
KSTUFF_BASELINE=UPSTREAM_LITE_1.10_CURRENT_INPUT
KSTUFF_SHA256=$KSTUFF_SHA
KSTUFF_DR_BASELINE=1.2_TEST1_FROZEN
KSTUFF_DR_SHA256=$DR_SHA
WEBSRV_BASELINE=0.34_UPSTREAM_PREBUILT_FROZEN
WEBSRV_SHA256=$WEB_SHA
FTPSRV_BASELINE=0.21_UPSTREAM_PREBUILT_FROZEN
FTPSRV_SHA256=$FTP_SHA
FTPSRV_PORT=2121
PS5DEBUG_NG_BASELINE=1.3.0_UPSTREAM_PREBUILT_FROZEN
PS5DEBUG_NG_SHA256=$DBG_SHA
PS5DEBUG_NG_PORT=744
KSTUFF_SELECTOR=BROWSER_LITE_1.10_OR_DR_1.2_NO_AUTO
SHADOWMOUNT_BASELINE=1.6beta16_PRISTINE_UPSTREAM_PREBUILT_FROZEN
SHADOWMOUNT_SHA256=$SHADOW_SHA
CHEATRUNNER_BASELINE=0.17_SOURCE_COMMIT_9c75165182bedb9c21e9b58a1468caeb8a3fdb0f
CHEATRUNNER_MODE=TOOLBOX_ON_DEMAND_SOURCE_BUILT
CHEATRUNNER_PORT=9999
DPIV2_12X_METAINFO_POLICY=ETAHEN_2.6B_URI_ONLY_FROM_12.20
DPIV2_12X_REFERENCE_SHA256=ca60c615ba43d823bc5ccec86ef0b6b581aa8e79e73aaa4276cf92695049cbee
R712_FW1220_PHU_KSTUFF_OFFSETS=PASS
PHU_OVERLAY_12X_SHA256=af930375e1be960254ce2ac70fbd29230b9f67937cf69bca8b66520371bdbb3b
PHU_OVERLAY_12X_POLICY=12.00_TO_12.70_KSTUFF110_SHARED_FIELDS
KSTUFF_PAUSE_12X_SYSENTVEC=0xDCC978
KSTUFF_PAUSE_12X_SYSENTVEC_PS4=0xDCCAF0
CHEATRUNNER_SHA256=$CHEATRUNNER_SHA
CHEATRUNNER_SIZE=$CHEATRUNNER_SIZE
RUNTIME_SEQUENCE=BOOTSTRAP_WEBSRV_SELECTOR_ONE_KSTUFF_DUAL_MEDIA_SHADOWMOUNT_FTPSRV_PS5DEBUG_NG_DAEMONS_TOOLBOX_SHELLUI_HOOK_PRELOAD_CHEATRUNNER_ON_DEMAND
PAYLOAD=$FINAL_BIN
PAYLOAD_SIZE=$PAYLOAD_SIZE
PAYLOAD_SHA256=$PAYLOAD_SHA
BUILD_JOBS=$JOBS
CMAKE_GENERATOR=$CMAKE_GENERATOR
LOG_FILE=$LOG_FILE
RESULT
cat "$RESULT_FILE"
