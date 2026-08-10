from pathlib import Path
root=Path(__file__).resolve().parents[1]
sc=(root/'Source Code').read_text() if False else ''
files={
'hooked': root/'Source Code/shellui/include/HookedFuncs.hpp',
'mono': root/'Source Code/shellui/src/MonoUtils.cpp',
'hook': root/'Source Code/shellui/src/HookFunctions.cpp',
'msg': root/'Source Code/util/source/msg.cpp',
'http': root/'Source Code/util/source/http.c',
'common': root/'Source Code/util/include/common_utils.h',
'cmake': root/'Source Code/unpacker/CMakeLists.txt',
}
t={k:p.read_text(errors='ignore') for k,p in files.items()}
checks=[]
def ok(name, cond):
    print(f'{name}={"PASS" if cond else "FAIL"}')
    checks.append((name,cond))
ok('FIX29_TARGET','PIZZA-HEN-v0.1-FIX45-PLUGIN-MANAGER-LIFECYCLE.elf' in t['cmake'])
ok('REPO_ENUM_4', all(x in t['hooked'] for x in ['CHEATS_REPO_HEN_COLLECTION','CHEATS_REPO_ETAHEN','CHEATS_REPO_GOLDHEN','CHEATS_REPO_RDX_PPSA']))
ok('UNIFIED_DEFAULT','selected_cheats_repo = CHEATS_REPO_HEN_COLLECTION' in t['hooked'])
ok('TOOLBOX_UNIFIED','Unified Collection (HEN-Cheats-Collection) - Recommended' in t['mono'])
ok('TOOLBOX_ETAHEN_SOURCE','PS5_Cheats Upstream Repository' in t['mono'])
ok('TOOLBOX_GOLDHEN','GoldHEN Cheat Repository' in t['mono'])
ok('TOOLBOX_RDX','RDX HEN-PPSA-Cheats' in t['mono'])
ok('SOURCE_URL_HEN','TeeKay87/HEN-Cheats-Collection' in t['msg'])
ok('SOURCE_URL_ETAHEN','etaHEN/PS5_Cheats' in t['msg'])
ok('SOURCE_URL_GOLDHEN','GoldHEN/GoldHEN_Cheat_Repository' in t['msg'])
ok('SOURCE_URL_RDX','RDX-Sci01/HEN-PPSA-Cheats' in t['msg'])
ok('SUBROOT_EXTRACT','extract_zip_subdir' in t['common'] and 'extract_zip_internal' in t['http'])
ok('STAGED_SWAP', all(x in t['msg'] for x in ['cheats.new','cheats.old','rename(stage_dir, active_dir)']))
ok('INDEX_GATE','Downloaded repository has no supported cheat index' in t['msg'])
ok('PER_SOURCE_COMMITS', all(x in t['http'] for x in ['cheat_commit_hencollection.txt','cheat_commit_etahen.txt','cheat_commit_goldhen.txt','cheat_commit_rdx.txt']))
ok('SOURCE_NAME_HELPER','pizzahen_cheat_repo_name' in t['hook'])
ok('NO_BINARY_UNION', 'Unified HEN-Cheats-Collection' in t['msg'])
failed=[n for n,c in checks if not c]
if failed: raise SystemExit('FIX29_STATIC_FAIL='+','.join(failed))
print(f'FIX29_STATIC={len(checks)}/{len(checks)} PASS')
