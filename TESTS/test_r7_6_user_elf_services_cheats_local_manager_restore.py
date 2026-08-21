#!/usr/bin/env python3
from pathlib import Path
import hashlib,re,sys
R=Path(__file__).resolve().parents[1]
S=R/'Source Code'
def text(p): return (S/p).read_text(errors='replace')
def sha(p): return hashlib.sha256((S/p).read_bytes()).hexdigest()
checks=[]
def ck(name, cond):
    cond=bool(cond); checks.append(cond); print(f'{name}={"PASS" if cond else "FAIL"}')

ui=text('bootstrapper/assets/toolbox_launcher.html')
hook=text('shellui/src/HookFunctions.cpp')
prx=text('shellui/src/prx.cpp')
api=text('toolbox_api/src/main.c')
dmain=text('daemon/source/main.cpp')
emb=text('daemon/source/embeddded_payloads.c')
pm=text('util/source/PluginManager.cpp')

expected={
 'daemon/assets/kstuff-toggle-1.elf':'9009b96f36721a1b4c305735038d70cd72d596c553156bfa2a27e60a68ae2dee',
 'daemon/assets/kstuff-toggle-2.elf':'ae8c39e79f731b5b0515b8487ff7986cf9a626e760881dacc107bd888f3694c6',
 'daemon/assets/kstuff-toggle-3.elf':'0e87e92959791d9edf04c314802fcf18ccf37db74ae353d434a0062557f85093',
 'daemon/assets/fan_target_65c.elf':'0bedeb564947530d09d1dfb27df63c2a09eaa7f51faf3ddcc90b3fb2870e6312',
 'daemon/assets/fan_target_70c.elf':'a9ad8502123799d58f8ddd9882d842f524c4ecc3ea6743a73c6dcdffd0bf30e0',
 'daemon/assets/fan_target_75c.elf':'4b52e09c48ebed1f369221c290e8ec4a9fdb2a477b7b7f44a1b8646958d9f69b',
 'daemon/assets/fan_target_80c.elf':'ccf2e709218f31cd9e6a0705c99646b8f030b877687df8377982a2f6ca10216e',
 'daemon/assets/fan_target_85c.elf':'c37019c351c1c5b05b43adbac29d85bfd25f8c0ab9d94371cacab1945d8e0fd0',
 'daemon/assets/klogsrv-ps5.elf':'e828ec144231f81547cb58bc7d2c396fa984be0c2295f31364b58017816dcceb',
 'daemon/assets/pizza_overlay_phu_original.elf':'8e20deefb9100705be8352dc6acb47241c6a044b93dc3f578f93c424789b2622',
}
for p,h in expected.items(): ck('R76_USER_ELF_'+Path(p).name.replace('.','_').replace('-','_').upper(), sha(p)==h)

# Exact deploy/embedding must survive the rebase.
for name in ['kstuff-toggle-1.elf','kstuff-toggle-2.elf','kstuff-toggle-3.elf','klogsrv-ps5.elf','fan_target_65c.elf','fan_target_70c.elf','fan_target_75c.elf','fan_target_80c.elf','fan_target_85c.elf','pizza_overlay_phu_original.elf']:
    ck('R76_EMBED_'+name.replace('.','_').replace('-','_').upper(), name in emb)
for path in ['/data/PIZZA_HEN/tools/kstuff-toggle-1.elf','/data/PIZZA_HEN/tools/kstuff-toggle-2.elf','/data/PIZZA_HEN/tools/kstuff-toggle-3.elf','/data/PIZZA_HEN/payloads/klogsrv-ps5.elf','/data/PIZZA_HEN/payloads/fan_target_65c.elf','/data/PIZZA_HEN/payloads/fan_target_85c.elf','/data/PIZZA_HEN/payloads/pizza_overlay.elf']:
    ck('R76_DEPLOY_'+path.split('/')[-1].replace('.','_').replace('-','_').upper(), path in dmain)

# KStuff Toggle: exact no-argument original payloads launched through existing websrv /hbldr.
ck('R76_KSTUFF_TOGGLE_THREE_BUTTONS', all(x in ui for x in ['runKstuffToggle(1)','runKstuffToggle(2)','runKstuffToggle(3)']))
ck('R76_KSTUFF_TOGGLE_DIRECT_HBLDR', ("async function launchElfDirect(path)" in ui or "async function launchElfDirect(elfPath)" in ui) and "path:'/data/PIZZA_HEN/tools/kstuff-toggle-'" not in ui and "'/data/PIZZA_HEN/tools/kstuff-toggle-'+mode+'.elf'" in ui)

