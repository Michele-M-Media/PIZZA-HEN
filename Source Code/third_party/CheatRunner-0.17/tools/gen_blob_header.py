#!/usr/bin/env python3
"""PIZZA HEN integration adapter for CheatRunner v0.17 missing source helper."""
import pathlib, sys
if len(sys.argv) != 4:
    raise SystemExit("usage: gen_blob_header.py INPUT OUTPUT.h SYMBOL")
src,out,sym=sys.argv[1:]
data=pathlib.Path(src).read_bytes()
arr=', '.join(f'0x{b:02x}' for b in data)
pathlib.Path(out).write_text(
    '#pragma once\n'
    f'static const unsigned char {sym}[] = {{{arr}}};\n'
    f'static const unsigned long {sym}_len = {len(data)}UL;\n', encoding='utf-8')
