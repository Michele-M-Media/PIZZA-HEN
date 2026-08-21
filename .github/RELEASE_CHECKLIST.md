# PIZZA HEN v1.0 Release Checklist

Use this checklist before merging the v1.0 release-preparation pull request into `main`.

- [ ] Final intended v1.0 source checkpoint has been synchronized to `release/v1.0`.
- [ ] Source tree matches the maintainer's hardware-tested checkpoint.
- [x] Canonical checkpoint SHA-256 verified: `354cb861325400930eaaf91706382a54897efe9ae425a80126c9313eef08b79b`.
- [x] Canonical checkpoint audit found no failed R7.14.x / R714 revision filenames or scanned references.
- [ ] Build completes with the intended PS5 Payload SDK/toolchain after the source sync.
- [x] Hardware status in README and release notes distinguishes confirmed vs experimental behavior.
- [x] DPIv2 12.x compatibility claim is limited to the hardware-confirmed 12.20–12.70 range.
- [x] Game Options CheatRunner shortcut remains marked experimental.
- [x] Third-party notices and licenses are retained in the canonical checkpoint.
- [ ] Final `Files changed` / source-sync diff has been reviewed before merge.
- [ ] Only after all items above are satisfied: merge PR #3 into `main`.

After merge, create the public `v1.0` tag/release from the verified `main` commit and attach only the intended public release artifacts.
