#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'ThirdParty/Payload-Repository-USER-SUPPLIED-FROZEN/payloads-original.json'
RAR=ROOT/'ThirdParty/Payload-Repository-USER-SUPPLIED-FROZEN/Nuovo Archivio WinRAR(1).rar'
CAT=ROOT/'Source Code/util/assets/pizzahen_payloads.json'
HDR=ROOT/'Source Code/util/include/pizzahen_payloads_builtin.hpp'
CPP=ROOT/'Source Code/util/source/PayloadRepository.cpp'
UI=ROOT/'Source Code/bootstrapper/assets/toolbox_launcher.html'
GEN=ROOT/'TOOLS/generate_pizzahen_payload_repository.py'
BUILD=ROOT/'build_v01_rebase_latest_toolbox.sh'
checks=[]
def ck(n,x):
    x=bool(x); checks.append((n,x)); print(f'R723_{n}={"PASS" if x else "FAIL"}')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
orig=json.loads(SRC.read_text(encoding='utf-8'))
cat=json.loads(CAT.read_text(encoding='utf-8'))
items=cat.get('payloads',[])
cpp=CPP.read_text(encoding='utf-8'); ui=UI.read_text(encoding='utf-8'); build=BUILD.read_text(encoding='utf-8')
ck('RAR_FROZEN',RAR.is_file() and sha(RAR)=='e28561cad71ae226ebcc8275ce6c22a722db092696f6fc8fcbe2a5357855024d')
ck('SOURCE_FROZEN',SRC.is_file() and sha(SRC)=='38d799b96dd9e006d1f676f74f77264aaf0958506a772992cc62834661c05a59')
ck('SOURCE_COUNT_83',len(orig.get('payloads',[]))==83)
ck('SOURCE_ELF_COUNT_79',sum(str(x.get('filename','')).lower().endswith('.elf') for x in orig.get('payloads',[]))==79)
nonelf=[x.get('filename') for x in orig.get('payloads',[]) if not str(x.get('filename','')).lower().endswith('.elf')]
ck('SOURCE_NON_ELF_EXACT',nonelf==['etaHEN_v2.5B.bin','etaHEN-2.6B.bin','zftp_v1.5.0.bin','zhttp_v1.5.0.bin'])
ck('CATALOG_SCHEMA',cat.get('schema')=='pizzahen.payload-source.v1')
ck('CATALOG_NAME',cat.get('name')=='PIZZA HEN Payload Repository')
ck('CATALOG_COUNT_79',len(items)==79)
ck('CATALOG_ELF_ONLY',all(str(x.get('filename','')).lower().endswith('.elf') for x in items))
ck('CATALOG_SAFE_FILENAMES',all('/' not in x['filename'] and '\\' not in x['filename'] and '..' not in x['filename'] for x in items))
ck('CATALOG_URLS',all(str(x.get('url','')).startswith(('https://','http://')) for x in items))
ck('CATALOG_SHA256',all(re.fullmatch(r'[0-9a-fA-F]{64}',str(x.get('checksum',''))) for x in items))
ck('CATALOG_UNIQUE_FILENAMES',len({x['filename'] for x in items})==79)
ck('CATALOG_SHA_FROZEN',sha(CAT)=='cb730e5ad03fa4de038991c18249473d2b4328ebc51dcce3e11613aff3ad873f')
ck('HEADER_SHA_FROZEN',sha(HDR)=='cff209028bdfb9f82aeff633be4bbb9da63589aab69fde949797fa79b7e69611')
ck('HEADER_EMBEDS_JSON','kPizzahenPayloadRepositoryJson' in HDR.read_text(encoding='utf-8') and 'PIZZA HEN Payload Repository' in HDR.read_text(encoding='utf-8'))
ck('GENERATOR_PRESENT',GEN.is_file() and 'PIZZA_REPO_ELF_COUNT' in GEN.read_text(encoding='utf-8'))
ck('OLD_REMOTE_REMOVED','itsplk.github.io/ps5-payloads-mirror/payloads.json' not in cpp)
ck('BUILTIN_SOURCE','builtin://PIZZA_HEN/payloads.json' in cpp and 'kPizzahenPayloadRepositoryJson' in cpp)
ck('REFRESH_NO_REMOTE_DOWNLOAD','download_file(kRepo' not in cpp and 'write_source_cache(raw)' in cpp)
ck('PARSER_SCOPES_PAYLOADS','strstr(all,"\\"payloads\\"")' in cpp)
ck('RUNTIME_ELF_FILTER','valid_filename(fn)&&url_ok&&valid_sha256(item.checksum)' in cpp)
ck('INSTALL_SHA_VERIFY','compute_sha256_file' in cpp and 'strcasecmp(got,pick->checksum)' in cpp)
ck('UI_PIZZA_SOURCE','PIZZA HEN Payload Repository' in ui and 'Download catalogo Payload Manager' not in ui)
ck('UI_I18N_DYNAMIC',"phText('loading')" in ui and "b.textContent=phText('install')" in ui and "phText('error')" in ui)
a=ui.index('const PH_I18N=')+len('const PH_I18N='); b=ui.index(';\nconst PH_BASE_MAP=',a); i18n=json.loads(ui[a:b])
ck('I18N_31',len(i18n)==31)
ck('I18N_REPO_DYNAMIC_KEYS',all(all(d.get(k,'').strip() for k in ('loading','ready','error','install','none')) for d in i18n.values()))
ck('BUILD_GENERATES_REPO','generate_pizzahen_payload_repository.py' in build and 'PIZZA_REPO_MODE=BUILTIN_PIZZA_HEN_ELF_ONLY' in build)
ck('BUILD_GATE','test_r723_pizzahen_payload_repository.py' in build)
failed=[n for n,v in checks if not v]
print(f'R723_TOTAL={len(checks)} PASS={len(checks)-len(failed)} FAIL={len(failed)}')
sys.exit(1 if failed else 0)
