#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$SCRIPT_DIR/Source Code"
SM_DIR="$SCRIPT_DIR/ThirdParty/ShadowMountPlus-1.6beta16-UPSTREAM-FROZEN"
SM_ELF="$SM_DIR/shadowmountplus.elf"
SM_SOURCE_ZIP="$SM_DIR/ShadowMountPlus-1.6beta16.zip"
SM_EXPECTED_SHA="a35246fb3bb6042b25653b51cdcbc33254b40339342bf1d2dd0d2eceee2ca526"
SM_SOURCE_EXPECTED_SHA="5af04b9481545a869660aa1942d3396d890757660f29a702a2244823fa28ec23"
SM_EXP_DIR="$SCRIPT_DIR/ThirdParty/ShadowMountPlus-1.7alpha8-EXPERIMENTAL-FROZEN"
SM_EXP_ELF="$SM_EXP_DIR/shadowmountplus.elf"
SM_EXP_SOURCE_ZIP="$SM_EXP_DIR/ShadowMountPlus-1.7alpha8.zip"
SM_EXP_EXPECTED_SHA="f15653fe90d81e5f82841ca693c0599d307c384d6454c1b0cc18190ae1ef4812"
SM_EXP_SOURCE_EXPECTED_SHA="144d227956d1d28ad1740a05d620ecf990ee6cc50b47ab86a7b258d1cca6cb25"
WEB_DIR="$SCRIPT_DIR/ThirdParty/websrv-0.34-UPSTREAM-FROZEN"
WEB_ELF="$WEB_DIR/websrv-ps5.elf"
WEB_SOURCE_ZIP="$WEB_DIR/websrv-0.34.zip"
WEB_EXPECTED_SHA="54730c867c6e1148536fdcb370e63a7762d989ea87b62488ad4caff64d43f263"
WEB_SOURCE_EXPECTED_SHA="cf89f500848d68a266655c5cea63831a32f5e489ddb93d898bb0b8699da8d5d0"
WEB_PIZZA_NO_TILE_SHA="16a18de9df60b4d726409121a2f24ea92616db03e1cc45fab49c8d05ae8b480c"
DR_DIR="$SCRIPT_DIR/ThirdParty/kstuff-dr-1.2-test1-UPSTREAM-FROZEN"
DR_ELF="$DR_DIR/kstuff-dr-1.2-test1.elf"
DR_SOURCE_ZIP="$DR_DIR/kstuff-lite-1.2-dr-test1.zip"
DR_EXPECTED_SHA="9c1b242eaed3704ef18be45d001a2c4ebf2d9222cfe3cbb0f0c3db33309abac9"
DR_SOURCE_EXPECTED_SHA="56f2a64fec342d6f5f8c9d29bbbbebae53dd1dea6836f1879347d5a4a16924ac"
KSTUFF_BASE_DIR="$SCRIPT_DIR/ThirdParty/kstuff-1.6.7-BASE-USER-SUPPLIED-FROZEN"
KSTUFF_BASE_ELF="$KSTUFF_BASE_DIR/kstuff-base-1.6.7.elf"
KSTUFF_BASE_SOURCE_ZIP="$KSTUFF_BASE_DIR/kstuff-1.6.7.zip"
KSTUFF_BASE_EXPECTED_SHA="f1c1f4b2b6395644af04cbe9828aba58586acf7aacb9e01113cac92ce16e3569"
KSTUFF_BASE_SOURCE_EXPECTED_SHA="9319f790b2be45e1de3e201a008f0f9a8ad9c2f3dac268c55bb82691daa6bbe4"
KSTUFF_BASE_DST="$SRC_DIR/bootstrapper/assets/kstuff-base-1.6.7.elf"
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
ELFLDR_DIR="$SCRIPT_DIR/ThirdParty/ps5-elfldr-0.24-148b71c-UPSTREAM-FROZEN"
ELFLDR_ELF="$ELFLDR_DIR/elfldr-ps5-v0.24-148b71c.elf"
ELFLDR_SOURCE_ZIP="$ELFLDR_DIR/ps5-elfldr-0.24-148b71c.zip"
ELFLDR_EXPECTED_SHA="6bf3a5416c84305f4e62cc952861f810806eb6613a3d24c4b35f947f2650ba33"
ELFLDR_SOURCE_EXPECTED_SHA="1445c355b8bce53a090b8e135efb3297c2b0b828927285e2ac233cb2b6a93935"
APR_DIR="$SCRIPT_DIR/ThirdParty/apr-emu-updater-1.4-USER-SUPPLIED-FROZEN"
APR_ELF="$APR_DIR/apr_emu_updater.elf"
APR_SOURCE_ZIP="$APR_DIR/apr-emu-updater-1.4.zip"
APR_EXPECTED_SHA="684a7e824e03f2402693641f347341a118fa0ac7a9573f212036a0a5337a8054"
APR_SOURCE_EXPECTED_SHA="db2743aab291f4bf51a90f0fd292d81de82949d67b78f433d6ed2a64b54a019b"
APR_PIZZA_NO_TILE_SHA="fcd9472ea50141a51e3d6663aee2eadbe99b9e6e0cedf1421b7c1d67f62727a9"
BACKPORK_DIR="$SCRIPT_DIR/ThirdParty/BackPork-0.1-USER-SUPPLIED-FROZEN"
BACKPORK_ELF="$BACKPORK_DIR/ps5-backpork.elf"
BACKPORK_EXPECTED_SHA="d74e4cd119b2bb1fd423f2f5b1c9a7f096b3e588c753af1ab48b983d56216a52"
GARLIC_DIR="$SCRIPT_DIR/ThirdParty/Garlic-SaveMgr-USER-SUPPLIED-FROZEN"
GARLIC_ELF="$GARLIC_DIR/garlic-savemgr.elf"
GARLIC_EXPECTED_SHA="124051ab3a762474720ae53187d2920bc96d6be1d69aa298e715667efc385a2f"
R719_DIR="$SCRIPT_DIR/ThirdParty/R7.19-USER-SUPPLIED-SERVICES-FROZEN"
FW_SPOOF_ELF="$R719_DIR/ps5-fw-spoof_v26616621599.elf"
FW_SPOOF_EXPECTED_SHA="f1754521caa92a6a1ac313a1b6c969ec49d67750e290ba99870958290a0961f0"
AIRPSX_ELF="$R719_DIR/airpsx_v0.19.elf"
AIRPSX_EXPECTED_SHA="ae025ca7727b3a8abf6a705903ca9116a6fa6e7f7ead606916109cf9044c5d63"
PS5UPLOAD_ELF="$R719_DIR/ps5upload_v5.4.8.elf"
PS5UPLOAD_EXPECTED_SHA="b255217ffcb5bc93a0ecdd4612927f241fbef3b3f936874223fcfba4cff17cf5"
NP_FAKE_SIGNIN_ELF="$R719_DIR/np-fake-signin_v1.3.elf"
NP_FAKE_SIGNIN_EXPECTED_SHA="f5c66fcb9e3f512e5463a7123d819b87f063d9955639366fa7ad26a2f0abefa4"
WKALI_ELF="$R719_DIR/webkit-autoloader-installer_v0.4.0-pre-00e1028.elf"
WKALI_EXPECTED_SHA="b920bc73133764a9847975a402b6f3bd4d9d97c797159153ccc5bcb98b6ee025"
APP_DUMPER_ELF="$R719_DIR/ps5-app-dumper_v1.11.elf"
APP_DUMPER_EXPECTED_SHA="18483751ebaea6879b020a9dd87c0a4fb4f1bf09f3708d950362a483f78cc0d0"
GC_DIR="$SCRIPT_DIR/ThirdParty/PS5-Game-Compressor-1.0.4-USER-SUPPLIED-FROZEN"
GC_ELF="$GC_DIR/game-compressor.elf"
GC_SOURCE_ZIP="$GC_DIR/PS5-Game-Compressor-1.0.4.zip"
GC_EXPECTED_SHA="e55e90aaade13b6e0d4316c1597ef90a21b67a06475c3e25de054224bc1e941b"
GC_SOURCE_EXPECTED_SHA="daf2adaa586ab9234e984c7f2a9e706764f408fe0f714bba34f17347e99e66b2"
GC_PIZZA_NO_TILE_SHA="535aa4a8e951c04b98df33eb7d476dbcb6cbec080c00dfc8d574f1e61b233ac3"
ELFLDR_DST="$SRC_DIR/lib/elfldr.bin"
APR_DST="$SRC_DIR/bootstrapper/assets/apr_emu_updater.elf"
BACKPORK_DST="$SRC_DIR/bootstrapper/assets/ps5-backpork.elf"
GARLIC_DST="$SRC_DIR/bootstrapper/assets/garlic-savemgr.elf"
FW_SPOOF_DST="$SRC_DIR/bootstrapper/assets/ps5-fw-spoof_v26616621599.elf"
AIRPSX_DST="$SRC_DIR/bootstrapper/assets/airpsx_v0.19.elf"
PS5UPLOAD_DST="$SRC_DIR/bootstrapper/assets/ps5upload_v5.4.8.elf"
NP_FAKE_SIGNIN_DST="$SRC_DIR/bootstrapper/assets/np-fake-signin_v1.3.elf"
WKALI_DST="$SRC_DIR/bootstrapper/assets/webkit-autoloader-installer_v0.4.0-pre-00e1028.elf"
APP_DUMPER_DST="$SRC_DIR/bootstrapper/assets/ps5-app-dumper_v1.11.elf"
GC_DST="$SRC_DIR/bootstrapper/assets/game-compressor.elf"
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
REMOTE_PLAY_ELF="$SCRIPT_DIR/ThirdParty/ps5-remoteplay-get-pin-v0.1.1-USER-SUPPLIED-FROZEN/ps5-remoteplay-get-pin_v0.1.1.elf"
REMOTE_PLAY_EXPECTED_SHA="1d611c1856dd2f4b4b6cb42ead1128a7f08a26585788f92de79fa4f67d721472"
REMOTE_PLAY_DST="$SRC_DIR/bootstrapper/assets/rp-get-pin.elf"
SVT_PLAY_ELF="$SCRIPT_DIR/ThirdParty/SVT-Play-v0.2-USER-SUPPLIED-FROZEN/svtplay_v0.2.elf"
SVT_PLAY_EXPECTED_SHA="5bdf25142512f25dc6269bd7c90a914001fcef5e731125a74aa23c1a8d91810f"
PROSPERO_ELF="$SCRIPT_DIR/ThirdParty/ProsperoPlayer-v1.0-USER-SUPPLIED-FROZEN/ProsperoPlayer_v1.0.elf"
PROSPERO_EXPECTED_SHA="40b9955273982cd563e1b16bd428ea6a9c399e7d4bc55b220fe223948572cdad"
PROSPERO_DST="$SRC_DIR/bootstrapper/assets/ProsperoPlayer_v1.0.elf"
PSPLAY_ELF="$SCRIPT_DIR/ThirdParty/PS-Play-v2.1-USER-SUPPLIED-FROZEN/PS-Play_v2.1.elf"
PSPLAY_EXPECTED_SHA="e3392379d5bc6ca4e44cb0d2a1d8921083b2c3ea480725f68378831874542d8d"
PSPLAY_DST="$SRC_DIR/bootstrapper/assets/PS-Play_v2.1.elf"
BFPLAYER_ELF="$SCRIPT_DIR/ThirdParty/BFplayer-v0.1.0-alpha.44-USER-SUPPLIED-FROZEN/BFplayer-standalone_v0.1.0-alpha.44.elf"
BFPLAYER_EXPECTED_SHA="0d028deb145d6fc9a5b55d43a45e072919178fbb261c66cd914ebcfb0b3b05c0"
BFPLAYER_DST="$SRC_DIR/bootstrapper/assets/BFplayer-standalone_v0.1.0-alpha.44.elf"
CHUKEI_DNS_ELF="$SCRIPT_DIR/ThirdParty/Chukei-DNS-v0.9.0-USER-SUPPLIED-FROZEN/Chukei_DNS_v0.9.0.elf"
CHUKEI_DNS_EXPECTED_SHA="0cf13e1ed87b57ffa4fdcfca5d9afe1572be29b4f632677cedf17657a972d750"
CHUKEI_DNS_DST="$SRC_DIR/bootstrapper/assets/Chukei_DNS_v0.9.0.elf"
NANODNS_ELF="$SCRIPT_DIR/ThirdParty/nanoDNS-v0.4-USER-SUPPLIED-FROZEN/nanoDNS_v0.4.elf"
NANODNS_EXPECTED_SHA="18a93655c59ad32e371e14c86f32d14fbd1fbc47a0e907f3e0b6667efb3ad964"
NANODNS_DST="$SRC_DIR/bootstrapper/assets/nanoDNS_v0.4.elf"
FAN03_DIR="$SCRIPT_DIR/ThirdParty/ps5-fan-control-v0.3-USER-SUPPLIED-FROZEN"
FAN03_ELF="$FAN03_DIR/ps5-fan-control-v0.3.elf"
FAN03_EXPECTED_SHA="b10b6b9b9c00efed8bf9202a83b6cb762345d1f84130a419eff7139250026b36"
FAN03_SOURCE_ZIP="$FAN03_DIR/ps5-fan-control-0.3.zip"
FAN03_SOURCE_EXPECTED_SHA="c85639057b5218445f3f5526c49b3df334d5f5ab99bbdfe8c4c9bf957b89e2e6"
FAN03_INI="$FAN03_DIR/fan_control.ini"
FAN03_INI_EXPECTED_SHA="71496515fde36be968623c7cda317b0ebd142c83c06343836ae2274184e9b266"
FAN03_DST="$SRC_DIR/daemon/assets/ps5-fan-control-v0.3.elf"
POORDS4_DIR="$SCRIPT_DIR/ThirdParty/PoorDS4-0.1.0-rc38-USER-SUPPLIED-FROZEN"
POORDS4_MAIN_ELF="$POORDS4_DIR/PoorDS4rc38.elf"
POORDS4_MAIN_EXPECTED_SHA="62d21fe837ee53dd4291e45d99259d4557def05e2d4196ab54e020ba28b5399e"
POORDS4_STATUS_ELF="$POORDS4_DIR/PoorDS4-status.elf"
POORDS4_STATUS_EXPECTED_SHA="c26a35a2c9ba9074ad33cf27a5afbd05536978518c546552df21d512b07a273d"
POORDS4_STOP_ELF="$POORDS4_DIR/PoorDS4-stop.elf"
POORDS4_STOP_EXPECTED_SHA="bf9f1dec35edcffe3744fbc69cb7d4601f6df3cef72fab36c38fd249e736107a"
POORDS4_SOURCE_ZIP="$POORDS4_DIR/PoorDS4-0.1.0-rc38.zip"
POORDS4_SOURCE_EXPECTED_SHA="5634b504b0eae5302a875346dc30449e05fd5932ef18baea8e046415a19ea41b"
POORDS4_SUMS="$POORDS4_DIR/SHA256SUMS.txt"
POORDS4_SUMS_EXPECTED_SHA="ec0533ec626a276d77bfc04325a2963fdd421c26549845c46607eb1227bf580a"
POORDS4_MAIN_DST="$SRC_DIR/daemon/assets/PoorDS4rc38.elf"
POORDS4_STATUS_DST="$SRC_DIR/daemon/assets/PoorDS4-status.elf"
POORDS4_STOP_DST="$SRC_DIR/daemon/assets/PoorDS4-stop.elf"
UNRAR_ELF="$SCRIPT_DIR/ThirdParty/unrar-ps5-v1.4.0-USER-SUPPLIED-FROZEN/unrar-ps5_v1.4.0.elf"
UNRAR_EXPECTED_SHA="2ef04b0bc8fc1932b29da1a53336c40ed0a3f6a945a0746bef2e5dde52149701"
UNRAR_DST="$SRC_DIR/bootstrapper/assets/unrar-ps5_v1.4.0.elf"
PS_GAME_STATE_ELF="$SCRIPT_DIR/ThirdParty/PS-Game-State-Lib-v0.1-USER-SUPPLIED-FROZEN/PS_Game_State_Lib_v0.1.elf"
PS_GAME_STATE_EXPECTED_SHA="a550e1494b0f8be3b244f8820ee8d899442d33a936f9ded6203a0318c7afdba8"
PS_GAME_STATE_DST="$SRC_DIR/bootstrapper/assets/PS_Game_State_Lib_v0.1.elf"
GHOSTPAD_ELF="$SCRIPT_DIR/ThirdParty/Ghostpad-v1.0.0-USER-SUPPLIED-FROZEN/Ghostpad_v1.0.0.elf"
GHOSTPAD_EXPECTED_SHA="94d43a8db7ec9df6e18f0a0da25aac0f60e1a0b14d35bfff261f6f5cdeabdba1"
GHOSTPAD_DST="$SRC_DIR/bootstrapper/assets/Ghostpad_v1.0.0.elf"
GHOSTCONTROL_ELF="$SCRIPT_DIR/ThirdParty/Ghostcontrol-v1.0.5-USER-SUPPLIED-FROZEN/Ghostcontrol-PS5-USB-Controller-Patcher_v1.0.5.elf"
GHOSTCONTROL_EXPECTED_SHA="69271d91f27397c9ad42150129639ce452ecb405021108f42c6c87926123a6f1"
GHOSTCONTROL_DST="$SRC_DIR/bootstrapper/assets/Ghostcontrol-PS5-USB-Controller-Patcher_v1.0.5.elf"
PS_DISCORD_ELF="$SCRIPT_DIR/ThirdParty/PS-DiscordPresence-v0.01-USER-SUPPLIED-FROZEN/PS-DiscordPresence_v0.01.elf"
PS_DISCORD_EXPECTED_SHA="375cf619ea6f6c594ea2b79ecbb98704723522d07e51c877687876d5fe589afb"
PS_DISCORD_DST="$SRC_DIR/bootstrapper/assets/PS-DiscordPresence_v0.01.elf"
CUSTOM_TOOL_ORIG="$SCRIPT_DIR/ThirdParty/PS5-Custom-Tool-Manager-vCustom-USER-SUPPLIED-ORIGINAL/PS5-Custom-Tool-Manager-_vCustom.elf"
CUSTOM_TOOL_ORIG_EXPECTED_SHA="297824ceaf6ea53fde57550adf9b5c2fc44c63ef60e8196ab92d351d1615d9cb"
CUSTOM_TOOL_DERIVED="$SCRIPT_DIR/ThirdParty/THEMES-AVATAR-INTEGRATED-DERIVED/PS5-Custom-Tool-Manager-_vCustom-pizza-web-only.elf"
CUSTOM_TOOL_DERIVED_EXPECTED_SHA="ecdf8a8eaa47f59bfe5b419dcb3f60bd3dc68deef9f36a5e36c125f3e71987b7"
CUSTOM_TOOL_DST="$SRC_DIR/bootstrapper/assets/PS5-Custom-Tool-Manager-_vCustom-pizza-web-only.elf"
WALLPAPER_MODDER_ORIG="$SCRIPT_DIR/ThirdParty/ps5-wallpaper-modd-v1.0-USER-SUPPLIED-ORIGINAL/ps5-wallpaper-modd_v1.0.elf"
WALLPAPER_MODDER_ORIG_EXPECTED_SHA="b18a866bac9deff45b921b7d3ea6143d541117b56c666d817ecdc81961829139"
WALLPAPER_MODDER_DERIVED="$SCRIPT_DIR/ThirdParty/THEMES-AVATAR-INTEGRATED-DERIVED/ps5-wallpaper-modd_v1.0-pizza-web-only.elf"
WALLPAPER_MODDER_DERIVED_EXPECTED_SHA="a2fa5e9c8ecb794fed189bcd204008ea446a12c2d1381fa601734b3d915d5360"
WALLPAPER_MODDER_DST="$SRC_DIR/bootstrapper/assets/ps5-wallpaper-modd_v1.0-pizza-web-only.elf"
WFM_ELF="$SCRIPT_DIR/ThirdParty/ps5-web-file-manager-v1.5-USER-SUPPLIED-FROZEN/ps5-web-file-manager_v1.5.elf"
WFM_EXPECTED_SHA="9a7d7e5c685900d7f916cdc08cb6f7ea7e9cf5a4576f2799157b3f251deedf3c"
WFM_PIZZA_NO_TILE_SHA="d0bc7620051079fff40147c4bcf364fda054b7e5bef9193abfba2ef76710006b"
WFM_DST="$SRC_DIR/bootstrapper/assets/web-file-mgr.elf"
LINUX_LOADER_ELF="$SCRIPT_DIR/ThirdParty/ps5-linux-loader-v2.4-USER-SUPPLIED-FROZEN/ps5-linux-loader_v2.4.elf"
LINUX_LOADER_EXPECTED_SHA="51382795b486f7c5a3681648d457d129088311fc3f9601aeaff78dc72fafcf1d"
LINUX_LOADER_DST="$SRC_DIR/bootstrapper/assets/ps5-linux-loader.elf"
PEGASUS_ELF="$SCRIPT_DIR/ThirdParty/pegasus-dl-v1.7.0-USER-SUPPLIED-FROZEN/pegasus-dl_v1.7.0.elf"
PEGASUS_EXPECTED_SHA="cb2a4b3c248323f2432ce118cb1bf4975146035239ce9b571a9bdb51b3fee226"
PEGASUS_PIZZA_NO_TILE_SHA="730cb6be1d16e93f7b06b269e8fa56f45866ab2fc51ac2ef1e90bbf341a1c02a"
PEGASUS_DST="$SRC_DIR/bootstrapper/assets/pegasus-dl.elf"
SPECTRUM_ELF="$SCRIPT_DIR/ThirdParty/Spectrum-Library-v1.4.2-USER-SUPPLIED-FROZEN/Spectrum-Library_v1.4.2.elf"
SPECTRUM_EXPECTED_SHA="54755ce62d99be610afe364e26de05eaa9e2d92192cda525790a563c6296261f"
SPECTRUM_PIZZA_NO_TILE_SHA="e747a5b01c468e1bbe7d09558751c90237e47a4d6bf932e1d174a4934b1afd4c"
SPECTRUM_DST="$SRC_DIR/bootstrapper/assets/Spectrum-Library.elf"
PIZZA_REPO_FROZEN_DIR="$SCRIPT_DIR/ThirdParty/Payload-Repository-USER-SUPPLIED-FROZEN"
PIZZA_REPO_SOURCE="$PIZZA_REPO_FROZEN_DIR/payloads-original.json"
PIZZA_REPO_SOURCE_EXPECTED_SHA="38d799b96dd9e006d1f676f74f77264aaf0958506a772992cc62834661c05a59"
PIZZA_REPO_RAR="$PIZZA_REPO_FROZEN_DIR/Nuovo Archivio WinRAR(1).rar"
PIZZA_REPO_RAR_EXPECTED_SHA="e28561cad71ae226ebcc8275ce6c22a722db092696f6fc8fcbe2a5357855024d"
PIZZA_REPO_JSON="$SRC_DIR/util/assets/pizzahen_payloads.json"
PIZZA_REPO_JSON_EXPECTED_SHA="cb730e5ad03fa4de038991c18249473d2b4328ebc51dcce3e11613aff3ad873f"
PIZZA_REPO_HEADER="$SRC_DIR/util/include/pizzahen_payloads_builtin.hpp"
PIZZA_REPO_HEADER_EXPECTED_SHA="cff209028bdfb9f82aeff633be4bbb9da63589aab69fde949797fa79b7e69611"
PIZZA_REPO_GENERATOR="$SCRIPT_DIR/TOOLS/generate_pizzahen_payload_repository.py"
KSTUFF_DST="$SRC_DIR/bootstrapper/assets/kstuff.elf"
SHADOW_DST="$SRC_DIR/bootstrapper/assets/shadowmountplus.elf"
SHADOW_EXP_DST="$SRC_DIR/bootstrapper/assets/shadowmountplus-experimental.elf"
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
echo " PIZZA HEN v2.00 - Complete I18N Hardware Baseline"
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

