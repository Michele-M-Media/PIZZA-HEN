Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

[System.Windows.Forms.Application]::EnableVisualStyles()

function Show-Error([string]$Message) {
    [System.Windows.Forms.MessageBox]::Show($Message, 'GameJS Builder', 'OK', 'Error') | Out-Null
}

function Show-Info([string]$Message) {
    [System.Windows.Forms.MessageBox]::Show($Message, 'GameJS Builder', 'OK', 'Information') | Out-Null
}

function New-GameJs([string]$HtmlBase64, [int]$Fps, [bool]$Gamepad, [bool]$Fullscreen, [bool]$TimerEnabled, [int]$TimerMinutes, [bool]$AutoStart) {
    $gamepadJs = ''
    if ($Gamepad) {
        $gamepadJs = @'
const MM_KEYS={left:37,up:38,right:39,down:40,enter:13,space:32};
const mmPressed=new Set();
function mmEmit(type,keyCode){
  const keyMap={37:'ArrowLeft',38:'ArrowUp',39:'ArrowRight',40:'ArrowDown',13:'Enter',32:' '};
  const codeMap={37:'ArrowLeft',38:'ArrowUp',39:'ArrowRight',40:'ArrowDown',13:'Enter',32:'Space'};
  const ev=new KeyboardEvent(type,{key:keyMap[keyCode]||'',code:codeMap[keyCode]||'',bubbles:true,cancelable:true});
  try{Object.defineProperty(ev,'keyCode',{get:()=>keyCode});}catch(_){ }
  try{Object.defineProperty(ev,'which',{get:()=>keyCode});}catch(_){ }
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
  mmSet(MM_KEYS.left,!!((p.buttons[14]&&p.buttons[14].pressed)||ax<-0.45));
  mmSet(MM_KEYS.right,!!((p.buttons[15]&&p.buttons[15].pressed)||ax>0.45));
  mmSet(MM_KEYS.up,!!((p.buttons[12]&&p.buttons[12].pressed)||ay<-0.45));
  mmSet(MM_KEYS.down,!!((p.buttons[13]&&p.buttons[13].pressed)||ay>0.45));
  mmSet(MM_KEYS.enter,!!(p.buttons[0]&&p.buttons[0].pressed));
  mmSet(MM_KEYS.space,!!(p.buttons[9]&&p.buttons[9].pressed));
}
setInterval(mmPollPad,16);
'@
    }

    $fullscreenCss = ''
    if ($Fullscreen) {
        $fullscreenCss = 'html,body{margin:0!important;padding:0!important;width:100%!important;height:100%!important;background:#000!important;overflow:hidden!important;}canvas{display:block;max-width:100vw!important;max-height:100vh!important;margin:auto!important;}'
    }

    $timerFlag = if ($TimerEnabled) { 'true' } else { 'false' }
    $autoFlag = if ($AutoStart) { 'true' } else { 'false' }

    return @"
(function(){
'use strict';
if(window.MMGame)return;

const MM_HTML_B64='$HtmlBase64';
const MM_TARGET_FPS=$Fps;
const MM_TIMER_ENABLED=$timerFlag;
const MM_TIMER_MINUTES=$TimerMinutes;
const MM_AUTOSTART=$autoFlag;
let mmRoot=null,mmFrame=null,mmTimer=null,mmTimerHandle=null,mmEnd=0;

function mmDecodeHtml(){
  const raw=atob(MM_HTML_B64);
  const bytes=new Uint8Array(raw.length);
  for(let i=0;i<raw.length;i++)bytes[i]=raw.charCodeAt(i);
  if(typeof TextDecoder!=='undefined')return new TextDecoder('utf-8').decode(bytes);
  let s=''; for(let i=0;i<bytes.length;i++)s+=String.fromCharCode(bytes[i]);
  try{return decodeURIComponent(escape(s));}catch(_){return s;}
}

function mmRuntimePrefix(){
  const js=`(function(){\n'use strict';\nconst MM_TARGET_FPS=${MM_TARGET_FPS};\nconst MM_FRAME_MS=1000/Math.max(1,MM_TARGET_FPS);\nconst mmNativeRAF=window.requestAnimationFrame?window.requestAnimationFrame.bind(window):(cb=>setTimeout(()=>cb(performance.now()),16));\nconst mmNativeCAF=window.cancelAnimationFrame?window.cancelAnimationFrame.bind(window):clearTimeout;\nlet mmLastFrame=0;\nwindow.requestAnimationFrame=function(cb){let handle=0;const tick=function(ts){if(!mmLastFrame||(ts-mmLastFrame)>=MM_FRAME_MS){mmLastFrame=ts;cb(ts);}else{handle=mmNativeRAF(tick);}};handle=mmNativeRAF(tick);return handle;};\nwindow.cancelAnimationFrame=function(id){return mmNativeCAF(id);};\nconst mmStyle=document.createElement('style');mmStyle.textContent=${JSON.stringify('$fullscreenCss')};document.head.appendChild(mmStyle);\n$gamepadJs\n})();`;
  return '<script>'+js.replace(/<\\/script/gi,'<\\/script')+'<\\/script>';
}

function mmUpdateTimer(){
  if(!mmTimer)return;
  const remain=Math.max(0,mmEnd-Date.now());
  const total=Math.ceil(remain/1000),mins=Math.floor(total/60),secs=total%60;
  mmTimer.textContent=String(mins).padStart(2,'0')+':'+String(secs).padStart(2,'0');
  if(remain<=0){mmTimer.textContent='00:00';mmTimer.style.background='rgba(120,0,0,.86)';return;}
  mmTimerHandle=setTimeout(mmUpdateTimer,Math.min(1000,remain));
}

function start(){
  if(mmRoot)return;
  mmRoot=document.createElement('div');
  mmRoot.id='mm-game-root';
  mmRoot.style.cssText='position:fixed;inset:0;z-index:2147483000;background:#000;overflow:hidden;';
  mmFrame=document.createElement('iframe');
  mmFrame.id='mm-game-frame';
  mmFrame.setAttribute('allow','fullscreen; gamepad');
  mmFrame.style.cssText='border:0;width:100%;height:100%;display:block;background:#000;';
  mmRoot.appendChild(mmFrame);
  document.body.appendChild(mmRoot);
  if(MM_TIMER_ENABLED){
    mmTimer=document.createElement('div');
    mmTimer.id='mm-game-timer';
    mmTimer.style.cssText='position:fixed;top:12px;right:14px;z-index:2147483647;padding:7px 10px;border-radius:8px;background:rgba(0,0,0,.72);color:#fff;font:600 16px/1.2 Segoe UI,Arial,sans-serif;letter-spacing:.5px;pointer-events:none;box-shadow:0 1px 5px rgba(0,0,0,.35)';
    document.body.appendChild(mmTimer);
    mmEnd=Date.now()+(MM_TIMER_MINUTES*60*1000);
    mmUpdateTimer();
  }
  mmFrame.srcdoc=mmRuntimePrefix()+mmDecodeHtml();
}

function stop(){
  if(mmTimerHandle){clearTimeout(mmTimerHandle);mmTimerHandle=null;}
  if(mmTimer&&mmTimer.parentNode)mmTimer.parentNode.removeChild(mmTimer);
  if(mmRoot&&mmRoot.parentNode)mmRoot.parentNode.removeChild(mmRoot);
  mmRoot=null;mmFrame=null;mmTimer=null;
}

function hide(){if(mmRoot)mmRoot.style.display='none';if(mmTimer)mmTimer.style.display='none';}
function show(){if(mmRoot)mmRoot.style.display='block';if(mmTimer)mmTimer.style.display='block';}

window.MMGame={start,stop,hide,show,isRunning:()=>!!mmRoot};
if(MM_AUTOSTART){
  const boot=()=>{try{start();}catch(e){console.error('[MMGame]',e);}};
  if(document.body)boot();else window.addEventListener('DOMContentLoaded',boot,{once:true});
}
})();
"@
}

