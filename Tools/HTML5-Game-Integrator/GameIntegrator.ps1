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
        if ($_.PSIsContainer) {
            Copy-Directory $_.FullName $target
        } else {
            Copy-Item -LiteralPath $_.FullName -Destination $target -Force
        }
    }
}

function New-Runtime([int]$Fps, [bool]$Gamepad, [bool]$Fullscreen) {
    $gamepadJs = ''
    if ($Gamepad) {
        $gamepadJs = @'
const MM_KEYS = {
  left: 37, up: 38, right: 39, down: 40,
  enter: 13, space: 32
};
const mmPressed = new Set();
function mmEmit(type, keyCode) {
  const keyMap = {37:'ArrowLeft',38:'ArrowUp',39:'ArrowRight',40:'ArrowDown',13:'Enter',32:' '};
  const codeMap = {37:'ArrowLeft',38:'ArrowUp',39:'ArrowRight',40:'ArrowDown',13:'Enter',32:'Space'};
  const ev = new KeyboardEvent(type, {key:keyMap[keyCode]||'', code:codeMap[keyCode]||'', bubbles:true, cancelable:true});
  try { Object.defineProperty(ev, 'keyCode', { get: () => keyCode }); } catch (_) {}
  try { Object.defineProperty(ev, 'which', { get: () => keyCode }); } catch (_) {}
  window.dispatchEvent(ev);
  document.dispatchEvent(ev);
}
function mmSet(keyCode, down) {
  if (down && !mmPressed.has(keyCode)) { mmPressed.add(keyCode); mmEmit('keydown', keyCode); }
  if (!down && mmPressed.has(keyCode)) { mmPressed.delete(keyCode); mmEmit('keyup', keyCode); }
}
function mmPollPad() {
  const pads = navigator.getGamepads ? navigator.getGamepads() : [];
  const p = pads && pads[0];
  if (!p) return;
  const ax = p.axes && p.axes.length > 0 ? p.axes[0] : 0;
  const ay = p.axes && p.axes.length > 1 ? p.axes[1] : 0;
  mmSet(MM_KEYS.left,  !!((p.buttons[14] && p.buttons[14].pressed) || ax < -0.45));
  mmSet(MM_KEYS.right, !!((p.buttons[15] && p.buttons[15].pressed) || ax >  0.45));
  mmSet(MM_KEYS.up,    !!((p.buttons[12] && p.buttons[12].pressed) || ay < -0.45));
  mmSet(MM_KEYS.down,  !!((p.buttons[13] && p.buttons[13].pressed) || ay >  0.45));
  mmSet(MM_KEYS.enter, !!(p.buttons[0] && p.buttons[0].pressed));
  mmSet(MM_KEYS.space, !!(p.buttons[9] && p.buttons[9].pressed));
}
setInterval(mmPollPad, 16);
'@
    }

    $fullscreenJs = ''
    if ($Fullscreen) {
        $fullscreenJs = @'
const mmStyle = document.createElement('style');
mmStyle.textContent = `
html,body{margin:0!important;padding:0!important;width:100%!important;height:100%!important;background:#000!important;overflow:hidden!important;}
canvas{display:block;max-width:100vw!important;max-height:100vh!important;margin:auto!important;}
`;
document.head.appendChild(mmStyle);
'@
    }

    return @"
(function(){
'use strict';
const MM_TARGET_FPS = $Fps;
const MM_FRAME_MS = 1000 / Math.max(1, MM_TARGET_FPS);
const mmNativeRAF = window.requestAnimationFrame ? window.requestAnimationFrame.bind(window) : (cb => setTimeout(() => cb(performance.now()), 16));
const mmNativeCAF = window.cancelAnimationFrame ? window.cancelAnimationFrame.bind(window) : clearTimeout;
let mmLastFrame = 0;
window.requestAnimationFrame = function(cb){
  let handle = 0;
  const tick = function(ts){
    if (!mmLastFrame || (ts - mmLastFrame) >= MM_FRAME_MS) {
      mmLastFrame = ts;
      cb(ts);
    } else {
      handle = mmNativeRAF(tick);
    }
  };
  handle = mmNativeRAF(tick);
  return handle;
};
window.cancelAnimationFrame = function(id){ return mmNativeCAF(id); };
$fullscreenJs
$gamepadJs
})();
"@
}

$form = New-Object System.Windows.Forms.Form
$form.Text = 'HTML5 Game Integrator'
$form.StartPosition = 'CenterScreen'
$form.Size = New-Object System.Drawing.Size(720, 420)
$form.MinimumSize = New-Object System.Drawing.Size(720, 420)
$form.BackColor = [System.Drawing.Color]::FromArgb(24,24,24)
$form.ForeColor = [System.Drawing.Color]::White
$form.Font = New-Object System.Drawing.Font('Segoe UI', 10)

