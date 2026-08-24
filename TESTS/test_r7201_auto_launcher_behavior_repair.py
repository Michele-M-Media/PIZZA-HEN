#!/usr/bin/env python3
from pathlib import Path
import json,re,sys,zipfile
ROOT=Path(__file__).resolve().parents[1]
UI=(ROOT/'Source Code/bootstrapper/assets/toolbox_launcher.html').read_text(encoding='utf-8')
BUILD=(ROOT/'build_v01_rebase_latest_toolbox.sh').read_text(encoding='utf-8')
checks=[]
def ck(n,x): checks.append((n,bool(x))); print(f'R7201_{n}={"PASS" if x else "FAIL"}')

def extract_obj(marker):
    a=UI.index(marker)+len(marker); d=0; ins=False; esc=False
    for i,ch in enumerate(UI[a:],a):
        if ins:
            if esc: esc=False
            elif ch=='\\': esc=True
            elif ch=='"': ins=False
        else:
            if ch=='"': ins=True
            elif ch=='{': d+=1
            elif ch=='}':
                d-=1
                if d==0: return json.loads(UI[a:i+1])
    raise RuntimeError(marker)
i18n=extract_obj('const PH_I18N=')
ck('I18N_31',len(i18n)==31)
req=('homebrew_channel_desc','homebrew_channel_opening','apr_emu_desc','apr_emu_starting','game_compressor_desc','game_compressor_starting')
ck('I18N_KEYS',all(all(k in v and v[k] for k in req) for v in i18n.values()))
ck('I18N_NO_OLD_NO_PKG_COPY',all('without a Launcher PKG' not in v['homebrew_channel_desc'] for v in i18n.values()))
ck('HOME_SUPERSEDED_NO_TILE', 'no launcher PKG or home-screen tile' in i18n['en-US']['homebrew_channel_desc'])
ck('APR_SUPERSEDED_NO_TILE','launcher PKG/tile disabled' in i18n['en-US']['apr_emu_desc'])
ck('GC_SUPERSEDED_NO_TILE','no PSGC50001 tile' in i18n['en-US']['game_compressor_desc'])
ck('NO_DUPLICATED_COPY','and automatically manages its home-screen launcher tile and automatically' not in UI and '; automatically manages launcher tile PSGC50001; automatically' not in UI)
ck('HOME_DIRECT_ROUTE',"const HOMEBREW_CHANNEL_URL='/index.html';" in UI and 'location.href=HOMEBREW_CHANNEL_URL' in UI)
ck('HOME_NO_MANUAL_PKG_CALL','.pkg' not in re.search(r'async function openHomebrewChannel\(el\).*?const APR_EMU_UPDATER_PATH',UI,re.S).group(0).lower())
ck('APR_ON_DEMAND','launchElfDirect(APR_EMU_UPDATER_PATH)' in UI and "APR_EMU_UPDATER_URL='http://127.0.0.1:6971/'" in UI)
ck('GC_ON_DEMAND',"runAction('plugin-launch '+GAME_COMPRESSOR_PATH+' GameCompressor')" in UI and "GAME_COMPRESSOR_URL='http://127.0.0.1:5910/'" in UI)
ck('BUILD_HOME_METADATA','R716_HOMEBREW_CHANNEL_LAUNCHER=DISABLED_IN_PIZZA_INTEGRATED_WEBSRV' in BUILD)
ck('BUILD_APR_METADATA','APR_EMU_UPDATER_LAUNCHER=DISABLED_AUTO_THREAD_AND_TILE_ENDPOINT' in BUILD)
ck('BUILD_GC_METADATA','R720_GAME_COMPRESSOR_TILE=DISABLED_GC_LAUNCHER_START' in BUILD)
ck('BUILD_POLICY','R7201_AUTO_LAUNCHER_BEHAVIOR=SUPERSEDED_BY_R7202_NO_TILE' in BUILD and 'R7202_PKG_POLICY=NO_PKG_NO_HOME_TILE' in BUILD)
# Source-ground the two automatic launcher cases directly from the frozen user-supplied archives.
aprzip=ROOT/'ThirdParty/apr-emu-updater-1.4-USER-SUPPLIED-FROZEN/apr-emu-updater-1.4.zip'
with zipfile.ZipFile(aprzip) as z:
    name=next(n for n in z.namelist() if n.endswith('/README.md') or n=='README.md')
    apr=z.read(name).decode('utf-8','ignore')
ck('APR_SOURCE_TILE','puts a tile on the **home screen**' in apr)
gczip=ROOT/'ThirdParty/PS5-Game-Compressor-1.0.4-USER-SUPPLIED-FROZEN/PS5-Game-Compressor-1.0.4.zip'
with zipfile.ZipFile(gczip) as z:
    names=z.namelist()
    mainn=next(n for n in names if n.endswith('/src/gc_main.c') or n=='src/gc_main.c')
    instn=next(n for n in names if n.endswith('/src/gc_app_installer.c') or n=='src/gc_app_installer.c')
    gm=z.read(mainn).decode('utf-8','ignore'); gi=z.read(instn).decode('utf-8','ignore')
ck('GC_SOURCE_LAUNCHER_START','gc_launcher_start();' in gm)
ck('GC_SOURCE_APPINST','sceAppInstUtil' in gi and 'GAME_COMPRESSOR_LAUNCHER_TITLE_ID' in gi)
ck('DOC', (ROOT/'R7_20_1_AUTO_LAUNCHER_BEHAVIOR_REPAIR.md').exists())
ok=sum(x for _,x in checks)
print(f'R7_20_1_AUTO_LAUNCHER_BEHAVIOR_REPAIR={ok}/{len(checks)} {"PASS" if ok==len(checks) else "FAIL"}')
sys.exit(0 if ok==len(checks) else 1)