verify_frozen_elf_only() {
  local label="$1" elf="$2" elf_expected="$3"
  [[ -s "$elf" ]] || { echo "${label}_ERROR=ELF_MISSING"; return 1; }
  local magic elf_sha
  magic="$(od -An -tx1 -N4 "$elf" | tr -d ' \n')"
  [[ "$magic" == "7f454c46" ]] || { echo "${label}_ERROR=BAD_ELF_MAGIC"; return 1; }
  elf_sha="$($HASHCMD "$elf" | awk '{print $1}')"
  [[ "$elf_sha" == "$elf_expected" ]] || { echo "${label}_ERROR=ELF_SHA256_MISMATCH"; echo "EXPECTED=$elf_expected"; echo "ACTUAL=$elf_sha"; return 1; }
  echo "${label}_ELF_SHA256=$elf_sha"
}

if ((DOCTOR)); then
  echo "[doctor] verifying pristine upstream ShadowMount artifacts..."
  verify_upstream_shadowmount
  echo "[doctor] verifying experimental ShadowMountPlus 1.7alpha8 artifacts..."
  verify_frozen_elf_source SHADOWMOUNT_EXPERIMENTAL "$SM_EXP_ELF" "$SM_EXP_EXPECTED_SHA" "$SM_EXP_SOURCE_ZIP" "$SM_EXP_SOURCE_EXPECTED_SHA"
  echo "[doctor] verifying frozen websrv 0.34..."
  verify_frozen_elf_source WEBSRV "$WEB_ELF" "$WEB_EXPECTED_SHA" "$WEB_SOURCE_ZIP" "$WEB_SOURCE_EXPECTED_SHA"
  echo "[doctor] verifying frozen KStuff DR 1.2 test1..."
  verify_frozen_elf_source KSTUFF_DR "$DR_ELF" "$DR_EXPECTED_SHA" "$DR_SOURCE_ZIP" "$DR_SOURCE_EXPECTED_SHA"
  verify_frozen_elf_source KSTUFF_BASE "$KSTUFF_BASE_ELF" "$KSTUFF_BASE_EXPECTED_SHA" "$KSTUFF_BASE_SOURCE_ZIP" "$KSTUFF_BASE_SOURCE_EXPECTED_SHA"
  echo "[doctor] verifying frozen ftpsrv 0.21..."
  verify_frozen_elf_source FTPSRV "$FTP_ELF" "$FTP_EXPECTED_SHA" "$FTP_SOURCE_ZIP" "$FTP_SOURCE_EXPECTED_SHA"
  echo "[doctor] verifying frozen ps5debug-NG v1.3.0..."
  verify_frozen_elf_source PS5DEBUG_NG "$DBG_ELF" "$DBG_EXPECTED_SHA" "$DBG_SOURCE_ZIP" "$DBG_SOURCE_EXPECTED_SHA"
  verify_frozen_elf_source ELFLDR024 "$ELFLDR_ELF" "$ELFLDR_EXPECTED_SHA" "$ELFLDR_SOURCE_ZIP" "$ELFLDR_SOURCE_EXPECTED_SHA"
  verify_frozen_elf_source APR_EMU_UPDATER "$APR_ELF" "$APR_EXPECTED_SHA" "$APR_SOURCE_ZIP" "$APR_SOURCE_EXPECTED_SHA"
  verify_frozen_elf_only BACKPORK "$BACKPORK_ELF" "$BACKPORK_EXPECTED_SHA"
  verify_frozen_elf_only GARLIC_SAVEMGR "$GARLIC_ELF" "$GARLIC_EXPECTED_SHA"
  verify_frozen_elf_only FW_SPOOF "$FW_SPOOF_ELF" "$FW_SPOOF_EXPECTED_SHA"
  verify_frozen_elf_only AIRPSX "$AIRPSX_ELF" "$AIRPSX_EXPECTED_SHA"
  verify_frozen_elf_only PS5UPLOAD "$PS5UPLOAD_ELF" "$PS5UPLOAD_EXPECTED_SHA"
  verify_frozen_elf_only NP_FAKE_SIGNIN "$NP_FAKE_SIGNIN_ELF" "$NP_FAKE_SIGNIN_EXPECTED_SHA"
  verify_frozen_elf_only WKALI "$WKALI_ELF" "$WKALI_EXPECTED_SHA"
  verify_frozen_elf_only APP_DUMPER "$APP_DUMPER_ELF" "$APP_DUMPER_EXPECTED_SHA"
  verify_frozen_elf_only REMOTE_PLAY "$REMOTE_PLAY_ELF" "$REMOTE_PLAY_EXPECTED_SHA"
  verify_frozen_elf_only SVT_PLAY "$SVT_PLAY_ELF" "$SVT_PLAY_EXPECTED_SHA"
  verify_frozen_elf_only PROSPERO_PLAYER "$PROSPERO_ELF" "$PROSPERO_EXPECTED_SHA"
  verify_frozen_elf_only PS_PLAY "$PSPLAY_ELF" "$PSPLAY_EXPECTED_SHA"
  verify_frozen_elf_only BFPLAYER "$BFPLAYER_ELF" "$BFPLAYER_EXPECTED_SHA"
  verify_frozen_elf_only CHUKEI_DNS "$CHUKEI_DNS_ELF" "$CHUKEI_DNS_EXPECTED_SHA"
  verify_frozen_elf_only NANODNS "$NANODNS_ELF" "$NANODNS_EXPECTED_SHA"