$form = New-Object System.Windows.Forms.Form
$form.Text = 'GameJS Builder'
$form.StartPosition = 'CenterScreen'
$form.Size = New-Object System.Drawing.Size(760, 500)
$form.MinimumSize = New-Object System.Drawing.Size(760, 500)
$form.BackColor = [System.Drawing.Color]::FromArgb(24,24,24)
$form.ForeColor = [System.Drawing.Color]::White
$form.Font = New-Object System.Drawing.Font('Segoe UI', 10)

$title = New-Object System.Windows.Forms.Label
$title.Text = 'GAME.JS BUILDER'
$title.Font = New-Object System.Drawing.Font('Segoe UI Semibold', 18)
$title.AutoSize = $true
$title.Location = New-Object System.Drawing.Point(22, 18)
$form.Controls.Add($title)

$sub = New-Object System.Windows.Forms.Label
$sub.Text = 'Convert a self-contained HTML5 game into one standalone game.js overlay.'
$sub.AutoSize = $true
$sub.ForeColor = [System.Drawing.Color]::Silver
$sub.Location = New-Object System.Drawing.Point(25, 58)
$form.Controls.Add($sub)

$sourceLabel = New-Object System.Windows.Forms.Label
$sourceLabel.Text = 'Self-contained HTML game:'
$sourceLabel.AutoSize = $true
$sourceLabel.Location = New-Object System.Drawing.Point(25, 100)
$form.Controls.Add($sourceLabel)

