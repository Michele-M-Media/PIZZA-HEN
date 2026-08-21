from pathlib import Path
import re, hashlib
ROOT=Path(__file__).resolve().parents[1]
ui=(ROOT/'Source Code/bootstrapper/assets/toolbox_launcher.html').read_text(errors='ignore')
expected={
 'system':'ee8372b83c7caa8fafa2f8b0f202a27678051a2898fcea13ad7a8707fe442de6',
 'rest':'60817e522777ae0b690851709d381f272f76a32830919221ca3a3b84be7fb6c8',
 'shortcuts':'a0d32948782140e2398df31a238c694e78a79abdc57d834b1bb78b26da177bad',
 'advanced':'de76e19dc00257afef195ddfc52e9de5dd796fd70faf575ffcd260a7d4168793',
 'store':'cc40154b81c94b8ca3388b628ed077d3ceff47a0e6be28fd16416e425cc5cbbd',
 'webman':'7605d21254ea30fc4ec3be63df141fb6f7ebc70d91a80516c17fb9e0d28fe6e1',
}

def ck(name,cond):
 print(f'{name}={"PASS" if cond else "FAIL"}')
 if not cond: raise SystemExit(1)
for sid,sha in expected.items():
 m=re.search(rf'<section id="{sid}" class="panel">.*?</section>',ui,re.S)
 ck('R763_R72_PANEL_'+sid.upper()+'_EXACT', bool(m) and hashlib.sha256(m.group(0).encode()).hexdigest()==sha)
# Hidden exactly like Game Manager: panel preserved, but no visible etaItem menu entry.
for label in ['System Options','Rest Mode Options','Extras / Firmware Backends','Controller Shortcuts','PS5 webMAN Games','Homebrew Store']:
 ck('R763_HIDDEN_MENU_'+label.upper().replace(' ','_').replace('/','_'), f'<span class="etaItemTitle">{label}</span>' not in ui)
for host in ['systemChecks','restChecks','shortcutControls','advancedResult','storeStatus']:
 ck('R763_INTERNAL_HOST_'+host.upper(), f'id="{host}"' in ui)
ck('R763_GAME_MANAGER_HIDDEN_PATTERN_PRESERVED','<section id="games" class="panel"><h2>Game Manager</h2>' in ui and '<span class="etaItemTitle">Game Manager</span>' not in ui)
ck('R763_NO_TOOLBOX_AUTO_GAME_OPTIONS_INJECTION',"setTimeout(()=>runAction('game-options-ensure')" not in ui)
ck('R763_JS_GUARDS_RETAINED',"function addChecks(id,defs){const box=document.getElementById(id);if(!box)return;" in ui and "function shortcut(id,title,subtitle,options){const host=document.getElementById('shortcutControls');if(!host)return;" in ui)
ck('R763_CURRENT_PLUGIN_SCAN_PRESERVED',"async function scanPlugins()" in ui and "await runAction('plugin-scan')" in ui)
ck('R763_PAYLOAD_MANAGER_PRESERVED','payload-repo-refresh' in ui and 'payload-repo-install' in ui)
print('R7_6_3_HIDDEN_LEGACY_TOOLBOX_HOSTS_RESTORE=PASS')