verify_frozen_elf_source PS5_FAN_CONTROL_V03 "$FAN03_ELF" "$FAN03_EXPECTED_SHA" "$FAN03_SOURCE_ZIP" "$FAN03_SOURCE_EXPECTED_SHA"
[[ "$($HASHCMD "$FAN03_INI" | awk '{print $1}')" == "$FAN03_INI_EXPECTED_SHA" ]] || { echo "PS5_FAN_CONTROL_V03_ERROR=INI_SHA256_MISMATCH"; exit 78; }
  verify_frozen_elf_source PS5_FAN_CONTROL_V03 "$FAN03_ELF" "$FAN03_EXPECTED_SHA" "$FAN03_SOURCE_ZIP" "$FAN03_SOURCE_EXPECTED_SHA"
  [[ "$($HASHCMD "$FAN03_INI" | awk '{print $1}')" == "$FAN03_INI_EXPECTED_SHA" ]] || { echo "PS5_FAN_CONTROL_V03_ERROR=INI_SHA256_MISMATCH"; exit 78; }
  verify_frozen_elf_source POORDS4_RC38 "$POORDS4_MAIN_ELF" "$POORDS4_MAIN_EXPECTED_SHA" "$POORDS4_SOURCE_ZIP" "$POORDS4_SOURCE_EXPECTED_SHA"
  verify_frozen_elf_only POORDS4_STATUS "$POORDS4_STATUS_ELF" "$POORDS4_STATUS_EXPECTED_SHA"
  verify_frozen_elf_only POORDS4_STOP "$POORDS4_STOP_ELF" "$POORDS4_STOP_EXPECTED_SHA"
  [[ "$($HASHCMD "$POORDS4_SUMS" | awk '{print $1}')" == "$POORDS4_SUMS_EXPECTED_SHA" ]] || { echo "POORDS4_ERROR=SHA256SUMS_MISMATCH"; exit 78; }
  verify_frozen_elf_only UNRAR_PS5 "$UNRAR_ELF" "$UNRAR_EXPECTED_SHA"
  verify_frozen_elf_only PS_GAME_STATE_LIB "$PS_GAME_STATE_ELF" "$PS_GAME_STATE_EXPECTED_SHA"
  verify_frozen_elf_only GHOSTPAD "$GHOSTPAD_ELF" "$GHOSTPAD_EXPECTED_SHA"
  verify_frozen_elf_only GHOSTCONTROL "$GHOSTCONTROL_ELF" "$GHOSTCONTROL_EXPECTED_SHA"
  verify_frozen_elf_only PS_DISCORD_PRESENCE "$PS_DISCORD_ELF" "$PS_DISCORD_EXPECTED_SHA"
  verify_frozen_elf_only CUSTOM_TOOL_ORIGINAL "$CUSTOM_TOOL_ORIG" "$CUSTOM_TOOL_ORIG_EXPECTED_SHA"
  verify_frozen_elf_only WALLPAPER_MODDER_ORIGINAL "$WALLPAPER_MODDER_ORIG" "$WALLPAPER_MODDER_ORIG_EXPECTED_SHA"
  python3 "$SCRIPT_DIR/TOOLS/build_themes_avatar_web_only_variants.py"
  verify_frozen_elf_only CUSTOM_TOOL_WEB_ONLY "$CUSTOM_TOOL_DERIVED" "$CUSTOM_TOOL_DERIVED_EXPECTED_SHA"
  verify_frozen_elf_only WALLPAPER_MODDER_WEB_ONLY "$WALLPAPER_MODDER_DERIVED" "$WALLPAPER_MODDER_DERIVED_EXPECTED_SHA"
  verify_frozen_elf_only WEB_FILE_MANAGER "$WFM_ELF" "$WFM_EXPECTED_SHA"
  verify_frozen_elf_only LINUX_LOADER "$LINUX_LOADER_ELF" "$LINUX_LOADER_EXPECTED_SHA"
  verify_frozen_elf_only PEGASUS_DL "$PEGASUS_ELF" "$PEGASUS_EXPECTED_SHA"
  verify_frozen_elf_only SPECTRUM_LIBRARY "$SPECTRUM_ELF" "$SPECTRUM_EXPECTED_SHA"
