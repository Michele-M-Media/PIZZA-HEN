#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "Source Code"
main = (SRC / "bootstrapper/source/main.cpp").read_text(errors="ignore")
cmake = (SRC / "bootstrapper/CMakeLists.txt").read_text(errors="ignore")
param = json.loads((SRC / "bootstrapper/assets/toolbox_shortcut_param.json").read_text())
icon = (SRC / "bootstrapper/assets/pizzahen_toolbox_icon.png").read_bytes()
unpacker = (SRC / "unpacker/CMakeLists.txt").read_text(errors="ignore")

checks = []
def ok(name, cond):
    checks.append((name, bool(cond)))
    print(f"{name}={'PASS' if cond else 'FAIL'}")

ok("FIX34_FINAL_TARGET", "PIZZA-HEN-v0.1-FIX45-PLUGIN-MANAGER-LIFECYCLE.elf" in unpacker)
ok("WELCOME_NOTIFICATION_PRESERVED", "PIZZA HEN is starting..." in main and "Choose a KStuff engine when the selector opens" in main)
ok("SELECTOR_LITE_PRESERVED", 'chosen_name = "kstuff-lite-1.09"' in main)
ok("SELECTOR_DR_PRESERVED", 'chosen_name = "kstuff-dr-1.2"' in main)
ok("SELECTOR_BROWSER_PRESERVED", "start_browser_kstuff_selector()" in main)
ok("ONE_ENGINE_REQUEST_PRESERVED", '"lite"' in main and '"dr"' in main and "kstuff_request.txt" in main)

welcome = main.find("welcome notification returned")
install = main.find("int early_media_tile_rc = install_pizzahen_toolbox_shortcut()")
selector = main.find("int selector_rc = start_browser_kstuff_selector()")
debug_ready = main.find("ps5debug-NG v1.3.0 ready on port 744")
ok("MEDIA_TILE_EARLY_ORDER", -1 not in (welcome, install, selector) and welcome < install < selector)
ok("MEDIA_TILE_BEFORE_DEBUG_GATE", -1 not in (install, debug_ready) and install < debug_ready)

ok("USER_SERVICE_INIT", "sceUserServiceInitialize(&user_prio)" in main)
ok("NETCTL_INIT", "sceNetCtlInit()" in main)
ok("NETCTL_LINK", "SceNetCtl" in cmake)
ok("APPINST_INIT", "sceAppInstUtilInitialize()" in main)
ok("APPINSTALL_TITLE_DIR", 'sceAppInstUtilAppInstallTitleDir(title_id, "/user/app/", nullptr)' in main)
ok("APPINSTALL_NID", '"Wudg3Xe3heE"' in main)
ok("REGISTRATION_SUCCESS_MARKER", ".pizzahen_media_registered" in main and "PIZZA_HEN_MEDIA_TILE_V1" in main)
ok("FAILED_REGISTRATION_RETRYABLE", 'unlink(registered_marker);' in main and "registration_failed" in main)
ok("STATUS_FILE", "/data/PIZZA_HEN/runtime/media_tile_status.txt" in main)
ok("FAILURE_NOTIFICATION_VISIBLE", "PIZZA HEN Toolbox icon install failed" in main)
ok("MEDIA_CATEGORY_65536", param.get("applicationCategoryType") == 65536)
ok("MEDIA_TITLE_ID", param.get("titleId") == "PZHN00001")
ok("DEEPLINK_WEBSRV_8080", str(param.get("deeplinkUri","")).startswith("http://127.0.0.1:8080/"))
ok("ICON_PNG_CONTAINER", len(icon) > 8 and icon[:8] == b"\x89PNG\r\n\x1a\n")

failed = [n for n,v in checks if not v]
if failed:
    raise SystemExit("FIX34_STATIC_FAIL=" + ",".join(failed))
print(f"FIX34_STATIC={len(checks)}/{len(checks)} PASS")
