#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
import hashlib, json, re, sys

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Source Code'
TOOL=SRC/'bootstrapper/assets/toolbox_launcher.html'
DBG=SRC/'bootstrapper/assets/debug_services_launcher.html'
KS=SRC/'bootstrapper/assets/kstuff_selector.js'
SH=SRC/'bootstrapper/assets/shadowmount_selector.html'

fails=[]
def ck(name,cond):
    print(name+'='+('PASS' if cond else 'FAIL'))
    if not cond:fails.append(name)

def sha_file(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

tool=TOOL.read_text(encoding='utf-8')
m=re.search(r'const PH_I18N=(\{.*?\});\nconst PH_BASE_MAP=',tool,re.S)
i18n=json.loads(m.group(1)) if m else {}
m2=re.search(r'const PH_BASE_MAP=(\{.*?\});\nfunction phNormalizeLocale',tool,re.S)
base_map=json.loads(m2.group(1)) if m2 else {}
locales=list(i18n)
ck('V200_I18N_31_LOCALES',len(locales)==31)
base_keys=set(i18n.get('en-US',{}))
ck('V200_I18N_EQUAL_KEYSETS',all(set(v)==base_keys for v in i18n.values()))
ck('V200_I18N_NO_EMPTY_VALUES',all(all(str(x).strip() for x in v.values()) for v in i18n.values()))
ck('V200_I18N_ARABIC_RTL',"document.documentElement.dir=PH_LOCALE==='ar-SA'?'rtl':'ltr'" in tool)
ck('V200_POORDS4_KEYS_ALL',all(all(k in v for k in ['poords4_intro','poords4_bridge_title','poords4_bridge_desc','poords4_status_title','poords4_status_desc','poords4_stop_title','poords4_stop_desc','poords4_warning','poords4_rest_note']) for v in i18n.values()))
ck('V200_FAN_KEYS_ALL',all(all(k in v for k in ['fan_dual_desc','fan_option1','fan_option1_desc','fan_option1_recommended','fan_option1_switch','fan_option2','fan_option2_target_desc','fan_option2_target_label','fan_v03_desc','fan_v03_footer']) for v in i18n.values()))

TECHNICAL_ALLOWED=set(["/data/PIZZA_HEN/payloads/pizza_overlay.elf", "/hbldr", "0%", "127.0.0.1:8080", "127.0.0.1:8080 · IPC · /hbldr", "65 °C", "70 °C", "75 °C", "80 °C", "85 °C", "AirPSX 0.19", "BFplayer standalone alpha.44", "BFplayer-standalone_v0.1.0-alpha.44.elf — TCP 9040", "BackPork 0.1", "Chukei DNS 0.9.0", "ELF Loader 0.24", "FIX70.20:", "Garlic SaveMgr", "Ghostcontrol 1.0.5", "Ghostpad 1.0.0", "KlogSrv", "NP Environment", "NP Fake Signin 1.3", "PIZZA HEN", "PIZZA HEN Toolbox", "PIZZA HEN v2.00 — Michele Media", "PIZZA Overlay", "PKGInstall", "PS Game State Lib 0.1", "PS-DiscordPresence 0.01", "PS-Play 2.1", "PS-Play_v2.1.elf — TCP 9055", "PS5 App Dumper 1.11", "PS5 Custom Tool Manager", "PS5 FW Spoof", "PS5 Fan Control v0.3", "PS5 Linux Loader 2.4", "PS5 Wallpaper Modder v1.0", "PS5Upload 5.4.8", "PoorDS4", "ProsperoPlayer 1.0", "ProsperoPlayer_v1.0.elf — TCP 9055", "UnRAR PS5 1.4.0", "WebKit Autoloader Installer", "nanoDNS 0.4", "›"])
class StaticTextParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack=[]; self.text=[]
    def handle_starttag(self,tag,attrs):
        self.stack.append(tag)
    def handle_endtag(self,tag):
        if self.stack:self.stack.pop()
    def handle_data(self,data):
        if self.stack and self.stack[-1] in ('script','style'): return
        s=data.strip()
        if s and s.lower()!='html': self.text.append(s)
p=StaticTextParser(); p.feed(tool)
unmapped=sorted(set(s for s in p.text if s not in base_map and s not in i18n['en-US'].values() and s not in TECHNICAL_ALLOWED))
ck('V200_STATIC_VISIBLE_TEXT_COVERED',not unmapped)
if unmapped: print('V200_UNMAPPED_STATIC='+repr(unmapped))

DYNAMIC_REQUIRED=["Avvio installazione Homebrew Store tramite handler etaHEN originale…", "Catalogo PKG non disponibile.", "Catalogo non disponibile.", "Comando etaHEN DownloadTheStore inviato al daemon.", "No games found in PIZZA HEN game roots.", "Scanning PIZZA HEN game roots…", "Scansione PKG già in corso…", "Scansione Plugins / Payload ELFs…", "Scansione USB / dischi esterni in coda…", "Scansione completata, caricamento catalogo…", "upstream websrv PKGInstall returned", "websrv PKGInstall launch failed", "Nessun plugin o payload trovato.", "Nessun PKG trovato.", "FAIL", "SENT"]
ck('V200_FIXED_DYNAMIC_STATUS_COVERED',all(s in base_map for s in DYNAMIC_REQUIRED))
ck('V200_POORDS4_VISIBLE_MAP',all(s in base_map for s in [
 'PoorDS4 0.1.0-rc38 by ItsBlurf. Original upstream release payloads, embedded and deployed byte-for-byte without binary modification.',
 'Automatic wireless DS4 bridge — RC38','Read-only status snapshot','Cooperative stop',
 'No status snapshot requested.'
]))
ck('V200_FAN_VISIBLE_MAP',all(s in base_map for s in [
 'Due implementazioni separate. PIZZA HEN non modifica i payload: quando ne attivi una, ferma l’altra per evitare che due daemon riscrivano contemporaneamente la soglia della ventola.',
 'Opzione 1 — fan_target 0.1','Opzione 2 — ps5-fan-control v0.3',
 'Temperatura obiettivo — Opzione 2'
]))

def functions(js):
    starts=[]
    for mm in re.finditer(r'(?:(async)\s+)?function\s+([A-Za-z_$][\w$]*)\s*\([^)]*\)\s*\{',js):
        starts.append((mm.start(),mm.group(2),mm.end()-1))
    out={}
    for st,name,brace in starts:
        depth=0; ins=None; esc=False; line=False; block=False; i=brace
        while i<len(js):
            c=js[i]; n=js[i+1] if i+1<len(js) else ''
            if line:
                if c=='\n':line=False
                i+=1;continue
            if block:
                if c=='*' and n=='/':block=False;i+=2;continue
                i+=1;continue
            if ins:
                if esc:esc=False
                elif c=='\\':esc=True
                elif c==ins:ins=None
                i+=1;continue
            if c=='/' and n=='/':line=True;i+=2;continue
            if c=='/' and n=='*':block=True;i+=2;continue
            if c in "'\"`":ins=c;i+=1;continue
            if c=='{':depth+=1
            elif c=='}':
                depth-=1
                if depth==0:
                    out[name]=js[st:i+1];break
            i+=1
    return out
f=functions(tool)
blob='\n\n'.join(k+'\n'+f[k] for k in sorted(f))
ck('V200_TOOLBOX_127_FUNCTIONS_FROZEN',len(f)==127 and hashlib.sha256(blob.encode()).hexdigest()=='c691490f4d37de43e5e3b8c788be3eb0796ec7f0a683f1d82b0665da9a68a8c4')
for name,expected in {
 'scanPkgs':'10d842aec854f6b1ffbc63b383023c28f30ddf70f87a0823fec8fc5f74c71c2b',
 'loadPkgCatalog':'86a25d4b7df94dd51ade747e4bea58ce4065e6ea7c09550929bfa0e40e372483',
 'installPkg':'5f3a7df595f36db5f369063a6269ae3cab9b72398bd979a015955142afe37e2b',
}.items():
    ck('V200_FROZEN_'+name, name in f and hashlib.sha256(f[name].encode()).hexdigest()==expected)

ck('V200_DEBUG_SERVICES_HARDWARE_FROZEN',sha_file(DBG)=='7f7134593eefa9628bc581eebe3a7fc66f40cba3bb8f9447ebd641bfe58eb399')

ks=KS.read_text(encoding='utf-8')
mk=re.search(r'const PH_SELECTOR_I18N=(\{.*?\});\nfunction phNormalizeLocale',ks,re.S)
ks_i=json.loads(mk.group(1)) if mk else {}
ck('V200_KSTUFF_31_LOCALES',len(ks_i)==31 and all(set(v)==set(ks_i['en-US']) for v in ks_i.values()))
sh=SH.read_text(encoding='utf-8')
ms=re.search(r'const I18N=(\{.*?\});\nfunction norm',sh,re.S)
sh_i=json.loads(ms.group(1)) if ms else {}
ck('V200_SHADOWMOUNT_31_LOCALES',len(sh_i)==31 and all(set(v)==set(sh_i['en-US']) for v in sh_i.values()))

expected={'en-US','en-GB','it-IT','fr-FR','fr-CA','de-DE','es-ES','es-419','pt-BR','pt-PT','nl-NL','da-DK','sv-SE','no-NO','fi-FI','pl-PL','cs-CZ','ro-RO','hu-HU','el-GR','tr-TR','ru-RU','uk-UA','id-ID','vi-VN','ja-JP','ko-KR','zh-Hans','zh-Hant','ar-SA','th-TH'}
hook=(SRC/'shellui/src/HookFunctions.cpp').read_text(encoding='utf-8',errors='ignore')
msg=(SRC/'util/source/msg.cpp').read_text(encoding='utf-8',errors='ignore')
hook_codes=set(re.findall(r'\{"([a-z]{2}(?:-[A-Za-z0-9]+)+)"\s*,',hook))
msg_codes=set(re.findall(r'\{"([a-z]{2}(?:-[A-Za-z0-9]+)+)"\s*,',msg))
ck('V200_NATIVE_31_LOCALES',expected.issubset(hook_codes))
ck('V200_SERVICE_NOTIFY_31_LOCALES',expected.issubset(msg_codes))

EXPECTED_ELFS={
  "KSTUFF_INPUT/kstuff-base-1.6.7.elf": "f1c1f4b2b6395644af04cbe9828aba58586acf7aacb9e01113cac92ce16e3569",
  "KSTUFF_INPUT/kstuff-v1.10-normal.elf": "b1dfe57f367a35374f605127915eda38c76a6ed5d1c729e427955798bd78c66a",
  "Source Code/bootstrapper/assets/BFplayer-standalone_v0.1.0-alpha.44.elf": "0d028deb145d6fc9a5b55d43a45e072919178fbb261c66cd914ebcfb0b3b05c0",
  "Source Code/bootstrapper/assets/Chukei_DNS_v0.9.0.elf": "0cf13e1ed87b57ffa4fdcfca5d9afe1572be29b4f632677cedf17657a972d750",
  "Source Code/bootstrapper/assets/Ghostcontrol-PS5-USB-Controller-Patcher_v1.0.5.elf": "69271d91f27397c9ad42150129639ce452ecb405021108f42c6c87926123a6f1",
  "Source Code/bootstrapper/assets/Ghostpad_v1.0.0.elf": "94d43a8db7ec9df6e18f0a0da25aac0f60e1a0b14d35bfff261f6f5cdeabdba1",
  "Source Code/bootstrapper/assets/PS-DiscordPresence_v0.01.elf": "375cf619ea6f6c594ea2b79ecbb98704723522d07e51c877687876d5fe589afb",
  "Source Code/bootstrapper/assets/PS-Play_v2.1.elf": "e3392379d5bc6ca4e44cb0d2a1d8921083b2c3ea480725f68378831874542d8d",
  "Source Code/bootstrapper/assets/PS5-Custom-Tool-Manager-_vCustom-pizza-web-only.elf": "ecdf8a8eaa47f59bfe5b419dcb3f60bd3dc68deef9f36a5e36c125f3e71987b7",
  "Source Code/bootstrapper/assets/PS_Game_State_Lib_v0.1.elf": "a550e1494b0f8be3b244f8820ee8d899442d33a936f9ded6203a0318c7afdba8",
  "Source Code/bootstrapper/assets/ProsperoPlayer_v1.0.elf": "40b9955273982cd563e1b16bd428ea6a9c399e7d4bc55b220fe223948572cdad",
  "Source Code/bootstrapper/assets/Spectrum-Library.elf": "e747a5b01c468e1bbe7d09558751c90237e47a4d6bf932e1d174a4934b1afd4c",
  "Source Code/bootstrapper/assets/airpsx_v0.19.elf": "ae025ca7727b3a8abf6a705903ca9116a6fa6e7f7ead606916109cf9044c5d63",
  "Source Code/bootstrapper/assets/apr_emu_updater.elf": "fcd9472ea50141a51e3d6663aee2eadbe99b9e6e0cedf1421b7c1d67f62727a9",
  "Source Code/bootstrapper/assets/game-compressor.elf": "535aa4a8e951c04b98df33eb7d476dbcb6cbec080c00dfc8d574f1e61b233ac3",
  "Source Code/bootstrapper/assets/garlic-savemgr.elf": "124051ab3a762474720ae53187d2920bc96d6be1d69aa298e715667efc385a2f",
  "Source Code/bootstrapper/assets/kstuff-base-1.6.7.elf": "f1c1f4b2b6395644af04cbe9828aba58586acf7aacb9e01113cac92ce16e3569",
  "Source Code/bootstrapper/assets/nanoDNS_v0.4.elf": "18a93655c59ad32e371e14c86f32d14fbd1fbc47a0e907f3e0b6667efb3ad964",
  "Source Code/bootstrapper/assets/np-fake-signin_v1.3.elf": "f5c66fcb9e3f512e5463a7123d819b87f063d9955639366fa7ad26a2f0abefa4",
  "Source Code/bootstrapper/assets/pegasus-dl.elf": "730cb6be1d16e93f7b06b269e8fa56f45866ab2fc51ac2ef1e90bbf341a1c02a",
  "Source Code/bootstrapper/assets/ps5-app-dumper_v1.11.elf": "18483751ebaea6879b020a9dd87c0a4fb4f1bf09f3708d950362a483f78cc0d0",
  "Source Code/bootstrapper/assets/ps5-backpork.elf": "d74e4cd119b2bb1fd423f2f5b1c9a7f096b3e588c753af1ab48b983d56216a52",
  "Source Code/bootstrapper/assets/ps5-fw-spoof_v26616621599.elf": "f1754521caa92a6a1ac313a1b6c969ec49d67750e290ba99870958290a0961f0",
  "Source Code/bootstrapper/assets/ps5-linux-loader.elf": "51382795b486f7c5a3681648d457d129088311fc3f9601aeaff78dc72fafcf1d",
  "Source Code/bootstrapper/assets/ps5-wallpaper-modd_v1.0-pizza-web-only.elf": "a2fa5e9c8ecb794fed189bcd204008ea446a12c2d1381fa601734b3d915d5360",
  "Source Code/bootstrapper/assets/ps5upload_v5.4.8.elf": "b255217ffcb5bc93a0ecdd4612927f241fbef3b3f936874223fcfba4cff17cf5",
  "Source Code/bootstrapper/assets/rp-get-pin.elf": "1d611c1856dd2f4b4b6cb42ead1128a7f08a26585788f92de79fa4f67d721472",
  "Source Code/bootstrapper/assets/shadowmountplus-experimental.elf": "f15653fe90d81e5f82841ca693c0599d307c384d6454c1b0cc18190ae1ef4812",
  "Source Code/bootstrapper/assets/shadowmountplus.elf": "a35246fb3bb6042b25653b51cdcbc33254b40339342bf1d2dd0d2eceee2ca526",
  "Source Code/bootstrapper/assets/unrar-ps5_v1.4.0.elf": "2ef04b0bc8fc1932b29da1a53336c40ed0a3f6a945a0746bef2e5dde52149701",
  "Source Code/bootstrapper/assets/web-file-mgr.elf": "d0bc7620051079fff40147c4bcf364fda054b7e5bef9193abfba2ef76710006b",
  "Source Code/bootstrapper/assets/webkit-autoloader-installer_v0.4.0-pre-00e1028.elf": "b920bc73133764a9847975a402b6f3bd4d9d97c797159153ccc5bcb98b6ee025",
  "Source Code/bootstrapper/assets/websrv-ps5.elf": "16a18de9df60b4d726409121a2f24ea92616db03e1cc45fab49c8d05ae8b480c",
  "Source Code/daemon/assets/PoorDS4-status.elf": "c26a35a2c9ba9074ad33cf27a5afbd05536978518c546552df21d512b07a273d",
  "Source Code/daemon/assets/PoorDS4-stop.elf": "bf9f1dec35edcffe3744fbc69cb7d4601f6df3cef72fab36c38fd249e736107a",
  "Source Code/daemon/assets/PoorDS4rc38.elf": "62d21fe837ee53dd4291e45d99259d4557def05e2d4196ab54e020ba28b5399e",
  "Source Code/daemon/assets/fan_target_65c.elf": "0bedeb564947530d09d1dfb27df63c2a09eaa7f51faf3ddcc90b3fb2870e6312",
  "Source Code/daemon/assets/fan_target_70c.elf": "a9ad8502123799d58f8ddd9882d842f524c4ecc3ea6743a73c6dcdffd0bf30e0",
  "Source Code/daemon/assets/fan_target_75c.elf": "4b52e09c48ebed1f369221c290e8ec4a9fdb2a477b7b7f44a1b8646958d9f69b",
  "Source Code/daemon/assets/fan_target_80c.elf": "ccf2e709218f31cd9e6a0705c99646b8f030b877687df8377982a2f6ca10216e",
  "Source Code/daemon/assets/fan_target_85c.elf": "c37019c351c1c5b05b43adbac29d85bfd25f8c0ab9d94371cacab1945d8e0fd0",
  "Source Code/daemon/assets/klogsrv-ps5.elf": "e828ec144231f81547cb58bc7d2c396fa984be0c2295f31364b58017816dcceb",
  "Source Code/daemon/assets/kstuff-toggle-1.elf": "9009b96f36721a1b4c305735038d70cd72d596c553156bfa2a27e60a68ae2dee",
  "Source Code/daemon/assets/kstuff-toggle-2.elf": "ae8c39e79f731b5b0515b8487ff7986cf9a626e760881dacc107bd888f3694c6",
  "Source Code/daemon/assets/kstuff-toggle-3.elf": "0e87e92959791d9edf04c314802fcf18ccf37db74ae353d434a0062557f85093",
  "Source Code/daemon/assets/pizza_overlay_phu_fw1220plus.elf": "af930375e1be960254ce2ac70fbd29230b9f67937cf69bca8b66520371bdbb3b",
  "Source Code/daemon/assets/pizza_overlay_phu_original.elf": "8e20deefb9100705be8352dc6acb47241c6a044b93dc3f578f93c424789b2622",
  "Source Code/daemon/assets/ps5-fan-control-v0.3.elf": "b10b6b9b9c00efed8bf9202a83b6cb762345d1f84130a419eff7139250026b36",
  "Source Code/daemon/assets/ps5debug.elf": "dae56bf7a30caa5f4eee929ec6a3dd0051e6da1a3651d9b20c299f339f36e43f",
  "ThirdParty/BFplayer-v0.1.0-alpha.44-USER-SUPPLIED-FROZEN/BFplayer-standalone_v0.1.0-alpha.44.elf": "0d028deb145d6fc9a5b55d43a45e072919178fbb261c66cd914ebcfb0b3b05c0",
  "ThirdParty/BackPork-0.1-USER-SUPPLIED-FROZEN/ps5-backpork.elf": "d74e4cd119b2bb1fd423f2f5b1c9a7f096b3e588c753af1ab48b983d56216a52",
  "ThirdParty/Chukei-DNS-v0.9.0-USER-SUPPLIED-FROZEN/Chukei_DNS_v0.9.0.elf": "0cf13e1ed87b57ffa4fdcfca5d9afe1572be29b4f632677cedf17657a972d750",
  "ThirdParty/Garlic-SaveMgr-USER-SUPPLIED-FROZEN/garlic-savemgr.elf": "124051ab3a762474720ae53187d2920bc96d6be1d69aa298e715667efc385a2f",
  "ThirdParty/Ghostcontrol-v1.0.5-USER-SUPPLIED-FROZEN/Ghostcontrol-PS5-USB-Controller-Patcher_v1.0.5.elf": "69271d91f27397c9ad42150129639ce452ecb405021108f42c6c87926123a6f1",
  "ThirdParty/Ghostpad-v1.0.0-USER-SUPPLIED-FROZEN/Ghostpad_v1.0.0.elf": "94d43a8db7ec9df6e18f0a0da25aac0f60e1a0b14d35bfff261f6f5cdeabdba1",
  "ThirdParty/PS-DiscordPresence-v0.01-USER-SUPPLIED-FROZEN/PS-DiscordPresence_v0.01.elf": "375cf619ea6f6c594ea2b79ecbb98704723522d07e51c877687876d5fe589afb",
  "ThirdParty/PS-Game-State-Lib-v0.1-USER-SUPPLIED-FROZEN/PS_Game_State_Lib_v0.1.elf": "a550e1494b0f8be3b244f8820ee8d899442d33a936f9ded6203a0318c7afdba8",
  "ThirdParty/PS-Play-v2.1-USER-SUPPLIED-FROZEN/PS-Play_v2.1.elf": "e3392379d5bc6ca4e44cb0d2a1d8921083b2c3ea480725f68378831874542d8d",
  "ThirdParty/PS5-Custom-Tool-Manager-vCustom-USER-SUPPLIED-ORIGINAL/PS5-Custom-Tool-Manager-_vCustom.elf": "297824ceaf6ea53fde57550adf9b5c2fc44c63ef60e8196ab92d351d1615d9cb",
  "ThirdParty/PS5-Game-Compressor-1.0.4-USER-SUPPLIED-FROZEN/game-compressor.elf": "e55e90aaade13b6e0d4316c1597ef90a21b67a06475c3e25de054224bc1e941b",
  "ThirdParty/PoorDS4-0.1.0-rc38-USER-SUPPLIED-FROZEN/PoorDS4-status.elf": "c26a35a2c9ba9074ad33cf27a5afbd05536978518c546552df21d512b07a273d",
  "ThirdParty/PoorDS4-0.1.0-rc38-USER-SUPPLIED-FROZEN/PoorDS4-stop.elf": "bf9f1dec35edcffe3744fbc69cb7d4601f6df3cef72fab36c38fd249e736107a",
  "ThirdParty/PoorDS4-0.1.0-rc38-USER-SUPPLIED-FROZEN/PoorDS4rc38.elf": "62d21fe837ee53dd4291e45d99259d4557def05e2d4196ab54e020ba28b5399e",
  "ThirdParty/ProsperoPlayer-v1.0-USER-SUPPLIED-FROZEN/ProsperoPlayer_v1.0.elf": "40b9955273982cd563e1b16bd428ea6a9c399e7d4bc55b220fe223948572cdad",
  "ThirdParty/R7.19-USER-SUPPLIED-SERVICES-FROZEN/airpsx_v0.19.elf": "ae025ca7727b3a8abf6a705903ca9116a6fa6e7f7ead606916109cf9044c5d63",
  "ThirdParty/R7.19-USER-SUPPLIED-SERVICES-FROZEN/np-fake-signin_v1.3.elf": "f5c66fcb9e3f512e5463a7123d819b87f063d9955639366fa7ad26a2f0abefa4",
  "ThirdParty/R7.19-USER-SUPPLIED-SERVICES-FROZEN/ps5-app-dumper_v1.11.elf": "18483751ebaea6879b020a9dd87c0a4fb4f1bf09f3708d950362a483f78cc0d0",
  "ThirdParty/R7.19-USER-SUPPLIED-SERVICES-FROZEN/ps5-fw-spoof_v26616621599.elf": "f1754521caa92a6a1ac313a1b6c969ec49d67750e290ba99870958290a0961f0",
  "ThirdParty/R7.19-USER-SUPPLIED-SERVICES-FROZEN/ps5upload_v5.4.8.elf": "b255217ffcb5bc93a0ecdd4612927f241fbef3b3f936874223fcfba4cff17cf5",
  "ThirdParty/R7.19-USER-SUPPLIED-SERVICES-FROZEN/webkit-autoloader-installer_v0.4.0-pre-00e1028.elf": "b920bc73133764a9847975a402b6f3bd4d9d97c797159153ccc5bcb98b6ee025",
  "ThirdParty/SVT-Play-v0.2-USER-SUPPLIED-FROZEN/svtplay_v0.2.elf": "5bdf25142512f25dc6269bd7c90a914001fcef5e731125a74aa23c1a8d91810f",
  "ThirdParty/ShadowMountPlus-1.6beta16-UPSTREAM-FROZEN/shadowmountplus.elf": "a35246fb3bb6042b25653b51cdcbc33254b40339342bf1d2dd0d2eceee2ca526",
  "ThirdParty/ShadowMountPlus-1.7alpha8-EXPERIMENTAL-FROZEN/shadowmountplus.elf": "f15653fe90d81e5f82841ca693c0599d307c384d6454c1b0cc18190ae1ef4812",
  "ThirdParty/Spectrum-Library-v1.4.2-USER-SUPPLIED-FROZEN/Spectrum-Library_v1.4.2.elf": "54755ce62d99be610afe364e26de05eaa9e2d92192cda525790a563c6296261f",
  "ThirdParty/THEMES-AVATAR-INTEGRATED-DERIVED/PS5-Custom-Tool-Manager-_vCustom-pizza-web-only.elf": "ecdf8a8eaa47f59bfe5b419dcb3f60bd3dc68deef9f36a5e36c125f3e71987b7",
  "ThirdParty/THEMES-AVATAR-INTEGRATED-DERIVED/ps5-wallpaper-modd_v1.0-pizza-web-only.elf": "a2fa5e9c8ecb794fed189bcd204008ea446a12c2d1381fa601734b3d915d5360",
  "ThirdParty/apr-emu-updater-1.4-USER-SUPPLIED-FROZEN/apr_emu_updater.elf": "684a7e824e03f2402693641f347341a118fa0ac7a9573f212036a0a5337a8054",
  "ThirdParty/ftpsrv-0.21-UPSTREAM-FROZEN/ftpsrv-ps5.elf": "c580f0534ac6349dc5a4a5c656eaced537b4c2b18da51886d943cea6393436c8",
  "ThirdParty/kstuff-1.6.7-BASE-USER-SUPPLIED-FROZEN/kstuff-base-1.6.7.elf": "f1c1f4b2b6395644af04cbe9828aba58586acf7aacb9e01113cac92ce16e3569",
  "ThirdParty/kstuff-dr-1.2-test1-UPSTREAM-FROZEN/kstuff-dr-1.2-test1.elf": "9c1b242eaed3704ef18be45d001a2c4ebf2d9222cfe3cbb0f0c3db33309abac9",
  "ThirdParty/nanoDNS-v0.4-USER-SUPPLIED-FROZEN/nanoDNS_v0.4.elf": "18a93655c59ad32e371e14c86f32d14fbd1fbc47a0e907f3e0b6667efb3ad964",
  "ThirdParty/pegasus-dl-v1.7.0-USER-SUPPLIED-FROZEN/pegasus-dl_v1.7.0.elf": "cb2a4b3c248323f2432ce118cb1bf4975146035239ce9b571a9bdb51b3fee226",
  "ThirdParty/ps5-elfldr-0.24-148b71c-UPSTREAM-FROZEN/elfldr-ps5-v0.24-148b71c.elf": "6bf3a5416c84305f4e62cc952861f810806eb6613a3d24c4b35f947f2650ba33",
  "ThirdParty/ps5-fan-control-v0.3-USER-SUPPLIED-FROZEN/ps5-fan-control-v0.3.elf": "b10b6b9b9c00efed8bf9202a83b6cb762345d1f84130a419eff7139250026b36",
  "ThirdParty/ps5-linux-loader-v2.4-USER-SUPPLIED-FROZEN/ps5-linux-loader_v2.4.elf": "51382795b486f7c5a3681648d457d129088311fc3f9601aeaff78dc72fafcf1d",
  "ThirdParty/ps5-remoteplay-get-pin-v0.1.1-USER-SUPPLIED-FROZEN/ps5-remoteplay-get-pin_v0.1.1.elf": "1d611c1856dd2f4b4b6cb42ead1128a7f08a26585788f92de79fa4f67d721472",
  "ThirdParty/ps5-wallpaper-modd-v1.0-USER-SUPPLIED-ORIGINAL/ps5-wallpaper-modd_v1.0.elf": "b18a866bac9deff45b921b7d3ea6143d541117b56c666d817ecdc81961829139",
  "ThirdParty/ps5-web-file-manager-v1.5-USER-SUPPLIED-FROZEN/ps5-web-file-manager_v1.5.elf": "9a7d7e5c685900d7f916cdc08cb6f7ea7e9cf5a4576f2799157b3f251deedf3c",
  "ThirdParty/ps5debug-NG-1.3.0-UPSTREAM-FROZEN/ps5debug-NG_v1.3.0.elf": "8f75fb90b45d7cc4d59147e3323577d7264cf572c78a27f76722202f492ad16a",
  "ThirdParty/unrar-ps5-v1.4.0-USER-SUPPLIED-FROZEN/unrar-ps5_v1.4.0.elf": "2ef04b0bc8fc1932b29da1a53336c40ed0a3f6a945a0746bef2e5dde52149701",
  "ThirdParty/websrv-0.34-UPSTREAM-FROZEN/websrv-ps5.elf": "54730c867c6e1148536fdcb370e63a7762d989ea87b62488ad4caff64d43f263"
}
TRANSIENT_ELF_PREFIXES=('Source Code/build/','Source Code/bin/','OUTPUT/','BUILD_LOGS/')
GENERATED_BOOTSTRAPPER_STAGE_ELFS={
  'Source Code/bootstrapper/assets/ftpsrv-ps5.elf',
  'Source Code/bootstrapper/assets/kstuff-dr-1.2-test1.elf',
  'Source Code/bootstrapper/assets/kstuff.elf',
  'Source Code/bootstrapper/assets/ps5debug-NG_v1.3.0.elf',
}
actual_shipped={}
for fp in sorted(ROOT.rglob('*.elf')):
    rel=fp.relative_to(ROOT).as_posix()
    if rel.startswith(TRANSIENT_ELF_PREFIXES) or rel in GENERATED_BOOTSTRAPPER_STAGE_ELFS:
        continue
    actual_shipped[rel]=sha_file(fp)
missing=sorted(set(EXPECTED_ELFS)-set(actual_shipped))
extra=sorted(set(actual_shipped)-set(EXPECTED_ELFS))
changed=sorted(k for k in EXPECTED_ELFS if k in actual_shipped and actual_shipped[k]!=EXPECTED_ELFS[k])
if missing: print('V200_ELF_MISSING='+repr(missing))
if extra: print('V200_ELF_EXTRA='+repr(extra))
if changed: print('V200_ELF_CHANGED='+repr(changed))
ck('V200_ALL_91_ELFS_FROZEN',len(EXPECTED_ELFS)==91 and not missing and not extra and not changed)

ck('V200_VERSION_TOOLBOX','PIZZA HEN v2.00 — Michele Media' in tool)
ck('V200_VERSION_DAEMON','PIZZA HEN v2.00 | Michele Media' in (SRC/'daemon/source/main.cpp').read_text(errors='ignore'))
ck('V200_VERSION_NATIVE','PIZZA HEN v2.00' in hook)

TOTAL=24
print('V2_00_COMPLETE_I18N_HARDWARE_BASELINE={}/{} {}'.format(TOTAL-len(fails),TOTAL,'PASS' if not fails else 'FAIL'))
sys.exit(1 if fails else 0)
