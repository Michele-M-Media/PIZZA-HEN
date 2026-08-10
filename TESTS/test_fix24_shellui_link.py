from pathlib import Path

root = Path(__file__).resolve().parents[1] / "Source Code"
embed = (root / "bootstrapper/source/daemon.c").read_text(encoding="utf-8")
boot = (root / "bootstrapper/source/main.cpp").read_text(encoding="utf-8")
cm = (root / "bootstrapper/CMakeLists.txt").read_text(encoding="utf-8")
unpacker = (root / "unpacker/CMakeLists.txt").read_text(encoding="utf-8")
checks=[]
def ok(name, cond):
    checks.append((name,bool(cond)))
    print(f"{name}={'PASS' if cond else 'FAIL'}")

ok("SHELLUI_PRX_START_PROVIDER", '.global shellui_prx_start' in embed and 'shellui_prx_start:' in embed)
ok("SHELLUI_PRX_SIZE_PROVIDER", '.global shellui_prx_size' in embed and 'shellui_prx_size:' in embed)
ok("SHELLUI_PRX_REAL_ASSET", 'daemon/assets/shellui.elf' in embed and '.incbin' in embed)
ok("SHELLUI_PRX_SIZE_EXPR", '.int    shellui_prx_end - shellui_prx_start' in embed)
ok("BOOTSTRAPPER_CONSUMER_MATCH", 'extern uint8_t shellui_prx_start[];' in boot and 'extern const unsigned int shellui_prx_size;' in boot)
ok("BOOTSTRAPPER_SHELLUI_DEPENDENCY", 'add_dependencies(${PROJECT_NAME} daemon util shellui selector_action toolbox_action)' in cm)
ok("FIX24_FINAL_TARGET", 'PIZZA-HEN-v0.1-FIX45-PLUGIN-MANAGER-LIFECYCLE.elf' in unpacker)
failed=[n for n,v in checks if not v]
if failed:
    raise SystemExit('FIX24_STATIC_FAIL=' + ','.join(failed))
print(f"FIX24_STATIC={len(checks)}/{len(checks)} PASS")