verify_frozen_elf_source GAME_COMPRESSOR "$GC_ELF" "$GC_EXPECTED_SHA" "$GC_SOURCE_ZIP" "$GC_SOURCE_EXPECTED_SHA"
  grep -q 'KStuff Lite 1.10' "$SRC_DIR/bootstrapper/assets/kstuff_selector.js"
  grep -q 'KStuff DR 1.2' "$SRC_DIR/bootstrapper/assets/kstuff_selector.js"
  grep -q 'KStuff 1.6.7' "$SRC_DIR/bootstrapper/assets/kstuff_selector.js"
  if grep -qi 'AUTO' "$SRC_DIR/bootstrapper/assets/kstuff_selector.js"; then echo "SELECTOR_ERROR=AUTO_MODE_PRESENT"; exit 30; fi
  echo "SELECTOR_MODE=THREE_CHOICES_NO_AUTO"
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
verify_frozen_elf_source KSTUFF_BASE "$KSTUFF_BASE_ELF" "$KSTUFF_BASE_EXPECTED_SHA" "$KSTUFF_BASE_SOURCE_ZIP" "$KSTUFF_BASE_SOURCE_EXPECTED_SHA"
verify_frozen_elf_source FTPSRV "$FTP_ELF" "$FTP_EXPECTED_SHA" "$FTP_SOURCE_ZIP" "$FTP_SOURCE_EXPECTED_SHA"
verify_frozen_elf_source PS5DEBUG_NG "$DBG_ELF" "$DBG_EXPECTED_SHA" "$DBG_SOURCE_ZIP" "$DBG_SOURCE_EXPECTED_SHA"
verify_frozen_elf_source ELFLDR024 "$ELFLDR_ELF" "$ELFLDR_EXPECTED_SHA" "$ELFLDR_SOURCE_ZIP" "$ELFLDR_SOURCE_EXPECTED_SHA"
verify_frozen_elf_source APR_EMU_UPDATER "$APR_ELF" "$APR_EXPECTED_SHA" "$APR_SOURCE_ZIP" "$APR_SOURCE_EXPECTED_SHA"
verify_frozen_elf_only BACKPORK "$BACKPORK_ELF" "$BACKPORK_EXPECTED_SHA"
verify_frozen_elf_only GARLIC_SAVEMGR "$GARLIC_ELF" "$GARLIC_EXPECTED_SHA"
verify_frozen_elf_only FW_SPOOF "$FW_SPOOF_ELF" "$FW_SPOOF_EXPECTED_SHA"
verify_frozen_elf_only AIRPSX "$AIRPSX_ELF" "$AIRPSX_EXPECTED_SHA"
verify_frozen_elf_only PS5UPLOAD "$PS5UPLOAD_ELF" "$PS5UPLOAD_EXPECTED_SHA"
verify_frozen_elf_only NP_FAKE_SIGNIN "$NP_FAKE_SIGNIN_ELF" "$NP_FAKE_SIGNIN_EXPECTED_SHA"
verify_frozen_elf_only WKALI "$WKALI_ELF" "$WKALI_EXPECTED_SHA"
verify_frozen_elf_only APP_DUMPER "$APP_DUMPER_ELF" "$APP_DUMPER_EXPECTED_SHA"
verify_frozen_elf_only SVT_PLAY "$SVT_PLAY_ELF" "$SVT_PLAY_EXPECTED_SHA"
verify_frozen_elf_only PROSPERO_PLAYER "$PROSPERO_ELF" "$PROSPERO_EXPECTED_SHA"
verify_frozen_elf_only PS_PLAY "$PSPLAY_ELF" "$PSPLAY_EXPECTED_SHA"
verify_frozen_elf_only BFPLAYER "$BFPLAYER_ELF" "$BFPLAYER_EXPECTED_SHA"
verify_frozen_elf_only CHUKEI_DNS "$CHUKEI_DNS_ELF" "$CHUKEI_DNS_EXPECTED_SHA"
verify_frozen_elf_only NANODNS "$NANODNS_ELF" "$NANODNS_EXPECTED_SHA"
verify_frozen_elf_source POORDS4_RC38 "$POORDS4_MAIN_ELF" "$POORDS4_MAIN_EXPECTED_SHA" "$POORDS4_SOURCE_ZIP" "$POORDS4_SOURCE_EXPECTED_SHA"
verify_frozen_elf_only POORDS4_STATUS "$POORDS4_STATUS_ELF" "$POORDS4_STATUS_EXPECTED_SHA"
verify_frozen_elf_only POORDS4_STOP "$POORDS4_STOP_ELF" "$POORDS4_STOP_EXPECTED_SHA"
[[ "$($HASHCMD "$POORDS4_SUMS" | awk '{print $1}')" == "$POORDS4_SUMS_EXPECTED_SHA" ]] || { echo "POORDS4_ERROR=SHA256SUMS_MISMATCH"; exit 78; }
verify_frozen_elf_only UNRAR_PS5 "$UNRAR_ELF" "$UNRAR_EXPECTED_SHA"
verify_frozen_elf_only PS_GAME_STATE_LIB "$PS_GAME_STATE_ELF" "$PS_GAME_STATE_EXPECTED_SHA"
verify_frozen_elf_only GHOSTPAD "$GHOSTPAD_ELF" "$GHOSTPAD_EXPECTED_SHA"
verify_frozen_elf_only GHOSTCONTROL "$GHOSTCONTROL_ELF" "$GHOSTCONTROL_EXPECTED_SHA"
verify_frozen_elf_only PS_DISCORD_PRESENCE "$PS_DISCORD_ELF" "$PS_DISCORD_EXPECTED_SHA"
verify_frozen_elf_only CUSTOM_TOOL_ORIGINAL "$CUSTOM_TOOL_ORIG" "$CUSTOM_TOOL_ORIG_EXPECTED_SHA"
verify_frozen_elf_only WALLPAPER_MODDER_ORIGINAL "$WALLPAPER_MODDER_ORIG" "$WALLPAPER_MODDER_ORIG_EXPECTED_SHA"
python3 "$SCRIPT_DIR/TOOLS/build_themes_avatar_web_only_variants.py"
verify_frozen_elf_only CUSTOM_TOOL_WEB_ONLY "$CUSTOM_TOOL_DERIVED" "$CUSTOM_TOOL_DERIVED_EXPECTED_SHA"
verify_frozen_elf_only WALLPAPER_MODDER_WEB_ONLY "$WALLPAPER_MODDER_DERIVED" "$WALLPAPER_MODDER_DERIVED_EXPECTED_SHA"
verify_frozen_elf_only WEB_FILE_MANAGER "$WFM_ELF" "$WFM_EXPECTED_SHA"
verify_frozen_elf_only LINUX_LOADER "$LINUX_LOADER_ELF" "$LINUX_LOADER_EXPECTED_SHA"
verify_frozen_elf_only PEGASUS_DL "$PEGASUS_ELF" "$PEGASUS_EXPECTED_SHA"
verify_frozen_elf_only SPECTRUM_LIBRARY "$SPECTRUM_ELF" "$SPECTRUM_EXPECTED_SHA"
echo "[no-pkg] Building PIZZA HEN integrated no-tile variants..."
python3 "$SCRIPT_DIR/TOOLS/build_integrated_no_tile_variants.py"
[[ "$("$HASHCMD" "$WEB_DST" | awk '{print $1}')" == "$WEB_PIZZA_NO_TILE_SHA" ]] || { echo "NO_TILE_ERROR=WEBSRV_DERIVED_SHA"; exit 37; }
[[ "$("$HASHCMD" "$APR_DST" | awk '{print $1}')" == "$APR_PIZZA_NO_TILE_SHA" ]] || { echo "NO_TILE_ERROR=APR_DERIVED_SHA"; exit 38; }
[[ "$("$HASHCMD" "$GC_DST" | awk '{print $1}')" == "$GC_PIZZA_NO_TILE_SHA" ]] || { echo "NO_TILE_ERROR=GAME_COMPRESSOR_DERIVED_SHA"; exit 39; }
[[ "$("$HASHCMD" "$WFM_DST" | awk '{print $1}')" == "$WFM_PIZZA_NO_TILE_SHA" ]] || { echo "NO_TILE_ERROR=WEB_FILE_MANAGER_DERIVED_SHA"; exit 40; }
[[ "$("$HASHCMD" "$PEGASUS_DST" | awk '{print $1}')" == "$PEGASUS_PIZZA_NO_TILE_SHA" ]] || { echo "NO_TILE_ERROR=PEGASUS_DERIVED_SHA"; exit 41; }
[[ "$("$HASHCMD" "$SPECTRUM_DST" | awk '{print $1}')" == "$SPECTRUM_PIZZA_NO_TILE_SHA" ]] || { echo "NO_TILE_ERROR=SPECTRUM_DERIVED_SHA"; exit 42; }
cp -f "$DR_ELF" "$DR_DST"
cp -f "$KSTUFF_BASE_ELF" "$KSTUFF_BASE_DST"
cp -f "$FTP_ELF" "$FTP_DST"
cp -f "$DBG_ELF" "$DBG_DST"
cp -f "$ELFLDR_ELF" "$ELFLDR_DST"
cp -f "$BACKPORK_ELF" "$BACKPORK_DST"
cp -f "$GARLIC_ELF" "$GARLIC_DST"
cp -f "$FW_SPOOF_ELF" "$FW_SPOOF_DST"
cp -f "$AIRPSX_ELF" "$AIRPSX_DST"
cp -f "$PS5UPLOAD_ELF" "$PS5UPLOAD_DST"
cp -f "$NP_FAKE_SIGNIN_ELF" "$NP_FAKE_SIGNIN_DST"
cp -f "$WKALI_ELF" "$WKALI_DST"
cp -f "$APP_DUMPER_ELF" "$APP_DUMPER_DST"
cp -f "$REMOTE_PLAY_ELF" "$REMOTE_PLAY_DST"
cp -f "$PROSPERO_ELF" "$PROSPERO_DST"
cp -f "$PSPLAY_ELF" "$PSPLAY_DST"
cp -f "$BFPLAYER_ELF" "$BFPLAYER_DST"
cp -f "$CHUKEI_DNS_ELF" "$CHUKEI_DNS_DST"
cp -f "$NANODNS_ELF" "$NANODNS_DST"
cp -f "$FAN03_ELF" "$FAN03_DST"
cp -f "$POORDS4_MAIN_ELF" "$POORDS4_MAIN_DST"
cp -f "$POORDS4_STATUS_ELF" "$POORDS4_STATUS_DST"
cp -f "$POORDS4_STOP_ELF" "$POORDS4_STOP_DST"
cp -f "$UNRAR_ELF" "$UNRAR_DST"
cp -f "$PS_GAME_STATE_ELF" "$PS_GAME_STATE_DST"
cp -f "$GHOSTPAD_ELF" "$GHOSTPAD_DST"
cp -f "$GHOSTCONTROL_ELF" "$GHOSTCONTROL_DST"
cp -f "$PS_DISCORD_ELF" "$PS_DISCORD_DST"
cp -f "$CUSTOM_TOOL_DERIVED" "$CUSTOM_TOOL_DST"
cp -f "$WALLPAPER_MODDER_DERIVED" "$WALLPAPER_MODDER_DST"
cp -f "$LINUX_LOADER_ELF" "$LINUX_LOADER_DST"
WEB_UPSTREAM_SHA="$($HASHCMD "$WEB_ELF" | awk '{print $1}')"
WEB_SHA="$($HASHCMD "$WEB_DST" | awk '{print $1}')"
DR_SHA="$($HASHCMD "$DR_ELF" | awk '{print $1}')"
KSTUFF_BASE_SHA="$($HASHCMD "$KSTUFF_BASE_ELF" | awk '{print $1}')"
FTP_SHA="$($HASHCMD "$FTP_ELF" | awk '{print $1}')"
DBG_SHA="$($HASHCMD "$DBG_ELF" | awk '{print $1}')"
ELFLDR_SHA="$($HASHCMD "$ELFLDR_ELF" | awk '{print $1}')"
APR_UPSTREAM_SHA="$($HASHCMD "$APR_ELF" | awk '{print $1}')"
APR_SHA="$($HASHCMD "$APR_DST" | awk '{print $1}')"
BACKPORK_SHA="$($HASHCMD "$BACKPORK_ELF" | awk '{print $1}')"
GARLIC_SHA="$($HASHCMD "$GARLIC_ELF" | awk '{print $1}')"
FW_SPOOF_SHA="$($HASHCMD "$FW_SPOOF_ELF" | awk '{print $1}')"
AIRPSX_SHA="$($HASHCMD "$AIRPSX_ELF" | awk '{print $1}')"
PS5UPLOAD_SHA="$($HASHCMD "$PS5UPLOAD_ELF" | awk '{print $1}')"
NP_FAKE_SIGNIN_SHA="$($HASHCMD "$NP_FAKE_SIGNIN_ELF" | awk '{print $1}')"
WKALI_SHA="$($HASHCMD "$WKALI_ELF" | awk '{print $1}')"
APP_DUMPER_SHA="$($HASHCMD "$APP_DUMPER_ELF" | awk '{print $1}')"
REMOTE_PLAY_SHA="$($HASHCMD "$REMOTE_PLAY_ELF" | awk '{print $1}')"
SVT_PLAY_SHA="$($HASHCMD "$SVT_PLAY_ELF" | awk '{print $1}')"
PROSPERO_SHA="$($HASHCMD "$PROSPERO_DST" | awk '{print $1}')"
PSPLAY_SHA="$($HASHCMD "$PSPLAY_DST" | awk '{print $1}')"
BFPLAYER_SHA="$($HASHCMD "$BFPLAYER_DST" | awk '{print $1}')"
CHUKEI_DNS_SHA="$($HASHCMD "$CHUKEI_DNS_DST" | awk '{print $1}')"
NANODNS_SHA="$($HASHCMD "$NANODNS_DST" | awk '{print $1}')"
FAN03_SHA="$($HASHCMD "$FAN03_DST" | awk '{print $1}')"
FAN03_INI_SHA="$($HASHCMD "$FAN03_INI" | awk '{print $1}')"
POORDS4_MAIN_SHA="$($HASHCMD "$POORDS4_MAIN_DST" | awk '{print $1}')"
POORDS4_STATUS_SHA="$($HASHCMD "$POORDS4_STATUS_DST" | awk '{print $1}')"
POORDS4_STOP_SHA="$($HASHCMD "$POORDS4_STOP_DST" | awk '{print $1}')"
UNRAR_SHA="$($HASHCMD "$UNRAR_DST" | awk '{print $1}')"
PS_GAME_STATE_SHA="$($HASHCMD "$PS_GAME_STATE_DST" | awk '{print $1}')"
GHOSTPAD_SHA="$($HASHCMD "$GHOSTPAD_DST" | awk '{print $1}')"
GHOSTCONTROL_SHA="$($HASHCMD "$GHOSTCONTROL_DST" | awk '{print $1}')"
PS_DISCORD_SHA="$($HASHCMD "$PS_DISCORD_DST" | awk '{print $1}')"
CUSTOM_TOOL_ORIG_SHA="$($HASHCMD "$CUSTOM_TOOL_ORIG" | awk '{print $1}')"
CUSTOM_TOOL_DERIVED_SHA="$($HASHCMD "$CUSTOM_TOOL_DST" | awk '{print $1}')"
WALLPAPER_MODDER_ORIG_SHA="$($HASHCMD "$WALLPAPER_MODDER_ORIG" | awk '{print $1}')"
WALLPAPER_MODDER_DERIVED_SHA="$($HASHCMD "$WALLPAPER_MODDER_DST" | awk '{print $1}')"
WFM_UPSTREAM_SHA="$($HASHCMD "$WFM_ELF" | awk '{print $1}')"
WFM_SHA="$($HASHCMD "$WFM_DST" | awk '{print $1}')"
LINUX_LOADER_SHA="$($HASHCMD "$LINUX_LOADER_DST" | awk '{print $1}')"
PEGASUS_UPSTREAM_SHA="$($HASHCMD "$PEGASUS_ELF" | awk '{print $1}')"
PEGASUS_SHA="$($HASHCMD "$PEGASUS_DST" | awk '{print $1}')"
SPECTRUM_UPSTREAM_SHA="$($HASHCMD "$SPECTRUM_ELF" | awk '{print $1}')"
SPECTRUM_SHA="$($HASHCMD "$SPECTRUM_DST" | awk '{print $1}')"
GC_UPSTREAM_SHA="$($HASHCMD "$GC_ELF" | awk '{print $1}')"
GC_SHA="$($HASHCMD "$GC_DST" | awk '{print $1}')"
echo "ELFLDR024_SHA256=$ELFLDR_SHA"
echo "APR_EMU_UPDATER_SHA256=$APR_SHA"
echo "BACKPORK_SHA256=$BACKPORK_SHA"
echo "GARLIC_SAVEMGR_SHA256=$GARLIC_SHA"
echo "FW_SPOOF_SHA256=$FW_SPOOF_SHA"
echo "AIRPSX_SHA256=$AIRPSX_SHA"
echo "PS5UPLOAD_SHA256=$PS5UPLOAD_SHA"
echo "NP_FAKE_SIGNIN_SHA256=$NP_FAKE_SIGNIN_SHA"
echo "WKALI_SHA256=$WKALI_SHA"
echo "APP_DUMPER_SHA256=$APP_DUMPER_SHA"
echo "GAME_COMPRESSOR_SHA256=$GC_SHA"
echo "CHUKEI_DNS_SHA256=$CHUKEI_DNS_SHA"
echo "NANODNS_SHA256=$NANODNS_SHA"
echo "UNRAR_PS5_SHA256=$UNRAR_SHA"
echo "PS_GAME_STATE_LIB_SHA256=$PS_GAME_STATE_SHA"
echo "GHOSTPAD_SHA256=$GHOSTPAD_SHA"
echo "GHOSTCONTROL_SHA256=$GHOSTCONTROL_SHA"
echo "PS_DISCORD_PRESENCE_SHA256=$PS_DISCORD_SHA"
echo "CUSTOM_TOOL_MANAGER_ORIGINAL_SHA256=$CUSTOM_TOOL_ORIG_SHA"
echo "CUSTOM_TOOL_MANAGER_WEB_ONLY_SHA256=$CUSTOM_TOOL_DERIVED_SHA"
echo "WALLPAPER_MODDER_ORIGINAL_SHA256=$WALLPAPER_MODDER_ORIG_SHA"
echo "WALLPAPER_MODDER_WEB_ONLY_SHA256=$WALLPAPER_MODDER_DERIVED_SHA"
echo "WEBSRV_MODE=PIZZA_INTEGRATED_0.34_NO_PKG_NO_TILE_DERIVED_FROM_FROZEN_UPSTREAM"
echo "KSTUFF_SELECTOR=LITE_1.10_OR_DR_1.2_OR_BASE_1.6.7_NO_AUTO"