$sourceBox = New-Object System.Windows.Forms.TextBox
$sourceBox.Location = New-Object System.Drawing.Point(28, 126)
$sourceBox.Size = New-Object System.Drawing.Size(580, 28)
$form.Controls.Add($sourceBox)

$browseSource = New-Object System.Windows.Forms.Button
$browseSource.Text = 'Browse'
$browseSource.Location = New-Object System.Drawing.Point(620, 124)
$browseSource.Size = New-Object System.Drawing.Size(100, 32)
$form.Controls.Add($browseSource)

$outputLabel = New-Object System.Windows.Forms.Label
$outputLabel.Text = 'Output game.js:'
$outputLabel.AutoSize = $true
$outputLabel.Location = New-Object System.Drawing.Point(25, 170)
$form.Controls.Add($outputLabel)

$outputBox = New-Object System.Windows.Forms.TextBox
$outputBox.Location = New-Object System.Drawing.Point(28, 196)
$outputBox.Size = New-Object System.Drawing.Size(580, 28)
$form.Controls.Add($outputBox)

$browseOutput = New-Object System.Windows.Forms.Button
$browseOutput.Text = 'Browse'
$browseOutput.Location = New-Object System.Drawing.Point(620, 194)
$browseOutput.Size = New-Object System.Drawing.Size(100, 32)
$form.Controls.Add($browseOutput)

$fpsLabel = New-Object System.Windows.Forms.Label
$fpsLabel.Text = 'Target FPS:'
$fpsLabel.AutoSize = $true
$fpsLabel.Location = New-Object System.Drawing.Point(28, 246)
$form.Controls.Add($fpsLabel)

$fps = New-Object System.Windows.Forms.NumericUpDown
$fps.Minimum = 10
$fps.Maximum = 120
$fps.Value = 20
$fps.Location = New-Object System.Drawing.Point(115, 242)
$fps.Size = New-Object System.Drawing.Size(75, 28)
$form.Controls.Add($fps)

$gamepad = New-Object System.Windows.Forms.CheckBox
$gamepad.Text = 'Controller mapping'
$gamepad.Checked = $true
$gamepad.AutoSize = $true
$gamepad.Location = New-Object System.Drawing.Point(225, 244)
$form.Controls.Add($gamepad)

$fullscreen = New-Object System.Windows.Forms.CheckBox
$fullscreen.Text = 'Fullscreen overlay'
$fullscreen.Checked = $true
$fullscreen.AutoSize = $true
$fullscreen.Location = New-Object System.Drawing.Point(405, 244)
$form.Controls.Add($fullscreen)

$autostart = New-Object System.Windows.Forms.CheckBox
$autostart.Text = 'Start automatically when game.js is loaded'
$autostart.Checked = $true
$autostart.AutoSize = $true
$autostart.Location = New-Object System.Drawing.Point(28, 286)
$form.Controls.Add($autostart)

$timerEnabled = New-Object System.Windows.Forms.CheckBox
$timerEnabled.Text = 'Countdown timer'
$timerEnabled.Checked = $true
$timerEnabled.AutoSize = $true
$timerEnabled.Location = New-Object System.Drawing.Point(28, 322)
$form.Controls.Add($timerEnabled)

