# PIZZA HEN v1.0 Release Checklist

Use this checklist before merging the v1.0 release-preparation pull request into `main`.

- [ ] Final intended v1.0 source checkpoint has been manually synchronized to `release/v1.0`.
- [ ] Source tree matches the maintainer's hardware-tested checkpoint.
- [ ] No failed R7.14.x experimental shortcut revisions are included unintentionally.
- [ ] Build completes with the intended PS5 Payload SDK/toolchain.
- [ ] Hardware status in README and release notes matches actual tests.
- [ ] DPIv2 12.x compatibility claim remains limited to the hardware-confirmed 12.20–12.70 range.
- [ ] Game Options CheatRunner shortcut remains marked experimental unless separately reconfirmed on hardware.
- [ ] Third-party notices and licenses remain intact.
- [ ] No credentials, tokens, private paths, private logs, or personal data are committed.
- [ ] `Files changed` has been reviewed before merge.
- [ ] Only after all items above are satisfied: merge PR #3 into `main`.

After merge, create the public `v1.0` tag/release from the verified `main` commit and attach only the intended public release artifacts.