# FIX20: ShadowMount runtime is the exact upstream 1.6beta16 ELF supplied by the user.
# It is intentionally NOT rebuilt or patched by the local SDK. This prevents SDK
# layout differences (for example source-vs-installed libkernel stubs) from
# changing upstream runtime behavior.
echo "[1/4] Verifying Stable + Experimental ShadowMountPlus inputs..."
verify_upstream_shadowmount
verify_frozen_elf_source SHADOWMOUNT_EXPERIMENTAL "$SM_EXP_ELF" "$SM_EXP_EXPECTED_SHA" "$SM_EXP_SOURCE_ZIP" "$SM_EXP_SOURCE_EXPECTED_SHA"
SHADOW_ELF="$SM_ELF"
cp -f "$SHADOW_ELF" "$SHADOW_DST"
cp -f "$SM_EXP_ELF" "$SHADOW_EXP_DST"
SHADOW_SHA="$($HASHCMD "$SHADOW_ELF" | awk '{print $1}')"
SHADOW_EXP_SHA="$($HASHCMD "$SM_EXP_ELF" | awk '{print $1}')"
echo "SHADOWMOUNT_STABLE_SHA256=$SHADOW_SHA"
echo "SHADOWMOUNT_EXPERIMENTAL_SHA256=$SHADOW_EXP_SHA"

echo "[sxml] Synchronizing encrypted ShellUI resources before static validation..."
(
  cd "$SRC_DIR"
  python3 shellui/assets/encryptxml.py
)
echo "SXML_PRETEST_SYNC=PASS"

echo "[repo] Verifying and generating PIZZA HEN Payload Repository..."
[[ -s "$PIZZA_REPO_SOURCE" ]] || { echo "PIZZA_REPO_ERROR=SOURCE_MISSING"; exit 71; }
[[ -s "$PIZZA_REPO_RAR" ]] || { echo "PIZZA_REPO_ERROR=RAR_MISSING"; exit 72; }
[[ -x "$PIZZA_REPO_GENERATOR" ]] || { echo "PIZZA_REPO_ERROR=GENERATOR_MISSING"; exit 73; }
PIZZA_REPO_SOURCE_SHA="$($HASHCMD "$PIZZA_REPO_SOURCE" | awk '{print $1}')"
PIZZA_REPO_RAR_SHA="$($HASHCMD "$PIZZA_REPO_RAR" | awk '{print $1}')"
[[ "$PIZZA_REPO_SOURCE_SHA" == "$PIZZA_REPO_SOURCE_EXPECTED_SHA" ]] || { echo "PIZZA_REPO_ERROR=SOURCE_SHA_MISMATCH"; exit 74; }
[[ "$PIZZA_REPO_RAR_SHA" == "$PIZZA_REPO_RAR_EXPECTED_SHA" ]] || { echo "PIZZA_REPO_ERROR=RAR_SHA_MISMATCH"; exit 75; }
python3 "$PIZZA_REPO_GENERATOR" --source "$PIZZA_REPO_SOURCE" --json-out "$PIZZA_REPO_JSON" --header-out "$PIZZA_REPO_HEADER"
PIZZA_REPO_JSON_SHA="$($HASHCMD "$PIZZA_REPO_JSON" | awk '{print $1}')"
PIZZA_REPO_HEADER_SHA="$($HASHCMD "$PIZZA_REPO_HEADER" | awk '{print $1}')"
[[ "$PIZZA_REPO_JSON_SHA" == "$PIZZA_REPO_JSON_EXPECTED_SHA" ]] || { echo "PIZZA_REPO_ERROR=JSON_SHA_MISMATCH"; exit 76; }
[[ "$PIZZA_REPO_HEADER_SHA" == "$PIZZA_REPO_HEADER_EXPECTED_SHA" ]] || { echo "PIZZA_REPO_ERROR=HEADER_SHA_MISMATCH"; exit 77; }
echo "PIZZA_REPO_SOURCE_SHA256=$PIZZA_REPO_SOURCE_SHA"
echo "PIZZA_REPO_JSON_SHA256=$PIZZA_REPO_JSON_SHA"
echo "PIZZA_REPO_HEADER_SHA256=$PIZZA_REPO_HEADER_SHA"
echo "PIZZA_REPO_MODE=BUILTIN_PIZZA_HEN_ELF_ONLY"

