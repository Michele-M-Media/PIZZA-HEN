#!/usr/bin/env python3
"""Build PIZZA HEN web-only integration variants for Themes Avatar.

The user-supplied original ELFs are never overwritten. The only intentional
changes are to their launcher/installer Web integration behavior:

* PS5 Custom Tool Manager: disable both calls into the XMB launcher installer,
  neutralize its public install route, remove the obsolete tile control from
  the embedded WebUI, and correct the startup notification.
* PS5 Wallpaper Modder: disable its home-screen AppInstUtil installer and its
  automatic browser launch, while retaining the expected hidden toggle DOM id
  so the upstream JavaScript remains valid.

All customization/wallpaper APIs and payload behavior outside those integration
points remain byte-for-byte derived from the supplied binaries.
"""
from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parents[1]
CUSTOM_ORIG = ROOT / 'ThirdParty/PS5-Custom-Tool-Manager-vCustom-USER-SUPPLIED-ORIGINAL/PS5-Custom-Tool-Manager-_vCustom.elf'
CUSTOM_DER = ROOT / 'ThirdParty/THEMES-AVATAR-INTEGRATED-DERIVED/PS5-Custom-Tool-Manager-_vCustom-pizza-web-only.elf'
WALL_ORIG = ROOT / 'ThirdParty/ps5-wallpaper-modd-v1.0-USER-SUPPLIED-ORIGINAL/ps5-wallpaper-modd_v1.0.elf'
WALL_DER = ROOT / 'ThirdParty/THEMES-AVATAR-INTEGRATED-DERIVED/ps5-wallpaper-modd_v1.0-pizza-web-only.elf'

CUSTOM_ORIG_SHA = '297824ceaf6ea53fde57550adf9b5c2fc44c63ef60e8196ab92d351d1615d9cb'
CUSTOM_DER_SHA = 'ecdf8a8eaa47f59bfe5b419dcb3f60bd3dc68deef9f36a5e36c125f3e71987b7'
WALL_ORIG_SHA = 'b18a866bac9deff45b921b7d3ea6143d541117b56c666d817ecdc81961829139'
WALL_DER_SHA = 'a2fa5e9c8ecb794fed189bcd204008ea446a12c2d1381fa601734b3d915d5360'


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def fixed_patch(buf: bytearray, off: int, old: bytes, new: bytes, label: str) -> None:
    if len(old) != len(new):
        raise RuntimeError(f'{label}: size-changing patch rejected')
    got = bytes(buf[off:off+len(old)])
    if got != old:
        raise RuntimeError(f'{label}: source bytes mismatch at 0x{off:x}: {got.hex()} != {old.hex()}')
    buf[off:off+len(old)] = new


def build_custom() -> bytes:
    src = CUSTOM_ORIG.read_bytes()
    if sha(src) != CUSTOM_ORIG_SHA:
        raise RuntimeError('Custom Tool Manager original SHA mismatch')
    b = bytearray(src)
    fixed_patch(b, 0xacfb, bytes.fromhex('e8a4260000'), bytes.fromhex('31c0909090'), 'startup XMB installer call')
    fixed_patch(b, 0x16a91, bytes.fromhex('e80e69ffff'), bytes.fromhex('31c0909090'), 'HTTP XMB installer call')

    old = b'/api/install-xmb'; new = b'/api/blocked-xmb'
    pos = bytes(b).find(old)
    if pos < 0 or len(old) != len(new):
        raise RuntimeError('Custom Tool Manager install route not found')
    b[pos:pos+len(old)] = new

    old = b"<button onclick='uninstallLauncher()'>Retirer tuile</button>"
    pos = bytes(b).find(old)
    if pos < 0:
        raise RuntimeError('Custom Tool Manager launcher button not found')
    new = b'<!-- PIZZA HEN: launcher control removed from WebUI -->'
    new += b' ' * (len(old) - len(new))
    b[pos:pos+len(old)] = new

    old = b'PS5 Custom Tool Manager V1: serveur web et raccourci installes'
    pos = bytes(b).find(old)
    if pos < 0:
        raise RuntimeError('Custom Tool Manager startup notification not found')
    new = b'PS5 Custom Tool Manager V1: web PIZZA HEN (no XMB launcher)'
    new += b' ' * (len(old) - len(new))
    b[pos:pos+len(old)] = new
    out = bytes(b)
    if sha(out) != CUSTOM_DER_SHA:
        raise RuntimeError('Custom Tool Manager derived SHA mismatch')
    return out


def build_wallpaper() -> bytes:
    src = WALL_ORIG.read_bytes()
    if sha(src) != WALL_ORIG_SHA:
        raise RuntimeError('Wallpaper Modder original SHA mismatch')
    b = bytearray(src)
    fixed_patch(b, 0xd8e1, bytes.fromhex('e86af9ffff'), bytes.fromhex('31c0909090'), 'home-screen installer call')
    fixed_patch(b, 0xda11, bytes.fromhex('e81afbffff'), bytes.fromhex('31c0909090'), 'automatic browser decision')

    pos = bytes(b).find(b'autoBrowserToggle')
    if pos < 0:
        raise RuntimeError('Wallpaper auto-browser control not found')
    start = bytes(b).rfind(b'<div class="settings-row">', 0, pos)
    end = bytes(b).find(b'<div id="dashboardScreen"', pos)
    if start < 0 or end <= start:
        raise RuntimeError('Wallpaper auto-browser WebUI block bounds not found')
    old = bytes(b[start:end])
    new = (b'<input type="checkbox" id="autoBrowserToggle" style="display:none">'
           b'<!-- PIZZA HEN web-only: automatic browser launch disabled -->')
    if len(new) > len(old):
        raise RuntimeError('Wallpaper WebUI replacement does not fit')
    new += b' ' * (len(old) - len(new))
    b[start:end] = new
    out = bytes(b)
    if sha(out) != WALL_DER_SHA:
        raise RuntimeError('Wallpaper Modder derived SHA mismatch')
    return out


def main() -> int:
    CUSTOM_DER.parent.mkdir(parents=True, exist_ok=True)
    custom = build_custom(); wall = build_wallpaper()
    CUSTOM_DER.write_bytes(custom); WALL_DER.write_bytes(wall)
    print(f'THEMES_AVATAR_CUSTOM_DERIVED_SHA256={sha(custom)}')
    print(f'THEMES_AVATAR_WALLPAPER_DERIVED_SHA256={sha(wall)}')
    print('THEMES_AVATAR_WEB_ONLY_VARIANTS=PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
