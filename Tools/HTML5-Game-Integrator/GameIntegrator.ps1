Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.IO.Compression.FileSystem

[System.Windows.Forms.Application]::EnableVisualStyles()

function Show-Error([string]$Message) {
    [System.Windows.Forms.MessageBox]::Show($Message, 'HTML5 Game Integrator', 'OK', 'Error') | Out-Null
}
function Show-Info([string]$Message) {
    [System.Windows.Forms.MessageBox]::Show($Message, 'HTML5 Game Integrator', 'OK', 'Information') | Out-Null
}
function Copy-Directory([string]$Source, [string]$Destination) {
    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    Get-ChildItem -LiteralPath $Source -Force | ForEach-Object {
        $target = Join-Path $Destination $_.Name
        if ($_.PSIsContainer) { Copy-Directory $_.FullName $target }
        else { Copy-Item -LiteralPath $_.FullName -Destination $target -Force }
    }
}
function Get-Sha256([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function New-Runtime([int]$Fps, [bool]$Gamepad, [bool]$Fullscreen, [bool]$TimerEnabled, [int]$TimerMinutes) {
    $gamepadJs = ''
    if ($Gamepad) {
        $gamepadJs = @'
const MM_KEYS={left:37,up:38,right:39,down:40,enter:13,space:32};
const mmPressed=new Set();
function mmEmit(type,keyCode){
  const keyMap={37:'ArrowLeft',38:'ArrowUp',39:'ArrowRight',40:'ArrowDown',13:'Enter',32:' '};
  const codeMap={37:'ArrowLeft',38:'ArrowUp',39:'ArrowRight',40:'ArrowDown',13:'Enter',32:'Space'};
  let ev;
  try { ev=new KeyboardEvent(type,{key:keyMap[keyCode]||'',code:codeMap[keyCode]||'',bubbles:true,cancelable:true}); }
  catch(_){ ev=document.createEvent('Event'); ev.initEvent(type,true,true); }
  try{Object.defineProperty(ev,'keyCode',{get:()=>keyCode});}catch(_){}
  try{Object.defineProperty(ev,'which',{get:()=>keyCode});}catch(_){}
  window.dispatchEvent(ev); document.dispatchEvent(ev);
}
function mmSet(keyCode,down){
  if(down&&!mmPressed.has(keyCode)){mmPressed.add(keyCode);mmEmit('keydown',keyCode);}
  if(!down&&mmPressed.has(keyCode)){mmPressed.delete(keyCode);mmEmit('keyup',keyCode);}
}
function mmPollPad(){
  const pads=navigator.getGamepads?navigator.getGamepads():[];
  const p=pads&&pads[0]; if(!p)return;
  const ax=p.axes&&p.axes.length>0?p.axes[0]:0;
  const ay=p.axes&&p.axes.length>1?p.axes[1]:0;
  mmSet(MM_KEYS.left,!!((p.buttons[14]&&p.buttons[14].pressed)||ax<-.45));
  mmSet(MM_KEYS.right,!!((p.buttons[15]&&p.buttons[15].pressed)||ax>.45));
  mmSet(MM_KEYS.up,!!((p.buttons[12]&&p.buttons[12].pressed)||ay<-.45));
  mmSet(MM_KEYS.down,!!((p.buttons[13]&&p.buttons[13].pressed)||ay>.45));
  mmSet(MM_KEYS.enter,!!(p.buttons[0]&&p.buttons[0].pressed));
  mmSet(MM_KEYS.space,!!(p.buttons[9]&&p.buttons[9].pressed));
}
setInterval(mmPollPad,16);
'@
    }
    $fullscreenJs = ''
    if ($Fullscreen) {
        $fullscreenJs = @'
const mmStyle=document.createElement('style');
mmStyle.textContent='html,body{margin:0!important;padding:0!important;width:100%!important;height:100%!important;background:#000!important;overflow:hidden!important}canvas{display:block;max-width:100vw!important;max-height:100vh!important;margin:auto!important}';
document.head.appendChild(mmStyle);
'@
    }
    $timerJs = ''
    if ($TimerEnabled) {
        $timerJs = @"
const MM_TIMER_MINUTES=$TimerMinutes;
const mmTimerEnd=Date.now()+(MM_TIMER_MINUTES*60*1000);
const mmTimer=document.createElement('div');
mmTimer.id='mmi-countdown'; mmTimer.setAttribute('aria-live','polite');
mmTimer.style.cssText='position:fixed;top:12px;right:14px;z-index:2147483647;padding:7px 10px;border-radius:8px;background:rgba(0,0,0,.72);color:#fff;font:600 16px/1.2 Segoe UI,Arial,sans-serif;letter-spacing:.5px;pointer-events:none;box-shadow:0 1px 5px rgba(0,0,0,.35)';
document.body.appendChild(mmTimer);
function mmUpdateTimer(){
  const remain=Math.max(0,mmTimerEnd-Date.now());
  const totalSeconds=Math.ceil(remain/1000);
  const mins=Math.floor(totalSeconds/60),secs=totalSeconds%60;
  mmTimer.textContent=String(mins).padStart(2,'0')+':'+String(secs).padStart(2,'0');
  if(remain<=0){mmTimer.textContent='00:00';mmTimer.style.background='rgba(120,0,0,.82)';return;}
  setTimeout(mmUpdateTimer,Math.min(1000,remain));
}
mmUpdateTimer();
"@
    }
    return @"
(function(){
'use strict';
const MM_TARGET_FPS=$Fps;
const MM_FRAME_MS=1000/Math.max(1,MM_TARGET_FPS);
const mmNativeRAF=window.requestAnimationFrame?window.requestAnimationFrame.bind(window):(cb=>setTimeout(()=>cb(performance.now()),16));
const mmNativeCAF=window.cancelAnimationFrame?window.cancelAnimationFrame.bind(window):clearTimeout;
let mmLastFrame=0;
window.requestAnimationFrame=function(cb){
  let handle=0;
  const tick=function(ts){
    if(!mmLastFrame||(ts-mmLastFrame)>=MM_FRAME_MS){mmLastFrame=ts;cb(ts);}else{handle=mmNativeRAF(tick);}
  };
  handle=mmNativeRAF(tick);return handle;
};
window.cancelAnimationFrame=function(id){return mmNativeCAF(id);};
$fullscreenJs
$gamepadJs
$timerJs
})();
"@
}
function New-AddonScript() {
    return @'
(function(){
'use strict';
let overlay=null;
function close(){ if(overlay&&overlay.parentNode)overlay.parentNode.removeChild(overlay); overlay=null; }
function open(url){
  close();
  overlay=document.createElement('div');
  overlay.style.cssText='position:fixed;inset:0;z-index:2147483646;background:#000;';
  const frame=document.createElement('iframe');
  frame.src=url||'game/index.html';
  frame.title='HTML5 Game';
  frame.style.cssText='border:0;width:100%;height:100%;display:block;background:#000;';
  overlay.appendChild(frame);
  document.body.appendChild(overlay);
}
window.MMGameAddon={open:open,close:close};
})();
'@
}

$form=New-Object System.Windows.Forms.Form
$form.Text='HTML5 Game Integrator'
$form.StartPosition='CenterScreen'
$form.Size=New-Object System.Drawing.Size(760,590)
$form.MinimumSize=New-Object System.Drawing.Size(760,590)
$form.BackColor=[System.Drawing.Color]::FromArgb(24,24,24)
$form.ForeColor=[System.Drawing.Color]::White
$form.Font=New-Object System.Drawing.Font('Segoe UI',10)

$title=New-Object System.Windows.Forms.Label
$title.Text='HTML5 GAME INTEGRATOR'
$title.Font=New-Object System.Drawing.Font('Segoe UI Semibold',18)
$title.AutoSize=$true
$title.Location=New-Object System.Drawing.Point(22,18)
$form.Controls.Add($title)

$sub=New-Object System.Windows.Forms.Label
$sub.Text='Bundle an unchanged host script with a lightweight HTML5 game addon.'
$sub.AutoSize=$true
$sub.ForeColor=[System.Drawing.Color]::Silver
$sub.Location=New-Object System.Drawing.Point(25,58)
$form.Controls.Add($sub)

$hostLabel=New-Object System.Windows.Forms.Label
$hostLabel.Text='Host JavaScript (optional - copied byte-for-byte):'
$hostLabel.AutoSize=$true
$hostLabel.Location=New-Object System.Drawing.Point(25,94)
$form.Controls.Add($hostLabel)
$hostBox=New-Object System.Windows.Forms.TextBox
$hostBox.Location=New-Object System.Drawing.Point(28,120)
$hostBox.Size=New-Object System.Drawing.Size(585,28)
$form.Controls.Add($hostBox)
$browseHost=New-Object System.Windows.Forms.Button
$browseHost.Text='Browse'
$browseHost.Location=New-Object System.Drawing.Point(625,118)
$browseHost.Size=New-Object System.Drawing.Size(92,32)
$form.Controls.Add($browseHost)

$sourceLabel=New-Object System.Windows.Forms.Label
$sourceLabel.Text='Game folder / ZIP / index.html:'
$sourceLabel.AutoSize=$true
$sourceLabel.Location=New-Object System.Drawing.Point(25,164)
$form.Controls.Add($sourceLabel)
$sourceBox=New-Object System.Windows.Forms.TextBox
$sourceBox.Location=New-Object System.Drawing.Point(28,190)
$sourceBox.Size=New-Object System.Drawing.Size(585,28)
$form.Controls.Add($sourceBox)
$browseSource=New-Object System.Windows.Forms.Button
$browseSource.Text='Browse'
$browseSource.Location=New-Object System.Drawing.Point(625,188)
$browseSource.Size=New-Object System.Drawing.Size(92,32)
$form.Controls.Add($browseSource)

$outputLabel=New-Object System.Windows.Forms.Label
$outputLabel.Text='Output ZIP:'
$outputLabel.AutoSize=$true
$outputLabel.Location=New-Object System.Drawing.Point(25,234)
$form.Controls.Add($outputLabel)
$outputBox=New-Object System.Windows.Forms.TextBox
$outputBox.Location=New-Object System.Drawing.Point(28,260)
$outputBox.Size=New-Object System.Drawing.Size(585,28)
$form.Controls.Add($outputBox)
$browseOutput=New-Object System.Windows.Forms.Button
$browseOutput.Text='Browse'
$browseOutput.Location=New-Object System.Drawing.Point(625,258)
$browseOutput.Size=New-Object System.Drawing.Size(92,32)
$form.Controls.Add($browseOutput)

$fpsLabel=New-Object System.Windows.Forms.Label
$fpsLabel.Text='Target FPS:'
$fpsLabel.AutoSize=$true
$fpsLabel.Location=New-Object System.Drawing.Point(28,309)
$form.Controls.Add($fpsLabel)
$fps=New-Object System.Windows.Forms.NumericUpDown
$fps.Minimum=10;$fps.Maximum=120;$fps.Value=20
$fps.Location=New-Object System.Drawing.Point(115,306)
$fps.Size=New-Object System.Drawing.Size(75,28)
$form.Controls.Add($fps)
$gamepad=New-Object System.Windows.Forms.CheckBox
$gamepad.Text='Add controller mapping';$gamepad.Checked=$true;$gamepad.AutoSize=$true
$gamepad.Location=New-Object System.Drawing.Point(230,308)
$form.Controls.Add($gamepad)
$fullscreen=New-Object System.Windows.Forms.CheckBox
$fullscreen.Text='Fullscreen-friendly layout';$fullscreen.Checked=$true;$fullscreen.AutoSize=$true
$fullscreen.Location=New-Object System.Drawing.Point(455,308)
$form.Controls.Add($fullscreen)
$timerEnabled=New-Object System.Windows.Forms.CheckBox
$timerEnabled.Text='Add countdown timer';$timerEnabled.Checked=$true;$timerEnabled.AutoSize=$true
$timerEnabled.Location=New-Object System.Drawing.Point(28,350)
$form.Controls.Add($timerEnabled)
$timerLabel=New-Object System.Windows.Forms.Label
$timerLabel.Text='Minutes:';$timerLabel.AutoSize=$true
$timerLabel.Location=New-Object System.Drawing.Point(230,351)
$form.Controls.Add($timerLabel)
$timerMinutes=New-Object System.Windows.Forms.NumericUpDown
$timerMinutes.Minimum=1;$timerMinutes.Maximum=180;$timerMinutes.Value=50
$timerMinutes.Location=New-Object System.Drawing.Point(292,347)
$timerMinutes.Size=New-Object System.Drawing.Size(75,28)
$form.Controls.Add($timerMinutes)

$preserve=New-Object System.Windows.Forms.Label
$preserve.Text='Host script protection: SHA-256 is checked before and after copy. The host file is never edited.'
$preserve.AutoSize=$true
$preserve.ForeColor=[System.Drawing.Color]::LightGreen
$preserve.Location=New-Object System.Drawing.Point(28,392)
$form.Controls.Add($preserve)

$build=New-Object System.Windows.Forms.Button
$build.Text='BUILD HOST + GAME BUNDLE'
$build.Font=New-Object System.Drawing.Font('Segoe UI Semibold',11)
$build.Location=New-Object System.Drawing.Point(28,430)
$build.Size=New-Object System.Drawing.Size(689,46)
$build.BackColor=[System.Drawing.Color]::FromArgb(0,120,215)
$build.ForeColor=[System.Drawing.Color]::White
$build.FlatStyle='Flat'
$form.Controls.Add($build)
$status=New-Object System.Windows.Forms.Label
$status.Text='Ready.';$status.AutoSize=$true;$status.ForeColor=[System.Drawing.Color]::Silver
$status.Location=New-Object System.Drawing.Point(28,492)
$form.Controls.Add($status)

$browseHost.Add_Click({
    $d=New-Object System.Windows.Forms.OpenFileDialog
    $d.Filter='JavaScript files (*.js)|*.js|All files (*.*)|*.*'
    if($d.ShowDialog()-eq 'OK'){$hostBox.Text=$d.FileName}
})
$browseSource.Add_Click({
    $d=New-Object System.Windows.Forms.OpenFileDialog
    $d.Filter='ZIP files (*.zip)|*.zip|HTML files (*.html)|*.html|All files (*.*)|*.*'
    if($d.ShowDialog()-eq 'OK'){
        $sourceBox.Text=$d.FileName
        if([string]::IsNullOrWhiteSpace($outputBox.Text)){
            $base=[System.IO.Path]::GetFileNameWithoutExtension($d.FileName)
            $outputBox.Text=Join-Path ([System.IO.Path]::GetDirectoryName($d.FileName)) ($base+'-host-game-bundle.zip')
        }
    }
})
$sourceBox.Add_DoubleClick({
    $d=New-Object System.Windows.Forms.FolderBrowserDialog
    if($d.ShowDialog()-eq 'OK'){
        $sourceBox.Text=$d.SelectedPath
        if([string]::IsNullOrWhiteSpace($outputBox.Text)){
            $outputBox.Text=Join-Path ([System.IO.Path]::GetDirectoryName($d.SelectedPath)) ((Split-Path $d.SelectedPath -Leaf)+'-host-game-bundle.zip')
        }
    }
})
$browseOutput.Add_Click({
    $d=New-Object System.Windows.Forms.SaveFileDialog
    $d.Filter='ZIP files (*.zip)|*.zip';$d.DefaultExt='zip'
    if($d.ShowDialog()-eq 'OK'){$outputBox.Text=$d.FileName}
})

$build.Add_Click({
    $src=$sourceBox.Text.Trim();$host=$hostBox.Text.Trim();$out=$outputBox.Text.Trim()
    if([string]::IsNullOrWhiteSpace($src)-or -not(Test-Path -LiteralPath $src)){Show-Error 'Select a valid game folder, ZIP, or index.html.';return}
    if(-not [string]::IsNullOrWhiteSpace($host)){
        if(-not(Test-Path -LiteralPath $host)){Show-Error 'Select a valid host JavaScript file or leave it empty.';return}
        if([System.IO.Path]::GetExtension($host).ToLowerInvariant()-ne '.js'){Show-Error 'The optional host file must be a .js file.';return}
    }
    if([string]::IsNullOrWhiteSpace($out)){Show-Error 'Choose an output ZIP.';return}

    $build.Enabled=$false;$status.Text='Building...';$form.Refresh()
    $temp=Join-Path ([System.IO.Path]::GetTempPath()) ('MMGameIntegrator_'+[guid]::NewGuid().ToString('N'))
    try{
        New-Item -ItemType Directory -Force -Path $temp|Out-Null
        $root=Join-Path $temp 'bundle';New-Item -ItemType Directory -Force -Path $root|Out-Null
        $gameRoot=Join-Path $root 'game';New-Item -ItemType Directory -Force -Path $gameRoot|Out-Null

        $srcItem=Get-Item -LiteralPath $src
        if($srcItem.PSIsContainer){Copy-Directory $src $gameRoot}
        elseif([System.IO.Path]::GetExtension($src).ToLowerInvariant()-eq '.zip'){[System.IO.Compression.ZipFile]::ExtractToDirectory($src,$gameRoot)}
        elseif([System.IO.Path]::GetExtension($src).ToLowerInvariant()-in @('.html','.htm')){Copy-Directory ([System.IO.Path]::GetDirectoryName($src)) $gameRoot}
        else{throw 'Input must be a game folder, ZIP, or HTML file.'}

        $index=Get-ChildItem -LiteralPath $gameRoot -Recurse -File|Where-Object{$_.Name -match '^index\.html?$'}|Select-Object -First 1
        if(-not $index){throw 'No index.html found in the selected game.'}
        $runtimePath=Join-Path $index.DirectoryName 'mmi_runtime.js'
        $runtime=New-Runtime -Fps ([int]$fps.Value) -Gamepad $gamepad.Checked -Fullscreen $fullscreen.Checked -TimerEnabled $timerEnabled.Checked -TimerMinutes ([int]$timerMinutes.Value)
        [System.IO.File]::WriteAllText($runtimePath,$runtime,[System.Text.UTF8Encoding]::new($false))
        $html=[System.IO.File]::ReadAllText($index.FullName)
        if($html -notmatch 'mmi_runtime\.js'){
            $tag="`r`n<script src=\"mmi_runtime.js\"></script>`r`n"
            if($html -match '</body>'){$html=$html -replace '</body>',($tag+'</body>')}else{$html+=$tag}
            [System.IO.File]::WriteAllText($index.FullName,$html,[System.Text.UTF8Encoding]::new($false))
        }

        $addonDir=Join-Path $root 'addon';New-Item -ItemType Directory -Force -Path $addonDir|Out-Null
        [System.IO.File]::WriteAllText((Join-Path $addonDir 'mmi_game_addon.js'),(New-AddonScript),[System.Text.UTF8Encoding]::new($false))

        $hostName=$null;$hostHash=$null
        if(-not [string]::IsNullOrWhiteSpace($host)){
            $hostDir=Join-Path $root 'host';New-Item -ItemType Directory -Force -Path $hostDir|Out-Null
            $hostName=[System.IO.Path]::GetFileName($host)
            $hostHash=Get-Sha256 $host
            $hostCopy=Join-Path $hostDir $hostName
            Copy-Item -LiteralPath $host -Destination $hostCopy -Force
            $copyHash=Get-Sha256 $hostCopy
            if($copyHash -ne $hostHash){throw 'Host JavaScript integrity check failed.'}
        }

        $meta=@{
            generatedBy='HTML5 Game Integrator';targetFps=[int]$fps.Value;gamepad=[bool]$gamepad.Checked;fullscreen=[bool]$fullscreen.Checked;
            countdownTimer=[bool]$timerEnabled.Checked;countdownMinutes=[int]$timerMinutes.Value;gameEntry='game/index.html';addon='addon/mmi_game_addon.js';
            hostFile=$hostName;hostSha256=$hostHash;hostModified=$false;generatedAtUtc=[DateTime]::UtcNow.ToString('o')
        }|ConvertTo-Json
        [System.IO.File]::WriteAllText((Join-Path $root 'MM_BUNDLE.json'),$meta,[System.Text.UTF8Encoding]::new($false))
        [System.IO.File]::WriteAllText((Join-Path $root 'HOST_SCRIPT_UNCHANGED.txt'),'The optional host JavaScript is copied byte-for-byte and is not edited by this utility.',[System.Text.UTF8Encoding]::new($false))

        $outDir=[System.IO.Path]::GetDirectoryName($out);if($outDir){New-Item -ItemType Directory -Force -Path $outDir|Out-Null}
        if(Test-Path -LiteralPath $out){Remove-Item -LiteralPath $out -Force}
        [System.IO.Compression.ZipFile]::CreateFromDirectory($root,$out,[System.IO.Compression.CompressionLevel]::Optimal,$false)
        $status.Text='Done: '+$out
        Show-Info "Bundle created successfully.`r`n`r`n$out`r`n`r`nThe optional host JavaScript was preserved unchanged."
    }catch{
        $status.Text='Failed.';Show-Error $_.Exception.Message
    }finally{
        try{if(Test-Path -LiteralPath $temp){Remove-Item -LiteralPath $temp -Recurse -Force}}catch{}
        $build.Enabled=$true
    }
})

[void]$form.ShowDialog()