echo "R72523_TOOLBOX_REMOTE_PLAY=REMOVED_NO_RUNTIME_CHANGE"
echo "R72523_TOOLBOX_LINUX_LOADER=REMOVED_NO_RUNTIME_CHANGE"
echo "R72523_TOOLBOX_SVT_PLAY=REMOVED_NO_RUNTIME_CHANGE"

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
python3 "$SCRIPT_DIR/TESTS/test_r714_shadowmount_dual_selector.py"
python3 "$SCRIPT_DIR/TESTS/test_r7141_incbin_compile_repair.py"
python3 "$SCRIPT_DIR/TESTS/test_r715_shadow_close_elfldr_apr.py"
python3 "$SCRIPT_DIR/TESTS/test_r7151_elfldr_switch_notify.py"
python3 "$SCRIPT_DIR/TESTS/test_r7152_elfldr_port_state_repair.py"
python3 "$SCRIPT_DIR/TESTS/test_r716_homebrew_channel.py"
python3 "$SCRIPT_DIR/TESTS/test_r717_backpork_garlic_services.py"
python3 "$SCRIPT_DIR/TESTS/test_r718_kstuff_base_shadow_skip_dump_installer.py"
python3 "$SCRIPT_DIR/TESTS/test_r7181_full_i18n.py"
python3 "$SCRIPT_DIR/TESTS/test_r719_six_services_full_i18n.py"
python3 "$SCRIPT_DIR/TESTS/test_r720_game_compressor_full_i18n.py"
python3 "$SCRIPT_DIR/TESTS/test_r7201_auto_launcher_behavior_repair.py"
python3 "$SCRIPT_DIR/TESTS/test_r7202_full_toolbox_no_pkg_integration.py"
python3 "$SCRIPT_DIR/TESTS/test_r723_pizzahen_payload_repository.py"
python3 "$SCRIPT_DIR/TESTS/test_r72522_dns_tools.py"
python3 "$SCRIPT_DIR/TESTS/test_r72523_toolbox_remove_remote_linux_svt.py"
python3 "$SCRIPT_DIR/TESTS/test_r72524_dns_service_lifecycle_repair.py"
python3 "$SCRIPT_DIR/TESTS/test_r72525_themes_avatar_web_integration.py"
python3 "$SCRIPT_DIR/TESTS/test_r72526_dns_original_notify_autostart_repair.py"
python3 "$SCRIPT_DIR/TESTS/test_r72527_services_original_elf_integration.py"
python3 "$SCRIPT_DIR/TESTS/test_r72528_psplay_autostart_remove_remote_garlic.py"
python3 "$SCRIPT_DIR/TESTS/test_r72529_storage_dashboard.py"
python3 "$SCRIPT_DIR/TESTS/test_r725210_pkg_restore_psplay_shadowmount_cleanup.py"
python3 "$SCRIPT_DIR/TESTS/test_r725211_dns_plain_separate_payloads.py"
python3 "$SCRIPT_DIR/TESTS/test_r725212_dns_services_original_elf_move.py"
python3 "$SCRIPT_DIR/TESTS/test_r725213_debug_services_hardware_launcher_restore.py"
python3 "$SCRIPT_DIR/TESTS/test_r725214_fan_target_dual_option.py"
python3 "$SCRIPT_DIR/TESTS/test_r725215_fan_control_v03_target_ui.py"
python3 "$SCRIPT_DIR/TESTS/test_r725216_poords4_tools_integration.py"
python3 "$SCRIPT_DIR/TESTS/test_v200_complete_i18n_hardware_baseline.py"
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

FINAL_ELF="$OUT_DIR/PIZZA-HEN-v2.00.elf"
FINAL_BIN="$OUT_DIR/PIZZA-HEN-v2.00.bin"
cp -f "$BUILT_ELF" "$FINAL_ELF"
cp -f "$BUILT_ELF" "$FINAL_BIN"
PAYLOAD_SHA="$($HASHCMD "$FINAL_BIN" | awk '{print $1}')"
PAYLOAD_SIZE="$(wc -c < "$FINAL_BIN" | tr -d ' ')"

cat > "$RESULT_FILE" <<RESULT
PIZZA_HEN_BUILD=PASS
PIZZA_HEN_VERSION=2.00-COMPLETE-I18N-HARDWARE-BASELINE
FIRMWARE_TARGET=10.01
FW_DEFINE=$FW_DEFINE
SDK_ROOT=$SDK
SDK_SOURCE=$SDK_SOURCE
SDK_POLICY=CAPABILITY_BASED_NO_RELEASE_PIN
KSTUFF_BASELINE=UPSTREAM_LITE_1.10_CURRENT_INPUT
KSTUFF_SHA256=$KSTUFF_SHA
KSTUFF_DR_BASELINE=1.2_TEST1_FROZEN
KSTUFF_DR_SHA256=$DR_SHA
KSTUFF_BASELINE_167=BASE_USER_SUPPLIED_FROZEN_FW_3XX_TO_10_01
KSTUFF_BASE_167_SHA256=$KSTUFF_BASE_SHA
WEBSRV_BASELINE=0.34_UPSTREAM_PREBUILT_FROZEN
WEBSRV_UPSTREAM_SHA256=$WEB_UPSTREAM_SHA
WEBSRV_PIZZA_INTEGRATED_SHA256=$WEB_SHA
WEBSRV_LAUNCHER=DISABLED_NO_PKG_NO_TILE
FTPSRV_BASELINE=0.21_UPSTREAM_PREBUILT_FROZEN
FTPSRV_SHA256=$FTP_SHA
FTPSRV_PORT=2121
PS5DEBUG_NG_BASELINE=1.3.0_UPSTREAM_PREBUILT_FROZEN
PS5DEBUG_NG_SHA256=$DBG_SHA
PS5DEBUG_NG_PORT=744
KSTUFF_SELECTOR=BROWSER_LITE_1.10_OR_DR_1.2_OR_BASE_1.6.7_NO_AUTO
SHADOWMOUNT_BASELINE=1.6beta16_PRISTINE_UPSTREAM_PREBUILT_FROZEN
SHADOWMOUNT_SHA256=$SHADOW_SHA
SHADOWMOUNT_EXPERIMENTAL_BASELINE=1.7alpha8_USER_SUPPLIED_PREBUILT_FROZEN
SHADOWMOUNT_EXPERIMENTAL_SHA256=$SHADOW_EXP_SHA
R715_SHADOW_SELECTOR_AUTO_CLOSE=GO_HOME_AFTER_REQUEST_COMMIT
ELFLDR_BASELINE=0.24_148b71c_UPSTREAM_PREBUILT_FROZEN
ELFLDR_SHA256=$ELFLDR_SHA
ELFLDR_PORT=9021
ELFLDR_MODE=TOOLBOX_SERVICES_ON_DEMAND
APR_EMU_UPDATER_BASELINE=1.4_USER_SUPPLIED_PREBUILT_FROZEN
APR_EMU_UPDATER_UPSTREAM_SHA256=$APR_UPSTREAM_SHA
APR_EMU_UPDATER_PIZZA_INTEGRATED_SHA256=$APR_SHA
APR_EMU_UPDATER_WEBUI_PORT=6971
APR_EMU_UPDATER_MODE=TOOLBOX_ON_DEMAND_NO_PKG_NO_TILE
APR_EMU_UPDATER_LAUNCHER=DISABLED_AUTO_THREAD_AND_TILE_ENDPOINT
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
R7151_ELFLDR_UI=SWITCH_ON_OFF
R7151_ELFLDR_NOTIFY=START_STOP_PIZZA_HEN_NOTIFICATION
R7152_ELFLDR_STATE=TCP_127_0_0_1_9021
R7152_ELFLDR_STABILIZATION=POLL_24X250MS
R716_HOMEBREW_CHANNEL=WEBSRV_0_34_INDEX_HTML_DIRECT_BROWSER
R716_HOMEBREW_CHANNEL_LAUNCHER=DISABLED_IN_PIZZA_INTEGRATED_WEBSRV
R716_HOMEBREW_CHANNEL_URL=/index.html
R716_HOMEBREW_CHANNEL_TRANSPORT=SAME_ORIGIN_WEBSRV_8080
R717_BACKPORK_BASELINE=0.1_USER_SUPPLIED_PREBUILT_FROZEN
R717_BACKPORK_SHA256=$BACKPORK_SHA
R717_BACKPORK_MODE=TOOLBOX_SERVICES_PID_STATE_SWITCH
R717_GARLIC_SAVEMGR_BASELINE=USER_SUPPLIED_PREBUILT_FROZEN
R717_GARLIC_SAVEMGR_SHA256=$GARLIC_SHA
R717_GARLIC_SAVEMGR_PORT=8082
R717_GARLIC_SAVEMGR_MODE=TOOLBOX_SERVICES_TCP_STATE_SWITCH
R718_SHADOWMOUNT_SKIP=DUMP_INSTALLER_OPTION_CONTINUE_PIPELINE
R718_DUMP_INSTALLER_REFERENCE=EchoStretch/dump_installer
R7181_I18N_POLICY=ALL_NEW_USER_VISIBLE_TEXT_31_LOCALES_SAME_CHANGESET
R7181_I18N_LOCALES=31
R719_FW_SPOOF_BASELINE=26616621599_USER_SUPPLIED_PREBUILT_FROZEN
R719_FW_SPOOF_SHA256=$FW_SPOOF_SHA
R719_FW_SPOOF_MODE=TOOLBOX_SERVICES_ONE_SHOT_PROCESS_STATE_REBOOT_CLEARS_EFFECT
R719_AIRPSX_BASELINE=0.19_USER_SUPPLIED_PREBUILT_FROZEN
R719_AIRPSX_SHA256=$AIRPSX_SHA
R719_AIRPSX_PORT=1214
R719_AIRPSX_MODE=TOOLBOX_SERVICES_TCP_STATE_SWITCH
R719_PS5UPLOAD_BASELINE=5.4.8_USER_SUPPLIED_PREBUILT_FROZEN
R719_PS5UPLOAD_SHA256=$PS5UPLOAD_SHA
R719_PS5UPLOAD_TRANSFER_PORT=9113
R719_PS5UPLOAD_MANAGEMENT_PORT=9114
R719_PS5UPLOAD_MODE=TOOLBOX_SERVICES_TCP_STATE_SWITCH
R719_NP_FAKE_SIGNIN_BASELINE=1.3_USER_SUPPLIED_PREBUILT_FROZEN
R719_NP_FAKE_SIGNIN_SHA256=$NP_FAKE_SIGNIN_SHA
R719_NP_FAKE_SIGNIN_MODE=TOOLBOX_SERVICES_ONE_SHOT_PROCESS_STATE_SIGN_OUT_REVERSES_EFFECT
R719_WKALI_BASELINE=0.4.0-pre-00e1028_USER_SUPPLIED_PREBUILT_FROZEN
R719_WKALI_SHA256=$WKALI_SHA
R719_WKALI_PORT=18181
R719_WKALI_MODE=TOOLBOX_SERVICES_TEMPORARY_TASK_PID_STATE
R719_APP_DUMPER_BASELINE=1.11_USER_SUPPLIED_PREBUILT_FROZEN
R719_APP_DUMPER_SHA256=$APP_DUMPER_SHA
R719_APP_DUMPER_MODE=TOOLBOX_SERVICES_TEMPORARY_USB_DUMP_TASK_PID_STATE
R719_I18N_POLICY=ALL_SIX_SERVICES_31_LOCALES_SAME_CHANGESET
R719_I18N_LOCALES=31
R720_GAME_COMPRESSOR_BASELINE=1.0.4_USER_SUPPLIED_PREBUILT_FROZEN
R720_GAME_COMPRESSOR_UPSTREAM_SHA256=$GC_UPSTREAM_SHA
R720_GAME_COMPRESSOR_PIZZA_INTEGRATED_SHA256=$GC_SHA
R720_GAME_COMPRESSOR_PORT=5910
R720_GAME_COMPRESSOR_MODE=TOOLBOX_TOPLEVEL_ON_DEMAND_TCP_STATE_WEBUI_NO_PKG_NO_TILE
R720_GAME_COMPRESSOR_TILE=DISABLED_GC_LAUNCHER_START
R720_I18N_POLICY=GAME_COMPRESSOR_PIZZA_HEN_TEXT_31_LOCALES_SAME_CHANGESET
R720_I18N_LOCALES=31
R7201_AUTO_LAUNCHER_BEHAVIOR=SUPERSEDED_BY_R7202_NO_TILE
R7202_FULL_TOOLBOX_INTEGRATION=HOME_BREW_CHANNEL_APR_EMU_GAME_COMPRESSOR
R7202_PKG_POLICY=NO_PKG_NO_HOME_TILE
R7202_DERIVATION=HASH_GATED_BYTE_PATCH_FROM_FROZEN_UPSTREAMS
R7202_I18N_LOCALES=31
R721_REMOTE_PLAY_BASELINE=0.1.1_USER_SUPPLIED_PREBUILT_FROZEN
R721_REMOTE_PLAY_SHA256=$REMOTE_PLAY_SHA
R721_REMOTE_PLAY_DEPLOY=/data/PIZZA_HEN/payloads/rp-get-pin.elf
R721_REMOTE_PLAY_MODE=SUPERSEDED_BY_R7252_MANAGED_SERVICE_SWITCH
R721_REMOTE_PLAY_PAIRING_TIMEOUT=120_SECONDS_UPSTREAM
R721_REMOTE_PLAY_RELAUNCH=R7252_SWITCH_ON_PLUGIN_LAUNCH_SWITCH_OFF_PLUGIN_STOP
R721_REMOTE_PLAY_PKG_POLICY=NO_PKG_NO_HOME_TILE
R721_I18N_POLICY=REMOTE_PLAY_PIZZA_HEN_TEXT_31_LOCALES_SAME_CHANGESET
R721_I18N_LOCALES=31
R722_WEB_FILE_MANAGER_BASELINE=1.5_USER_SUPPLIED_FROZEN
R722_WEB_FILE_MANAGER_UPSTREAM_SHA256=$WFM_UPSTREAM_SHA
R722_WEB_FILE_MANAGER_PIZZA_NO_TILE_SHA256=$WFM_SHA
R722_WEB_FILE_MANAGER_PORT=8888_PLUS_FALLBACK_RANGE
R722_LINUX_LOADER_BASELINE=2.4_USER_SUPPLIED_FROZEN
R722_LINUX_LOADER_SHA256=$LINUX_LOADER_SHA
R722_LINUX_LOADER_FW_POLICY=UPSTREAM_3.00_TO_7.61_EXACT_ALLOWLIST
R722_LINUX_LOADER_KSTUFF_POLICY=BOTH_PAUSED_BEFORE_LAUNCH_ABORT_ON_PAUSE_FAILURE
R722_PEGASUS_DL_BASELINE=1.7.0_USER_SUPPLIED_FROZEN
R722_PEGASUS_DL_UPSTREAM_SHA256=$PEGASUS_UPSTREAM_SHA
R722_PEGASUS_DL_PIZZA_NO_TILE_SHA256=$PEGASUS_SHA
R722_PEGASUS_DL_PORT=6970
R722_SPECTRUM_LIBRARY_BASELINE=1.4.2_USER_SUPPLIED_FROZEN
R722_SPECTRUM_LIBRARY_UPSTREAM_SHA256=$SPECTRUM_UPSTREAM_SHA
R722_SPECTRUM_LIBRARY_PIZZA_NO_TILE_SHA256=$SPECTRUM_SHA
R722_SPECTRUM_LIBRARY_PORT=7575
R722_PKG_POLICY=FULL_TOOLBOX_NO_EXTERNAL_LAUNCHER_PKG_NO_HOME_TILE
R722_I18N_POLICY=ALL_PIZZA_HEN_TEXT_31_LOCALES_SAME_CHANGESET
R722_I18N_LOCALES=31
R7221_REMOTE_PLAY_MODE=SUPERSEDED_BY_R7252_MANAGED_SERVICE_SWITCH
R7221_REMOTE_PLAY_STOP=R7252_NORMAL_PLUGIN_MANAGER_SWITCH
R7221_REMOTE_PLAY_AUTOSTART=NOT_TOUCHED_BY_R7252_REMOTE_PLAY_SWITCH
R7221_APR_LABEL=Apr_Emu_Update
R7221_SETTINGS_LABEL=Tools_LOCALIZED_31
R7221_I18N_LOCALES=31
R723_PAYLOAD_REPOSITORY=BUILTIN_PIZZA_HEN
R723_PAYLOAD_REPOSITORY_SOURCE=USER_SUPPLIED_AIO_STORE_PAYLOADS_JSON
R723_PAYLOAD_REPOSITORY_SOURCE_COUNT=83
R723_PAYLOAD_REPOSITORY_ELF_COUNT=79
R723_PAYLOAD_REPOSITORY_SKIPPED_NON_ELF=4
R723_PAYLOAD_REPOSITORY_RUNTIME_SOURCE=builtin://PIZZA_HEN/payloads.json
R723_PAYLOAD_REPOSITORY_OLD_REMOTE_MIRROR=REMOVED
R723_PAYLOAD_REPOSITORY_CHECKSUM_POLICY=SHA256_REQUIRED
R723_PAYLOAD_REPOSITORY_FILENAME_POLICY=ELF_ONLY_SAFE_BASENAME