# Local manager R7.3 controls restored while repository remains.
for label in ['>SCANSIONA<','>AGGIORNA LISTA<','>PLUGIN FOLDER<','>PAYLOAD FOLDER<','>AGGIORNA REPOSITORY<']:
    ck('R76_LOCAL_UI_'+re.sub(r'[^A-Z]+','_',label.upper()).strip('_'), label in ui)
ck('R76_LOCAL_SCAN_INTERNAL_USB', all(x in pm for x in ['/data/PIZZA_HEN/plugins','/data/PIZZA_HEN/payloads','/user/data/PIZZA_HEN/plugins','/mnt/usb%d/PIZZA_HEN/plugins','/usb%d/PIZZA_HEN/payloads']))
ck('R76_LOCAL_START_STOP_AUTOSTART', all(x in ui for x in ["plugin-launch ","plugin-stop ","plugin-autostart "]))
ck('R76_PAYLOAD_MANAGER_COEXISTS', all(x in ui for x in ['payload-repo-refresh','payload-repo-install','Payload Repository']))
ck('R76_LOCAL_FILTER_NO_OBJECT_VALUES', 'Object.values(FAN_TARGET_PATHS)' not in ui and 'isFanTargetPath(it.path)' in ui)

# Fan: source-grounded single-controller lifecycle; stop every variant before starting selected one.
ck('R76_FAN_STOP_ALL_HELPER', 'async function stopAllFanTargets()' in ui and "plugin-stop '+path+' '+fanTargetBaseName(path)+' payload" in ui)
ck('R76_FAN_START_AFTER_STOP_ALL', re.search(r'toggleFanTarget\(on,el\).*?await stopAllFanTargets\(\);if\(on\).*?plugin-launch',ui,re.S) is not None)
ck('R76_FAN_CHANGE_STOPS_OLD', re.search(r'changeFanTarget\(sel\).*?await stopAllFanTargets\(\);await runAction\(\'plugin-launch',ui,re.S) is not None)

# Klog and PHU use the exact supplied binaries with existing lifecycle routes.
ck('R76_KLOG_GENERIC_MANAGER', "KLOGSRV_PATH='/data/PIZZA_HEN/payloads/klogsrv-ps5.elf'" in ui and "plugin-launch '+KLOGSRV_PATH" in ui and "plugin-stop '+KLOGSRV_PATH" in ui)
ck('R76_PHU_EXACT_R74_ROUTE', "PIZZA_OVERLAY_PATH='/data/PIZZA_HEN/payloads/pizza_overlay.elf'" in ui and 'OVERLAY_RUNTIME_LOCK' in ui and "pizza-overlay-stop" in ui)

# Native Cheats: exact old etaHEN/PIZZA source route, but lazy service owns consumers.
ck('R76_CHEAT_OPTION_ROUTE_R79_INTENTIONAL_DELTA', '★ PIZZA HEN Cheats' in hook and 'toolbox-launcher.html?tid=' in hook and 'cheats_uri += "#cheats"' in hook)
for token in ['OnPress_Hook','uri_boot_hook','uri_boot_hook_2','OnPreCreate_Hook','GetManifestResourceStream_Hook']:
    ck('R76_LAZY_CHEAT_HOOK_'+token.upper(), token in prx[prx.find('if (shell_service_requested)'):prx.find('const char *enc_ver')])
ck('R76_DEBUG_SKIPS_LAZY_NATIVE_CHEAT_HOOKS', prx.count('if (!game_options_service_current)') >= 4 and 'native Cheats manifest hook already owned by lazy Shell service' in prx)
ck('R76_NO_POST_KSTUFF_PRELOAD', dmain.count('cmd_ensure_shell_service_runtime();')==1)
ck('R76_CHEATRUNNER_NOT_RUNTIME_DEP', 'CheatRunner' not in ui+hook+prx+dmain+emb+api)

# Every literal runAction command in UI must still have an API handler.
acts=set()
for m in re.finditer(r"runAction\((?:`|'|\")([^`'\"]+)",ui):
    a=m.group(1).split()[0]
    if re.fullmatch(r'[a-z0-9-]+',a): acts.add(a)
handlers=set(re.findall(r'!strcmp\(action,"([^"]+)"\)',api))
ck('R76_ALL_LITERAL_UI_ACTIONS_HAVE_HANDLER', not sorted(acts-handlers))

print('R7_6_USER_ELF_SERVICES_CHEATS_LOCAL_MANAGER_RESTORE='+('PASS' if all(checks) else 'FAIL'))
sys.exit(0 if all(checks) else 1)