$timerLabel = New-Object System.Windows.Forms.Label
$timerLabel.Text = 'Minutes:'
$timerLabel.AutoSize = $true
$timerLabel.Location = New-Object System.Drawing.Point(190, 323)
$form.Controls.Add($timerLabel)

$timerMinutes = New-Object System.Windows.Forms.NumericUpDown
$timerMinutes.Minimum = 1
$timerMinutes.Maximum = 180
$timerMinutes.Value = 50
$timerMinutes.Location = New-Object System.Drawing.Point(252, 319)
$timerMinutes.Size = New-Object System.Drawing.Size(75, 28)
$form.Controls.Add($timerMinutes)

$build = New-Object System.Windows.Forms.Button
$build.Text = 'BUILD GAME.JS'
$build.Font = New-Object System.Drawing.Font('Segoe UI Semibold', 11)
$build.Location = New-Object System.Drawing.Point(28, 370)
$build.Size = New-Object System.Drawing.Size(692, 46)
$build.BackColor = [System.Drawing.Color]::FromArgb(0,120,215)
$build.ForeColor = [System.Drawing.Color]::White
$build.FlatStyle = 'Flat'
$form.Controls.Add($build)

$status = New-Object System.Windows.Forms.Label
$status.Text = 'Ready.'
$status.AutoSize = $true
$status.ForeColor = [System.Drawing.Color]::Silver
$status.Location = New-Object System.Drawing.Point(28, 430)
$form.Controls.Add($status)

$browseSource.Add_Click({
    $dialog = New-Object System.Windows.Forms.OpenFileDialog
    $dialog.Filter = 'HTML files (*.html;*.htm)|*.html;*.htm|All files (*.*)|*.*'
    if ($dialog.ShowDialog() -eq 'OK') {
        $sourceBox.Text = $dialog.FileName
        if ([string]::IsNullOrWhiteSpace($outputBox.Text)) {
            $outputBox.Text = Join-Path ([System.IO.Path]::GetDirectoryName($dialog.FileName)) 'game.js'
        }
    }
})

$browseOutput.Add_Click({
    $dialog = New-Object System.Windows.Forms.SaveFileDialog
    $dialog.Filter = 'JavaScript files (*.js)|*.js'
    $dialog.DefaultExt = 'js'
    $dialog.FileName = 'game.js'
    if ($dialog.ShowDialog() -eq 'OK') { $outputBox.Text = $dialog.FileName }
})

$build.Add_Click({
    $src = $sourceBox.Text.Trim()
    $out = $outputBox.Text.Trim()
    if ([string]::IsNullOrWhiteSpace($src) -or -not (Test-Path -LiteralPath $src)) { Show-Error 'Select a valid self-contained HTML file.'; return }
    if ([System.IO.Path]::GetExtension($src).ToLowerInvariant() -notin @('.html','.htm')) { Show-Error 'Input must be an HTML file.'; return }
    if ([string]::IsNullOrWhiteSpace($out)) { Show-Error 'Choose the output game.js file.'; return }

    try {
        $build.Enabled = $false
        $status.Text = 'Building game.js...'
        $form.Refresh()

        $html = [System.IO.File]::ReadAllText($src)
        $htmlBytes = [System.Text.Encoding]::UTF8.GetBytes($html)
        $htmlBase64 = [Convert]::ToBase64String($htmlBytes)
        $js = New-GameJs -HtmlBase64 $htmlBase64 -Fps ([int]$fps.Value) -Gamepad $gamepad.Checked -Fullscreen $fullscreen.Checked -TimerEnabled $timerEnabled.Checked -TimerMinutes ([int]$timerMinutes.Value) -AutoStart $autostart.Checked

        $outDir = [System.IO.Path]::GetDirectoryName($out)
        if ($outDir -and -not (Test-Path -LiteralPath $outDir)) { New-Item -ItemType Directory -Force -Path $outDir | Out-Null }
        [System.IO.File]::WriteAllText($out, $js, [System.Text.UTF8Encoding]::new($false))

        $status.Text = 'Done: game.js created.'
        Show-Info ("Created:`r`n" + $out + "`r`n`r`nThe source HTML was not modified.")
    } catch {
        $status.Text = 'Build failed.'
        Show-Error $_.Exception.Message
    } finally {
        $build.Enabled = $true
    }
})

[void]$form.ShowDialog()