R7232_REMOTE_PLAY_MODE=SUPERSEDED_BY_R7252_MANAGED_SERVICE_SWITCH
R7232_REMOTE_PLAY_ELF=BYTE_EXACT_USER_SUPPLIED_V0.1.1
R7232_REMOTE_PLAY_SHA256=$REMOTE_PLAY_SHA
R7232_REMOTE_PLAY_DEPLOY=/data/PIZZA_HEN/payloads/rp-get-pin.elf
R7232_REMOTE_PLAY_PROCESS_MANAGER=RESTORED_BY_R7252_REMOTE_PLAY_SWITCH
R7232_REMOTE_PLAY_PKG_POLICY=NO_PKG_NO_HOME_TILE
R725_SVT_PLAY_BASELINE=0.2_USER_SUPPLIED_FROZEN
R725_SVT_PLAY_SHA256=$SVT_PLAY_SHA
R725_SVT_PLAY_MODE=TOOLBOX_TOPLEVEL_DIRECT_WEBAPP_URI_NO_ELF_INJECTION
R725_SVT_PLAY_WEBAPP=https://ps5-payload-dev.github.io/svtplay
R725_SVT_PLAY_INSTALLER_BREW10002=NOT_LAUNCHED_NO_PKG_NO_TILE
R7251_PROSPERO_PLAYER_BASELINE=1.0_USER_SUPPLIED_FROZEN
R7251_PROSPERO_PLAYER_SHA256=$PROSPERO_SHA
R7251_PROSPERO_PLAYER_SERVICE_PATH=/data/PIZZA_HEN/payloads/ProsperoPlayer_v1.0.elf
R7251_PS_PLAY_BASELINE=2.1_USER_SUPPLIED_FROZEN
R7251_PS_PLAY_SHA256=$PSPLAY_SHA
R7251_PS_PLAY_SERVICE_PATH=/data/PIZZA_HEN/payloads/PS-Play_v2.1.elf
R7251_BFPLAYER_BASELINE=0.1.0-alpha.44_USER_SUPPLIED_FROZEN
R7251_BFPLAYER_SHA256=$BFPLAYER_SHA
R7251_BFPLAYER_SERVICE_PATH=/data/PIZZA_HEN/payloads/BFplayer-standalone_v0.1.0-alpha.44.elf
R7251_MEDIA_PLAYER_CONTROL=SERVICES_START_STOP_ONLY
R7251_MEDIA_PLAYER_INSTALL_DELETE=REMOVED
R7251_MEDIA_PLAYER_AUTOSTART=NOT_CREATED
R7251_MEDIA_PLAYER_ELFS=BYTE_EXACT_USER_SUPPLIED
R7251_MEDIA_PLAYER_UI=STANDARD_SERVICE_SWITCHES_NO_GROUP_LABEL
R7252_REMOTE_PLAY_MODE=MANAGED_SERVICE_SWITCH
R7252_REMOTE_PLAY_ELF=BYTE_EXACT_USER_SUPPLIED_V0.1.1
R7252_REMOTE_PLAY_SHA256=$REMOTE_PLAY_SHA
R7252_REMOTE_PLAY_DEPLOY=/data/PIZZA_HEN/payloads/rp-get-pin.elf
R7252_REMOTE_PLAY_AUTOSTART=OFF_UNCHANGED
R7252_REMOTE_PLAY_PKG_POLICY=NO_PKG_NO_HOME_TILE
R72522_DNS_TOOLS=CHUKEI_DNS_0.9.0_AND_NANODNS_0.4
R72522_DNS_ELFS=BYTE_EXACT_USER_SUPPLIED
R72522_CHUKEI_DNS_SHA256=$CHUKEI_DNS_SHA
R72522_NANODNS_SHA256=$NANODNS_SHA
R72522_DNS_CONTROL=SUPERSEDED_BY_R725212_STANDARD_SERVICES_SWITCHES
R72522_DNS_AUTOSTART=NOT_CREATED
R72522_DNS_I18N=31_LOCALES
R72525_THEMES_AVATAR=PS5_CUSTOM_TOOL_MANAGER_AND_PS5_WALLPAPER_MODDER
R72525_CUSTOM_TOOL_ORIGINAL_SHA256=$CUSTOM_TOOL_ORIG_SHA
R72525_CUSTOM_TOOL_WEB_ONLY_SHA256=$CUSTOM_TOOL_DERIVED_SHA
R72525_WALLPAPER_ORIGINAL_SHA256=$WALLPAPER_MODDER_ORIG_SHA
R72525_WALLPAPER_WEB_ONLY_SHA256=$WALLPAPER_MODDER_DERIVED_SHA
R72525_INSTALLER_POLICY=NO_HOME_TILE_NO_LAUNCHER_ICON_NO_PKG
R72525_WEB_LAUNCH=ON_DEMAND_CHEATRUNNER_STYLE_IFRAME
R72525_WEB_PORTS=8089,8095
R72525_AUTOSTART=NONE
R72525_I18N=31_LOCALES
R72526_DNS_ELFS=ORIGINAL_USER_SUPPLIED_BYTE_EXACT
R72526_DNS_SUCCESS_NOTIFY=UPSTREAM_OWNED_NO_GENERIC_OVERLAY
R72526_RETIRED_AUTOSTART=STALE_MARKERS_CLEARED_BEFORE_SCAN
R72527_SERVICES_ORIGINAL_ELFS=UNRAR_PS5,PS_GAME_STATE_LIB,GHOSTPAD,GHOSTCONTROL,PS_DISCORD_PRESENCE,PS5_LINUX_LOADER
R72527_SERVICE_UI=STANDARD_SERVICES_SWITCHES
R72527_ELF_POLICY=BYTE_EXACT_USER_SUPPLIED_NO_BINARY_PATCHING
R72527_AUTOSTART=NONE_MANUAL_ONLY
R72527_I18N=31_LOCALES
R72528_PSPLAY_AUTOSTART=HARD_FILENAME_BLOCK_ALL_SCANNED_ROOTS
R72528_REMOTE_PLAY_SERVICE=RETIRED_PURGED
R72528_GARLIC_WORKER_SERVICE=RETIRED_PURGED
R72528_ACTIVE_IMPORTED_SERVICES=UNRAR_PS5,PS_GAME_STATE_LIB,GHOSTPAD,GHOSTCONTROL,PS_DISCORD_PRESENCE,PS5_LINUX_LOADER
R72527_UNRAR_SHA256=$UNRAR_SHA
R72527_PS_GAME_STATE_SHA256=$PS_GAME_STATE_SHA
R72527_GHOSTPAD_SHA256=$GHOSTPAD_SHA
R72527_GHOSTCONTROL_SHA256=$GHOSTCONTROL_SHA
R72527_PS_DISCORD_SHA256=$PS_DISCORD_SHA
R72527_LINUX_LOADER_SHA256=$LINUX_LOADER_SHA
R72529_STORAGE_DASHBOARD=INTERNAL_NVME_USB_READ_ONLY
R72529_STORAGE_INTERNAL=/user
R72529_STORAGE_EXT=/mnt/ext0,/mnt/ext1
R72529_STORAGE_USB=/mnt/usb0../mnt/usb7
R72529_STORAGE_SOURCE=KERNEL_GETFSSTAT_MNT_NOWAIT
R72529_PACKAGE_INSTALLER=UNCHANGED
R72529_I18N=31_LOCALES
R725210_PACKAGE_INSTALLER=R72528_BYTE_EXACT_RESTORED
R725210_STORAGE_ENTRY=SEPARATE_TOP_LEVEL_SCREEN
R725210_STORAGE_WEBKIT=NO_NULLISH_COALESCING
R725210_PSPLAY_NOTIFICATION=STALE_DATA_HOMEBREW_SOURCE_CLEANED_BEFORE_SHADOWMOUNT
R725210_SHADOWMOUNT=PRISTINE_UNCHANGED
RUNTIME_SEQUENCE=BOOTSTRAP_WEBSRV_NO_TILE_KSTUFF_SELECTOR_3WAY_SHADOWMOUNT_SELECTOR_STABLE_EXPERIMENTAL_OR_SKIP_AUTO_CLOSE_OPTIONAL_SHADOWMOUNT_FTPSRV_PS5DEBUG_NG_DAEMONS_TOOLBOX_SERVICES_ELFLDR_BACKPORK_GARLIC_AIRPSX_PS5UPLOAD_FW_SPOOF_NP_FAKE_SIGNIN_WKALI_APP_DUMPER_ALL_ON_DEMAND_HOME_BREW_CHANNEL_APR_EMU_UPDATE_GAME_COMPRESSOR_5910_REMOTE_PLAY_MANAGED_SERVICE_SWITCH_WEB_FILE_MANAGER_NO_TILE_LINUX_LOADER_GUARDED_GAME_DOWNLOAD_PEGASUS_6970_NO_TILE_SPECTRUM_7575_NO_TILE_CHEATRUNNER_ON_DEMAND_POORDS4_RC38_TOOLS_START_STATUS_COOPERATIVE_STOP_SVT_PLAY_DIRECT_WEBAPP_PROSPERO_PSPLAY_BFPLAYER_SERVICES_START_STOP_ONLY_DNS_CHUKEI_NANODNS_STANDARD_SERVICES_SWITCHES
PAYLOAD=$FINAL_BIN
PAYLOAD_SIZE=$PAYLOAD_SIZE
PAYLOAD_SHA256=$PAYLOAD_SHA
BUILD_JOBS=$JOBS
CMAKE_GENERATOR=$CMAKE_GENERATOR
LOG_FILE=$LOG_FILE
RESULT
cat "$RESULT_FILE"

