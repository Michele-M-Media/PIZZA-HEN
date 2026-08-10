#!/usr/bin/env python3
from pathlib import Path
import lzma, sys
if len(sys.argv) != 4:
    raise SystemExit("usage: pizzahen_pack_lzma.py INPUT OUTPUT_LZMA OUTPUT_SIZE")
src, out_lzma, out_size = map(Path, sys.argv[1:])
data = src.read_bytes()
out_size.write_text(str(len(data)), encoding="ascii")
out_lzma.write_bytes(lzma.compress(data, format=lzma.FORMAT_ALONE, preset=9))
