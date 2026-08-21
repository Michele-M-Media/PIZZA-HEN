# PIZZA HEN CheatRunner v0.17 build adapter

The supplied CheatRunner v0.17 source archive (commit `9c75165182bedb9c21e9b58a1468caeb8a3fdb0f`) references `tools/gen_gzip_header.py` and `tools/gen_blob_header.py` from CMake but does not contain those files. PIZZA HEN adds only these deterministic build-time generators. They do not change CheatRunner runtime logic, API, data paths, port, trainer formats, or dashboard source.
