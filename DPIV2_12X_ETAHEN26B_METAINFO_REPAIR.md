# DPIv2 12.20+ etaHEN 2.6B MetaInfo repair

Baseline: `PIZZA-HEN-v1.0-MULTILANGUAGE-CHEATRUNNER-COMPILE-REPAIR.zip`
Baseline SHA-256: `9f9dafef3000c9257f7a8ccc0b7ac0000c07a88fcf1b7beebc7fa0d1b9308783`

## Hardware evidence before this repair

- 11.60: Debug Services PASS; DPIv2 PASS.
- 12.20 before repair: DPIv2 URL install returned `0x80B22404` / HTTP 404.

Therefore the 11.x / <=12.00 DPIv2 behavior was frozen and the repair is selected only from firmware 12.20 upward.

## etaHEN 2.6B binary evidence

The observed etaHEN 2.6B DPIv2 URL handler zero-initializes the six-qword `MetaInfo` object and sets only qword 0 (`uri`) before `sceAppInstUtilInstallByPackage`.

PIZZA HEN therefore uses:

- `uri = URL`
- `ex_uri = NULL`
- `playgo_scenario_id = NULL`
- `content_id = NULL`
- `content_name = NULL`
- `icon_url = NULL`

for firmware 12.20+ while preserving the prior URL behavior on <=12.00.

## Final hardware status

For the v1.0 release checkpoint, the DPIv2 12.x path is hardware-confirmed on firmware **12.20 through 12.70**.
