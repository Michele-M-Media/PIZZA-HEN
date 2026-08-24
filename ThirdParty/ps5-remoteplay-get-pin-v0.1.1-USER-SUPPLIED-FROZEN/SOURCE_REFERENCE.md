# Source reference

Upstream: https://github.com/idlesauce/ps5-remoteplay-get-pin

User-supplied ELF: `ps5-remoteplay-get-pin_v0.1.1.elf`
SHA-256: `1d611c1856dd2f4b4b6cb42ead1128a7f08a26585788f92de79fa4f67d721472`

The upstream Makefile builds the payload as `rp-get-pin.elf`. PIZZA HEN preserves the supplied ELF bytes but deploys it with that upstream basename so the payload's own duplicate-instance/cancel logic remains effective.
