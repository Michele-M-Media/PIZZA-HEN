# DPIv2 12.20+ etaHEN 2.6B MetaInfo repair

Baseline: `PIZZA-HEN-v1.0-MULTILANGUAGE-CHEATRUNNER-COMPILE-REPAIR.zip`
Baseline SHA-256: `9f9dafef3000c9257f7a8ccc0b7ac0000c07a88fcf1b7beebc7fa0d1b9308783`

## Hardware evidence before this repair

- 11.60: Debug Services PASS; DPIv2 PASS (same tester baseline).
- 12.20: Debug Services PASS; DPIv2 URL install returns `0x80B22404` / HTTP 404.

Therefore the 11.x / <=12.00 DPIv2 behavior is frozen. This repair is selected only from firmware 12.20 upward.

## New etaHEN 2.6B binary evidence

Reference supplied by the user: `etaHEN (1).elf`.
SHA-256: `ca60c615ba43d823bc5ccec86ef0b6b581aa8e79e73aaa4276cf92695049cbee`.

The extracted etaHEN 2.6B utility ELF calls `sceAppInstUtilInstallByPackage` in the DPIv2 URL handler at virtual address approximately `0x11fa80`.
Immediately before that call, the 0x30-byte `MetaInfo` object is copied from a six-qword all-zero template and only qword 0 (`uri`) is replaced with the submitted URL. Thus the call shape is:

- `uri = URL`
- `ex_uri = NULL`
- `playgo_scenario_id = NULL`
- `content_id = NULL`
- `content_name = NULL`
- `icon_url = NULL`

This is materially different from the older etaHEN source used by the tester baseline, which passed empty-string pointers and `content_name="etaHEN DPIv2"`.

The current etaHEN 2.6B legacy DPI path still uses the older non-NULL empty-string/content-name form, proving that this is a DPIv2-specific binary change rather than a generic structure-layout guess.

## PIZZA HEN policy

- <= 12.00: preserve the tester baseline URL MetaInfo byte-for-byte at source level.
- >= 12.20: zero-initialize `MetaInfo`, set only `.uri`, matching the observed etaHEN 2.6B DPIv2 URL call shape.
- DPIv2 port 12800, `sceAppInstUtilInitialize`, `PlayGoInfo`, `SceAppInstallPkgInfo`, upload-file path, Debug Services, Onion routing/fingerprints and CheatRunner are unchanged.

This is source/binary-grounded compatibility work. It is not claimed hardware-PASS until tested on 12.20+.
