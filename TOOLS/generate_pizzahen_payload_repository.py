#!/usr/bin/env python3
import argparse, hashlib, json, pathlib, re, sys

REQ = ('name','filename','url','description','version','category','checksum')
HEX64 = re.compile(r'^[0-9a-fA-F]{64}$')

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--source', required=True)
    ap.add_argument('--json-out', required=True)
    ap.add_argument('--header-out', required=True)
    args=ap.parse_args()
    src=pathlib.Path(args.source)
    jout=pathlib.Path(args.json_out)
    hout=pathlib.Path(args.header_out)
    data=json.loads(src.read_text(encoding='utf-8'))
    payloads=data.get('payloads')
    if not isinstance(payloads,list):
        raise SystemExit('payloads array missing')
    kept=[]; skipped=[]; seen=set()
    for idx,item in enumerate(payloads):
        if not isinstance(item,dict):
            raise SystemExit(f'payload[{idx}] is not an object')
        filename=str(item.get('filename',''))
        if not filename.lower().endswith('.elf'):
            skipped.append(filename)
            continue
        missing=[k for k in REQ if not isinstance(item.get(k),str) or not item.get(k)]
        if missing:
            raise SystemExit(f'{filename}: missing/invalid fields: {missing}')
        if '/' in filename or '\\' in filename or '..' in filename or len(filename)>240:
            raise SystemExit(f'{filename}: unsafe filename')
        if filename in seen:
            raise SystemExit(f'{filename}: duplicate filename')
        seen.add(filename)
        if not item['url'].startswith(('https://','http://')):
            raise SystemExit(f'{filename}: unsupported URL')
        if not HEX64.fullmatch(item['checksum']):
            raise SystemExit(f'{filename}: checksum must be SHA-256 hex')
        kept.append({k:item[k] for k in REQ})
    normalized={
        'name':'PIZZA HEN Payload Repository',
        'schema':'pizzahen.payload-source.v1',
        'payloads':kept,
    }
    text=json.dumps(normalized,ensure_ascii=False,indent=2)+'\n'
    if 'PIZZAREPO"' in text or ')PIZZAREPO"' in text:
        raise SystemExit('raw string delimiter collision')
    jout.parent.mkdir(parents=True,exist_ok=True)
    jout.write_text(text,encoding='utf-8')
    header=(
        '#pragma once\n'
        '// Generated from the user-supplied repository catalog. Do not hand-edit.\n'
        'static constexpr const char kPizzahenPayloadRepositoryJson[] = R"PIZZAREPO(\n'
        + text +
        ')PIZZAREPO";\n'
    )
    hout.parent.mkdir(parents=True,exist_ok=True)
    hout.write_text(header,encoding='utf-8')
    print(f'PIZZA_REPO_SOURCE_COUNT={len(payloads)}')
    print(f'PIZZA_REPO_ELF_COUNT={len(kept)}')
    print(f'PIZZA_REPO_SKIPPED_NON_ELF={len(skipped)}')
    print('PIZZA_REPO_SKIPPED_NAMES=' + ';'.join(skipped))
    print('PIZZA_REPO_JSON_SHA256=' + sha256_bytes(text.encode('utf-8')))
    print('PIZZA_REPO_HEADER_SHA256=' + sha256_bytes(header.encode('utf-8')))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
