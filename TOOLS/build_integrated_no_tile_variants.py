#!/usr/bin/env python3
from pathlib import Path
import hashlib
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'Source Code' / 'bootstrapper' / 'assets'

ITEMS = {
    'websrv': {
        'src': ROOT / 'ThirdParty/websrv-0.34-UPSTREAM-FROZEN/websrv-ps5.elf',
        'dst': SRC / 'websrv-ps5.elf',
        'sha': '54730c867c6e1148536fdcb370e63a7762d989ea87b62488ad4caff64d43f263',
        'out_sha': '16a18de9df60b4d726409121a2f24ea92616db03e1cc45fab49c8d05ae8b480c',
        'patches': [
            (0x9C67, bytes.fromhex('e874020000'), bytes.fromhex('9090909090'),
             'disable sys_init -> install_launcher()'),
        ],
    },
    'apr': {
        'src': ROOT / 'ThirdParty/apr-emu-updater-1.4-USER-SUPPLIED-FROZEN/apr_emu_updater.elf',
        'dst': SRC / 'apr_emu_updater.elf',
        'sha': '684a7e824e03f2402693641f347341a118fa0ac7a9573f212036a0a5337a8054',
        'out_sha': 'fcd9472ea50141a51e3d6663aee2eadbe99b9e6e0cedf1421b7c1d67f62727a9',
        'patches': [
            (0x45CF, bytes.fromhex('488d3d0b010000'), bytes.fromhex('e9300000009090'),
             'bypass automatic tile-install thread'),
            (0x9D78, bytes.fromhex('0f8421030000'), bytes.fromhex('909090909090'),
             'disable /api/tile/install handler branch'),
            (0x2231D,
             b'<button class="btn" id="installTile">Reinstall tile</button>',
             b'<button id="installTile" hidden></button>' + b' ' * 19,
             'hide tile button in embedded WebUI'),
            (0x25636,
             b"banner.className = launcher.present ? 'msg' : 'msg show';",
             b"banner.className = 'msg';" + b' ' * 32,
             'hide launcher-upload banner in Toolbox-integrated mode'),
        ],
    },
    'web_file_manager': {
        'src': ROOT / 'ThirdParty/ps5-web-file-manager-v1.5-USER-SUPPLIED-FROZEN/ps5-web-file-manager_v1.5.elf',
        'dst': SRC / 'web-file-mgr.elf',
        'sha': '9a7d7e5c685900d7f916cdc08cb6f7ea7e9cf5a4576f2799157b3f251deedf3c',
        'out_sha': 'd0bc7620051079fff40147c4bcf364fda054b7e5bef9193abfba2ef76710006b',
        'patches': [
            (0x14584, bytes.fromhex('554889'), bytes.fromhex('31c0c3'),
             'disable app_install_if_needed() launcher installer'),
        ],
    },
    'pegasus_dl': {
        'src': ROOT / 'ThirdParty/pegasus-dl-v1.7.0-USER-SUPPLIED-FROZEN/pegasus-dl_v1.7.0.elf',
        'dst': SRC / 'pegasus-dl.elf',
        'sha': 'cb2a4b3c248323f2432ce118cb1bf4975146035239ce9b571a9bdb51b3fee226',
        'out_sha': '730cb6be1d16e93f7b06b269e8fa56f45866ab2fc51ac2ef1e90bbf341a1c02a',
        'patches': [
            (0x4129, bytes.fromhex('67e8311d0200'), bytes.fromhex('909090909090'),
             'disable startup launcher_auto_install_init() call'),
            (0x26050, bytes.fromhex('31ffbe010000'), bytes.fromhex('b8ffffffffc3'),
             'disable manual launcher_install_async()'),
        ],
    },
    'spectrum_library': {
        'src': ROOT / 'ThirdParty/Spectrum-Library-v1.4.2-USER-SUPPLIED-FROZEN/Spectrum-Library_v1.4.2.elf',
        'dst': SRC / 'Spectrum-Library.elf',
        'sha': '54755ce62d99be610afe364e26de05eaa9e2d92192cda525790a563c6296261f',
        'out_sha': 'e747a5b01c468e1bbe7d09558751c90237e47a4d6bf932e1d174a4934b1afd4c',
        'patches': [
            (0x11C888, bytes.fromhex('554889'), bytes.fromhex('31c0c3'),
             'disable Spectrum home-tile installer worker'),
        ],
    },
    'game_compressor': {
        'src': ROOT / 'ThirdParty/PS5-Game-Compressor-1.0.4-USER-SUPPLIED-FROZEN/game-compressor.elf',
        'dst': SRC / 'game-compressor.elf',
        'sha': 'e55e90aaade13b6e0d4316c1597ef90a21b67a06475c3e25de054224bc1e941b',
        'out_sha': '535aa4a8e951c04b98df33eb7d476dbcb6cbec080c00dfc8d574f1e61b233ac3',
        'patches': [
            (0x11944, bytes.fromhex('e850580200'), bytes.fromhex('9090909090'),
             'disable on_ready -> gc_launcher_start()'),
        ],
    },
}

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def patch_one(name, item):
    src = item['src']
    dst = item['dst']
    data = bytearray(src.read_bytes())
    got = sha256(data)
    if got != item['sha']:
        raise SystemExit(f'{name}: baseline SHA mismatch: {got}')
    for offset, old, new, label in item['patches']:
        if len(old) != len(new):
            raise SystemExit(f'{name}: patch size mismatch: {label}')
        current = bytes(data[offset:offset+len(old)])
        if current != old:
            raise SystemExit(
                f'{name}: patch preimage mismatch at 0x{offset:x} ({label})\n'
                f' expected={old.hex()}\n actual={current.hex()}')
        data[offset:offset+len(old)] = new
    out = sha256(data)
    if out != item['out_sha']:
        raise SystemExit(f'{name}: derived SHA mismatch: {out}')
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(data)
    print(f'{name}: PASS baseline={got} derived={out} -> {dst}')

for name, item in ITEMS.items():
    patch_one(name, item)
print('PIZZA_NO_TILE_VARIANTS=PASS')