# R7.25.2.3 metadata
echo "R72523_TOOLBOX_REMOVED=REMOTE_PLAY,LINUX_LOADER,SVT_PLAY"
echo "R72523_REMOVAL_MODE=PHYSICAL_UI_REMOVAL_AND_TOOLBOX_CATALOG_FILTER"
# R7.25.2.4 DNS lifecycle repair metadata
echo "R72524_DNS_CONTROL=SUPERSEDED_BY_R725212_STANDARD_SERVICES_SWITCHES"
echo "R72524_DNS_ELFS=BYTE_EXACT_USER_SUPPLIED_UNMODIFIED"
echo "R72524_DNS_MUTUAL_EXCLUSION=SUPERSEDED_NO_CROSS_PAYLOAD_CONTROL"
echo "R72524_DNS_STOP=SUPERSEDED_STANDARD_PAYLOAD_STOP"
echo "R72524_DNS_AUTOSTART=NOT_CREATED"
# R7.25.2.5 Themes Avatar metadata
echo "R72525_THEMES_AVATAR=PS5_CUSTOM_TOOL_MANAGER_AND_PS5_WALLPAPER_MODDER"
echo "R72525_CUSTOM_TOOL_ORIGINAL_SHA256=$CUSTOM_TOOL_ORIG_SHA"
echo "R72525_CUSTOM_TOOL_WEB_ONLY_SHA256=$CUSTOM_TOOL_DERIVED_SHA"
echo "R72525_WALLPAPER_ORIGINAL_SHA256=$WALLPAPER_MODDER_ORIG_SHA"
echo "R72525_WALLPAPER_WEB_ONLY_SHA256=$WALLPAPER_MODDER_DERIVED_SHA"
echo "R72525_INSTALLER_POLICY=NO_HOME_TILE_NO_LAUNCHER_ICON_NO_PKG"
echo "R72525_WEB_LAUNCH=ON_DEMAND_CHEATRUNNER_STYLE_IFRAME"
echo "R72525_WEB_PORTS=8089,8095"
echo "R72525_AUTOSTART=NONE"
echo "R72525_I18N=31_LOCALES"
echo "R72526_DNS_ELFS=ORIGINAL_USER_SUPPLIED_BYTE_EXACT"
echo "R72526_DNS_SUCCESS_NOTIFY=SUPERSEDED_GENERIC_PIZZA_LAUNCH_NOTIFY_RESTORED"
echo "R72526_RETIRED_AUTOSTART=STALE_MARKERS_CLEARED_BEFORE_SCAN"

# R7.25.2.11 DNS plain separate payloads metadata
echo "R725211_DNS_MODE=SUPERSEDED_BY_R725212_SERVICES"
echo "R725211_DNS_ELFS=ORIGINAL_USER_SUPPLIED_BYTE_EXACT"
echo "R725211_DNS_CROSS_CONTROL=NONE"
echo "R725211_DNS_STOP=STANDARD_PAYLOAD_STOP"
echo "R725211_DNS_NOTIFY=GENERIC_PIZZA_LAUNCH_STOP_PLUS_PAYLOAD_OWN_NOTIFICATIONS"
echo "R725211_DNS_AUTOSTART=NOT_CREATED"


# R7.25.2.12 DNS moved to standard Services metadata
echo "R725212_DNS_UI=DEDICATED_CHANGE_DNS_SCREEN_REMOVED"
echo "R725212_DNS_SERVICES=CHUKEI_DNS_0.9.0,NANODNS_0.4"
echo "R725212_DNS_CONTROL=STANDARD_SERVICES_TOGGLE_MANAGED_TASK"
echo "R725212_DNS_ELFS=RECOPIED_FROM_CURRENT_USER_UPLOADS_BYTE_EXACT"
echo "R725212_DNS_SPECIAL_UI_LIFECYCLE=NONE"
echo "R725212_DNS_AUTOSTART=NONE"

# R7.25.2.13 Debug Services hardware bridge restore metadata
echo "R725213_DEBUG_SERVICES_LAUNCHER=R3_V01_HARDWARE_FROZEN_RESTORED"
echo "R725213_DEBUG_SERVICES_LAUNCHER_SHA256=7f7134593eefa9628bc581eebe3a7fc66f40cba3bb8f9447ebd641bfe58eb399"
echo "R725213_DEBUG_SERVICES_HELPER=V01_FROZEN_UNCHANGED"
echo "R725213_DEBUG_SERVICES_TILE=PZHN00002_31_LOCALIZED_TITLES_PRESERVED"

# R7.25.2.14 Fan Target dual option metadata
echo "R725214_FAN_TARGET_OPTION1=FAN_TARGET_0.1_EXISTING_FIVE_ELFS_UNCHANGED"
echo "R725214_FAN_TARGET_OPTION2=PS5_FAN_CONTROL_V0.3_ORIGINAL_ELF"
echo "R725214_FAN_CONTROL_SHA256=$FAN03_SHA"
echo "R725214_FAN_CONTROL_INI_SHA256=$FAN03_INI_SHA"
echo "R725214_FAN_CONTROL_RUNTIME=/data/PIZZA_HEN/payloads/ps5-fan-control-v0.3.elf"
echo "R725214_FAN_CONTROL_CONFIG=UPSTREAM_USB0_TO_USB7_THEN_DATA_THEN_DEFAULT_70C"
echo "R725214_FAN_OPTIONS=MUTUALLY_EXCLUSIVE_AT_TOOLBOX_CONTROL_LAYER"
echo "R725215_FAN_CONTROL_V03_TARGET_UI=TARGET_TEMPERATURE_30_90_C"
echo "R725215_FAN_CONTROL_V03_CONFIG=/data/fan_control.ini"
echo "R725215_FAN_CONTROL_V03_ELF=UNCHANGED"
echo "R725215_FAN_CONTROL_V03_USB_PRECEDENCE=ORIGINAL"

# R7.25.2.16 PoorDS4 Tools integration metadata
echo "R725216_POORDS4_VERSION=0.1.0-rc38"
echo "R725216_POORDS4_UI=TOOLS_DEDICATED_ENTRY"
echo "R725216_POORDS4_MAIN_SHA256=$POORDS4_MAIN_SHA"
echo "R725216_POORDS4_STATUS_SHA256=$POORDS4_STATUS_SHA"
echo "R725216_POORDS4_STOP_SHA256=$POORDS4_STOP_SHA"
echo "R725216_POORDS4_RUNTIME=/data/PIZZA_HEN/payloads/PoorDS4rc38.elf"
echo "R725216_POORDS4_STATUS=ORIGINAL_READ_ONLY_STATUS_ELF"
echo "R725216_POORDS4_STOP=ORIGINAL_COOPERATIVE_STOP_ELF"
echo "R725216_POORDS4_AUTOSTART=NONE"
echo "R725216_POORDS4_BINARY_POLICY=BYTE_EXACT_USER_SUPPLIED_NO_PATCHING"
echo "R725216_POORDS4_FW_POLICY=UPSTREAM_EXACT_OR_STRUCTURAL_FAIL_CLOSED"
echo "R7252161_STATIC_GATE_REPAIR=R716_HANDLER_BOUNDARY_ONLY_NO_RUNTIME_CHANGE"