$title = New-Object System.Windows.Forms.Label
$title.Text = 'HTML5 GAME INTEGRATOR'
$title.Font = New-Object System.Drawing.Font('Segoe UI Semibold', 18)
$title.AutoSize = $true
$title.Location = New-Object System.Drawing.Point(22, 18)
$form.Controls.Add($title)

$sub = New-Object System.Windows.Forms.Label
$sub.Text = 'Prepare a lightweight game package with FPS cap + controller support.'
$sub.AutoSize = $true
$sub.ForeColor = [System.Drawing.Color]::Silver
$sub.Location = New-Object System.Drawing.Point(25, 58)
$form.Controls.Add($sub)

$sourceLabel = New-Object System.Windows.Forms.Label
$sourceLabel.Text = 'Game folder or ZIP:'
$sourceLabel.AutoSize = $true
$sourceLabel.Location = New-Object System.Drawing.Point(25, 100)
$form.Controls.Add($sourceLabel)

$sourceBox = New-Object System.Windows.Forms.TextBox
$sourceBox.Location = New-Object System.Drawing.Point(28, 126)
$sourceBox.Size = New-Object System.Drawing.Size(550, 28)
$form.Controls.Add($sourceBox)

$browseSource = New-Object System.Windows.Forms.Button
$browseSource.Text = 'Browse'
$browseSource.Location = New-Object System.Drawing.Point(590, 124)
$browseSource.Size = New-Object System.Drawing.Size(92, 32)
$form.Controls.Add($browseSource)

$outputLabel = New-Object System.Windows.Forms.Label
$outputLabel.Text = 'Output ZIP:'
$outputLabel.AutoSize = $true
$outputLabel.Location = New-Object System.Drawing.Point(25, 170)
$form.Controls.Add($outputLabel)

$outputBox = New-Object System.Windows.Forms.TextBox
$outputBox.Location = New-Object System.Drawing.Point(28, 196)
$outputBox.Size = New-Object System.Drawing.Size(550, 28)
$form.Controls.Add($outputBox)

$browseOutput = New-Object System.Windows.Forms.Button
$browseOutput.Text = 'Browse'
$browseOutput.Location = New-Object System.Drawing.Point(590, 194)
$browseOutput.Size = New-Object System.Drawing.Size(92, 32)
$form.Controls.Add($browseOutput)

$fpsLabel = New-Object System.Windows.Forms.Label
$fpsLabel.Text = 'Target FPS:'
$fpsLabel.AutoSize = $true
$fpsLabel.Location = New-Object System.Drawing.Point(28, 245)
$form.Controls.Add($fpsLabel)

$fps = New-Object System.Windows.Forms.NumericUpDown
$fps.Minimum = 10
$fps.Maximum = 120
$fps.Value = 20
$fps.Location = New-Object System.Drawing.Point(115, 242)
$fps.Size = New-Object System.Drawing.Size(75, 28)
$form.Controls.Add($fps)

$gamepad = New-Object System.Windows.Forms.CheckBox
$gamepad.Text = 'Add controller mapping'
$gamepad.Checked = $true
$gamepad.AutoSize = $true
$gamepad.Location = New-Object System.Drawing.Point(230, 244)
$form.Controls.Add($gamepad)

$fullscreen = New-Object System.Windows.Forms.CheckBox
$fullscreen.Text = 'Fullscreen-friendly layout'
$fullscreen.Checked = $true
$fullscreen.AutoSize = $true
$fullscreen.Location = New-Object System.Drawing.Point(430, 244)
$form.Controls.Add($fullscreen)

$build = New-Object System.Windows.Forms.Button
$build.Text = 'BUILD GAME PACKAGE'
$build.Font = New-Object System.Drawing.Font('Segoe UI Semibold', 11)
$build.Location = New-Object System.Drawing.Point(28, 300)
$build.Size = New-Object System.Drawing.Size(654, 46)
$build.BackColor = [System.Drawing.Color]::FromArgb(0,120,215)
$build.ForeColor = [System.Drawing.Color]::White
$build.FlatStyle = 'Flat'
$form.Controls.Add($build)

$status = New-Object System.Windows.Forms.Label
$status.Text = 'Ready.'
$status.AutoSize = $true
$status.ForeColor = [System.Drawing.Color]::Silver
$status.Location = New-Object System.Drawing.Point(28, 356)
$form.Controls.Add($status)

$browseSource.Add_Click({
    $dialog = New-Object System.Windows.Forms.OpenFileDialog
    $dialog.Filter = 'ZIP files (*.zip)|*.zip|HTML files (*.html)|*.html|All files (*.*)|*.*'
    if ($dialog.ShowDialog() -eq 'OK') {
        $sourceBox.Text = $dialog.FileName
        if ([string]::IsNullOrWhiteSpace($outputBox.Text)) {
            $base = [System.IO.Path]::GetFileNameWithoutExtension($dialog.FileName)
            $outputBox.Text = Join-Path ([System.IO.Path]::GetDirectoryName($dialog.FileName)) ($base + '-20fps-gamepad.zip')
        }
    }
})

