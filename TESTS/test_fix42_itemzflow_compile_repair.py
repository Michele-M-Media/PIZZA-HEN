from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
hook = (ROOT / "Source Code/shellui/src/HookFunctions.cpp").read_text(errors="ignore")
cm = (ROOT / "Source Code/unpacker/CMakeLists.txt").read_text(errors="ignore")
build = (ROOT / "build_pizzahen_multisdk.sh").read_text(errors="ignore")
checks=[]
def ok(name, cond):
    if not cond:
        raise SystemExit(f"{name}=FAIL")
    checks.append(name); print(f"{name}=PASS")
ok("FIX42_UNUSED_RESTORE_HELPER_REMOVED", "restore_pizzahen_itemzflow_theme" not in hook)
ok("FIX42_APPLY_THEME_PRESERVED", "apply_pizzahen_itemzflow_theme" in hook)
ok("FIX42_DIRECT_ITEMZFLOW_PRESERVED", 'launch_pizzahen_backend("ITEM00001", "Game Manager")' in hook)
ok("FIX42_SYSTEMSERVICE_PRESERVED", "sceSystemServiceLaunchApp(title_id, argv, &ctx)" in hook)
ok("FIX42_MULTI_SDK_PRESERVED", all(x in build for x in ["PIZZA_HEN_SDK","PS5_PAYLOAD_SDK","PS5SDK","PAYLOAD_SDK","PIZZA_HEN_TOOLCHAIN_FILE"]))
ok("FIX42_TARGET", "PIZZA-HEN-v0.1-FIX45-PLUGIN-MANAGER-LIFECYCLE.elf" in cm)
print(f"FIX42_STATIC={len(checks)}/{len(checks)} PASS")
