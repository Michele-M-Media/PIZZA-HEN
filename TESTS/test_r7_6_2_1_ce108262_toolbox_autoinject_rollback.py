from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/'Source Code/bootstrapper/assets/toolbox_launcher.html').read_text(errors='ignore')
checks={
 'NO_AUTO_GAME_OPTIONS_ENSURE': "setTimeout(()=>runAction('game-options-ensure')" not in html,
 'GAME_OPTIONS_ACTION_STILL_AVAILABLE': "game-options-ensure" in (ROOT/'Source Code/toolbox_api/src/main.c').read_text(errors='ignore'),
 'R762_ADDCHECKS_GUARD_PRESERVED': "if(!box)return;" in html,
 'R762_SHORTCUT_GUARD_PRESERVED': "if(!host)return;" in html,
 'PLUGIN_SCAN_PRESERVED': "onclick=\"scanPlugins()\"" in html,
 'PAYLOAD_REPO_PRESERVED': "onclick=\"refreshPayloadRepository()\"" in html,
}
for k,v in checks.items(): print(f"{k}={'PASS' if v else 'FAIL'}")
if not all(checks.values()): raise SystemExit(1)
print('R7_6_2_1_CE108262_TOOLBOX_AUTOINJECT_ROLLBACK=PASS')