$sourceBox.Add_DoubleClick({
    $folder = New-Object System.Windows.Forms.FolderBrowserDialog
    if ($folder.ShowDialog() -eq 'OK') {
        $sourceBox.Text = $folder.SelectedPath
        if ([string]::IsNullOrWhiteSpace($outputBox.Text)) {
            $outputBox.Text = Join-Path ([System.IO.Path]::GetDirectoryName($folder.SelectedPath)) ((Split-Path $folder.SelectedPath -Leaf) + '-20fps-gamepad.zip')
        }
    }
})

$browseOutput.Add_Click({
    $dialog = New-Object System.Windows.Forms.SaveFileDialog
    $dialog.Filter = 'ZIP files (*.zip)|*.zip'
    $dialog.DefaultExt = 'zip'
    if ($dialog.ShowDialog() -eq 'OK') { $outputBox.Text = $dialog.FileName }
})

$build.Add_Click({
    $src = $sourceBox.Text.Trim()
    $out = $outputBox.Text.Trim()
    if ([string]::IsNullOrWhiteSpace($src) -or -not (Test-Path -LiteralPath $src)) { Show-Error 'Select a valid game folder, ZIP, or index.html.'; return }
    if ([string]::IsNullOrWhiteSpace($out)) { Show-Error 'Choose an output ZIP.'; return }

    $build.Enabled = $false
    $status.Text = 'Building...'
    $form.Refresh()

    $temp = Join-Path ([System.IO.Path]::GetTempPath()) ('MMGameIntegrator_' + [guid]::NewGuid().ToString('N'))
    try {
        New-Item -ItemType Directory -Force -Path $temp | Out-Null
        $work = Join-Path $temp 'game'
        New-Item -ItemType Directory -Force -Path $work | Out-Null

        if ((Get-Item -LiteralPath $src).PSIsContainer) {
            Copy-Directory $src $work
        } elseif ([System.IO.Path]::GetExtension($src).ToLowerInvariant() -eq '.zip') {
            [System.IO.Compression.ZipFile]::ExtractToDirectory($src, $work)
        } elseif ([System.IO.Path]::GetExtension($src).ToLowerInvariant() -in @('.html','.htm')) {
            Copy-Directory ([System.IO.Path]::GetDirectoryName($src)) $work
        } else {
            throw 'Input must be a game folder, ZIP, or HTML file.'
        }

        $index = Get-ChildItem -LiteralPath $work -Recurse -File | Where-Object { $_.Name -match '^index\.html?$' } | Select-Object -First 1
        if (-not $index) { throw 'No index.html found in the selected game.' }

        $runtimePath = Join-Path $index.DirectoryName 'mmi_runtime.js'
        $runtime = New-Runtime -Fps ([int]$fps.Value) -Gamepad $gamepad.Checked -Fullscreen $fullscreen.Checked
        [System.IO.File]::WriteAllText($runtimePath, $runtime, [System.Text.UTF8Encoding]::new($false))

        $html = [System.IO.File]::ReadAllText($index.FullName)
        if ($html -notmatch 'mmi_runtime\.js') {
            $tag = "`r`n<script src=\"mmi_runtime.js\"></script>`r`n"
            if ($html -match '</body>') { $html = $html -replace '</body>', ($tag + '</body>') }
            else { $html += $tag }
            [System.IO.File]::WriteAllText($index.FullName, $html, [System.Text.UTF8Encoding]::new($false))
        }

        $meta = @{
            generatedBy = 'HTML5 Game Integrator'
            targetFps = [int]$fps.Value
            gamepad = [bool]$gamepad.Checked
            fullscreen = [bool]$fullscreen.Checked
            generatedAtUtc = [DateTime]::UtcNow.ToString('o')
        } | ConvertTo-Json
        [System.IO.File]::WriteAllText((Join-Path $work 'MM_GAME_PACKAGE.json'), $meta, [System.Text.UTF8Encoding]::new($false))

        $outDir = [System.IO.Path]::GetDirectoryName($out)
        if ($outDir) { New-Item -ItemType Directory -Force -Path $outDir | Out-Null }
        if (Test-Path -LiteralPath $out) { Remove-Item -LiteralPath $out -Force }
        [System.IO.Compression.ZipFile]::CreateFromDirectory($work, $out, [System.IO.Compression.CompressionLevel]::Optimal, $false)

        $status.Text = 'Done: ' + $out
        Show-Info "Game package created successfully.`r`n`r`n$out"
    } catch {
        $status.Text = 'Failed.'
        Show-Error $_.Exception.Message
    } finally {
        try { if (Test-Path -LiteralPath $temp) { Remove-Item -LiteralPath $temp -Recurse -Force } } catch {}
        $build.Enabled = $true
    }
})

[void]$form.ShowDialog()
