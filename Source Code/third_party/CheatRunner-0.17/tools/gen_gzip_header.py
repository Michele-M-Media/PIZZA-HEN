#!/usr/bin/env python3
"""PIZZA HEN integration adapter for CheatRunner v0.17.
The v0.17 source archive references tools/gen_gzip_header.py but does not ship it.
This adapter reads CheatRunner's C-string .inc asset, produces deterministic gzip (mtime=0),
and emits the exact symbols consumed by cr_api_dashboard.c.
"""
import ast, gzip, pathlib, sys
if len(sys.argv) != 4:
    raise SystemExit("usage: gen_gzip_header.py INPUT.inc OUTPUT.h SYMBOL")
src, out, sym = map(str, sys.argv[1:])
text=pathlib.Path(src).read_text(encoding='utf-8')
parts=[]
for raw in text.splitlines():
    line=raw.strip()
    if not line: continue
    try:
        v=ast.literal_eval(line)
    except Exception as e:
        raise SystemExit(f"cannot parse C-string line in {src}: {line[:80]}: {e}")
    if not isinstance(v,str): raise SystemExit(f"non-string literal in {src}")
    parts.append(v)
data=''.join(parts).encode('utf-8')
gz=gzip.compress(data, compresslevel=9, mtime=0)
arr=', '.join(f'0x{b:02x}' for b in gz)
pathlib.Path(out).write_text(
    '#pragma once\n'
    f'static const unsigned char {sym}[] = {{{arr}}};\n'
    f'static const unsigned long {sym}_len = {len(gz)}UL;\n', encoding='utf-8')
