from pathlib import Path
root=Path(__file__).resolve().parents[1]
sm=root/'ThirdParty/ShadowMountPlus-1.6beta16-PIZZA-HEN'
paths=(sm/'include/sm_paths.h').read_text()
cfg=(sm/'src/sm_config_mount.c').read_text()
checks={
 'PIZZAHEN_INTERNAL': '/data/PIZZA_HEN/games' in paths,
 'PIZZAHEN_USERDATA': '/user/data/PIZZA_HEN/games' in paths,
 'PIZZAHEN_USB0': '/mnt/usb0/PIZZA_HEN/games' in paths,
 'PIZZAHEN_USB7': '/mnt/usb7/PIZZA_HEN/games' in paths,
 'PIZZAHEN_EXT0': '/mnt/ext0/PIZZA_HEN/games' in paths,
 'PIZZAHEN_EXT1': '/mnt/ext1/PIZZA_HEN/games' in paths,
 'PIZZAHEN_EXT2': '/mnt/ext2/PIZZA_HEN/games' in paths,
 'LEGACY_ETAHEN': '/data/etaHEN/games' in paths,
 'MANAGED_PIZZAHEN': 'pizzahen_roots' in cfg and '/data/PIZZA_HEN/games' in cfg,
 'MANAGED_AFTER_CUSTOM': 'add_runtime_managed_scan_paths(state);' in cfg,
}
for k,v in checks.items(): print(f'{k}={"PASS" if v else "FAIL"}')
if not all(checks.values()): raise SystemExit(1)
print(f'FIX17_SCANROOT_TESTS={sum(checks.values())}/{len(checks)} PASS')
