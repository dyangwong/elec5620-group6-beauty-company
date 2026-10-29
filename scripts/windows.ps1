[CmdletBinding()]
param(
    [ValidateSet('Setup','Start','Stop','Diagnose','Verify','InstallModel','StartModel','StopModel','RepairModel','SmokeTest')]
    [string]$Action = 'Diagnose',
    [ValidateSet('mock','strata')][string]$Mode = 'mock',
    [ValidateRange(1,65535)][int]$Port = 5620,
    [string]$Database = 'var/company.sqlite3',
    [string]$LlmConfig = 'var/llm.strata.json',
    [switch]$LiveMc,
    [string]$VideoConfig = ''
)
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $repoRoot
try {
    if (-not [IO.Path]::IsPathRooted($LlmConfig)) {
        $LlmConfig = Join-Path $repoRoot $LlmConfig
    }
    $LlmConfig = [IO.Path]::GetFullPath($LlmConfig)
    $runtimeRoot = Join-Path $repoRoot 'var'
    New-Item -ItemType Directory -Force $runtimeRoot | Out-Null
    $pythonPath = Join-Path $repoRoot '.venv/Scripts/python.exe'
    $terminalRoot = Join-Path $runtimeRoot 'strata-terminal'
    $strataPython = Join-Path $terminalRoot 'python/python.exe'
    $strataScript = Join-Path $terminalRoot 'strata.py'
    $feed = 'https://github.com/Niko1221/Strata/releases/download/v0.2.1'
    $stateFile = Join-Path $runtimeRoot "app-$Port.process.json"
    $tempRoot = Join-Path $runtimeRoot 'tmp'
    New-Item -ItemType Directory -Force $tempRoot | Out-Null
    $env:TEMP = $tempRoot
    $env:TMP = $tempRoot
    $env:PYTHONUTF8 = '1'
    foreach ($pair in @{
        STRATA_INSTALL_DIR='strata-install'; STRATA_COMPONENTS_DIR='strata-components';
        STRATA_PROFILE_DIR='strata-profiles'; STRATA_RUNTIME_DIR='strata-runtime';
        STRATA_PRESET_DIR='strata-presets'; STRATA_LAUNCH_PRESET_DIR='strata-launch-presets';
        STRATA_SETTINGS_FILE='strata-settings.json'
    }.GetEnumerator()) { [Environment]::SetEnvironmentVariable($pair.Key, (Join-Path $runtimeRoot $pair.Value), 'Process') }

    function Check-Exit([string]$operation) {
        if ($LASTEXITCODE -ne 0) { throw "$operation failed (exit $LASTEXITCODE). No completion is claimed." }
    }
    function Need-Python {
        if (-not (Test-Path -LiteralPath $pythonPath)) { throw 'Run -Action Setup first.' }
    }
    function Need-Strata {
        if (-not (Test-Path -LiteralPath $strataPython)) { throw 'Run -Action InstallModel first.' }
    }
    function Prepare-ModelRuntime {
        Need-Strata
        & $strataPython (Join-Path $PSScriptRoot 'strata_runtime.py')
        Check-Exit 'Owner-private model runtime preparation'
    }
    function Start-InstalledModel {
        $statusOutput = & $strataPython $strataScript runtime status --profile launch-elec5620-ba --output json
        $runtimeStatus = $statusOutput | ConvertFrom-Json
        if ($runtimeStatus.ok -and $runtimeStatus.state -eq 'ready') {
            Write-Output 'Saved model is already ready; reusing the existing runtime.'
        } elseif ($runtimeStatus.state -in @('stopped','stale')) {
            & $strataPython $strataScript runtime start --profile launch-elec5620-ba --wait 180
            Check-Exit 'Saved model profile start'
        } else {
            throw "Model runtime state is $($runtimeStatus.state). Inspect diagnostics; no second runtime was started."
        }
        $modelList = Invoke-RestMethod 'http://127.0.0.1:8080/v1/models' -TimeoutSec 10
        Write-Output "Model service ready. Copy the exact ID into $LlmConfig :"
        $modelList.data | Select-Object id
    }
    function Get-OwnedProcess {
        if (-not (Test-Path -LiteralPath $stateFile)) { return $null }
        $receipt = Get-Content -Raw -LiteralPath $stateFile | ConvertFrom-Json
        $process = Get-Process -Id $receipt.pid -ErrorAction SilentlyContinue
        if (-not $process) { return $null }
        # An inaccessible or reused PID is not proof that this is our process.
        try {
            $startedAt = $process.StartTime
            $executable = $process.Path
        } catch { return $null }
        if ($startedAt -and $executable -and
            $startedAt.ToUniversalTime().Ticks.ToString() -eq $receipt.startTicks -and
            $executable -eq $receipt.executable) { return $process }
        return $null
    }
    switch ($Action) {
        'Setup' {
            if (-not (Test-Path -LiteralPath $pythonPath)) {
                if (Test-Path -LiteralPath (Join-Path $repoRoot '.venv')) { throw 'Existing incomplete .venv preserved; inspect it manually.' }
                & python -c 'import sys; assert sys.version_info >= (3,9)'
                Check-Exit 'Python check'
                & python -m venv (Join-Path $repoRoot '.venv')
                Check-Exit 'Virtual environment creation'
            }
            & $pythonPath --version
            Check-Exit 'Virtual environment check'
            if (-not (Test-Path -LiteralPath $LlmConfig)) {
                # Exclusive creation: never replace an existing local config.
                $configFull = [IO.Path]::GetFullPath($LlmConfig)
                $stream = [IO.File]::Open($configFull, 'CreateNew', 'Write', 'None')
                try {
                    $bytes = [IO.File]::ReadAllBytes((Join-Path $repoRoot 'config/llm.strata.example.json'))
                    $stream.Write($bytes, 0, $bytes.Length)
                } finally { $stream.Dispose() }
            }
            Write-Output 'App ready: standard library only. Default mock mode needs no model or key.'
        }
        'Start' {
            Need-Python
            if ($LiveMc -and $Mode -ne 'strata') { throw 'LiveMc requires -Mode strata; default mock was preserved.' }
            if (Get-OwnedProcess) { Write-Output "Already running on port $Port; configuration preserved."; break }
            $probe = [Net.Sockets.TcpClient]::new()
            try { $probe.Connect('127.0.0.1', $Port); $busyPort = $true } catch { $busyPort = $false } finally { $probe.Dispose() }
            if ($busyPort) { throw "Port $Port is busy; no existing process was changed." }
            $arguments = @('-m', 'beauty_company', '--port', "$Port", '--db', "`"$Database`"", '--llm-mode', $Mode)
            if ($Mode -eq 'strata') {
                & $pythonPath -c 'import sys; from beauty_company.adapters.llm import LlmConfig; LlmConfig.load(sys.argv[1])' $LlmConfig
                Check-Exit 'Live configuration validation'
                $arguments += @('--llm-config', "`"$LlmConfig`"")
            }
            if ($LiveMc) { $arguments += '--mc-live' }
            if ($VideoConfig) {
                if (-not [IO.Path]::IsPathRooted($VideoConfig)) { $VideoConfig = Join-Path $repoRoot $VideoConfig }
                & $pythonPath -c 'import sys; from beauty_company.adapters.template_video import VideoConfig; VideoConfig.load(sys.argv[1])' $VideoConfig
                Check-Exit 'Video configuration validation'
                $arguments += @('--mc-video-config', "`"$VideoConfig`"")
            }
            $stamp = Get-Date -Format 'yyyyMMdd-HHmmss-ffff'
            $stdout = Join-Path $runtimeRoot "app-$Port-$stamp.out.log"
            $stderr = Join-Path $runtimeRoot "app-$Port-$stamp.err.log"
            $process = Start-Process -FilePath $pythonPath -ArgumentList $arguments -WorkingDirectory $repoRoot -WindowStyle Hidden -PassThru -RedirectStandardOutput $stdout -RedirectStandardError $stderr
            @{pid=$process.Id; startTicks=$process.StartTime.ToUniversalTime().Ticks.ToString(); executable=$pythonPath; mode=$Mode; mcLive=[bool]$LiveMc; templateVideo=[bool]$VideoConfig} |
                ConvertTo-Json | Set-Content -LiteralPath $stateFile -Encoding UTF8
            $healthy = $false
            for ($attempt=0; $attempt -lt 30; $attempt++) {
                if ($process.HasExited) { break }
                try {
                    $health = Invoke-RestMethod "http://127.0.0.1:$Port/api/health" -TimeoutSec 2
                    if ($health.status -eq 'ok') { $healthy = $true; break }
                } catch { Start-Sleep -Milliseconds 200 }
            }
            if (-not $healthy) { throw "App did not become ready. Inspect $stderr" }
            Write-Output "Ready: http://127.0.0.1:$Port | BA $($health.capabilities.ba), MC text $($health.capabilities.mc), media $($health.capabilities.media). Model availability is checked by SmokeTest."
        }
        'Stop' {
            $process = Get-OwnedProcess
            if ($process) { Stop-Process -Id $process.Id; Write-Output "Stopped this script's app on port $Port. Database and config preserved." }
            else { Write-Output 'No matching owned process; nothing stopped.' }
        }
        'Verify' {
            Need-Python
            & $pythonPath -m unittest discover -s tests -v
            Check-Exit 'Offline tests'
            & $pythonPath scripts/check_repository.py
            Check-Exit 'Repository verification'
            if (Get-Command node -ErrorAction SilentlyContinue) { & node --check beauty_company/web/app.js; Check-Exit 'JavaScript syntax' }
        }
        'Diagnose' {
            Write-Output ([Environment]::OSVersion.VersionString)
            $cpuKey = [Microsoft.Win32.Registry]::LocalMachine.OpenSubKey('HARDWARE\DESCRIPTION\System\CentralProcessor\0')
            Write-Output $cpuKey.GetValue('ProcessorNameString')
            Write-Output "Logical processors: $([Environment]::ProcessorCount)"
            & python scripts/hardware_probe.py
            & nvidia-smi --query-gpu=name,memory.total,memory.free,driver_version --format=csv
            Get-PSDrive -PSProvider FileSystem | Select-Object Name,@{n='FreeGiB';e={[math]::Round($_.Free/1GB,2)}} | Format-Table
            & git --version
            & python --version
            & git status --short --branch
            if (Test-Path -LiteralPath $strataPython) { & $strataPython $strataScript --version; & $strataPython $strataScript doctor }
            Write-Output 'Never share local config contents, session cookies, keys or databases with diagnostics.'
        }
        'InstallModel' {
            $archive = Join-Path $runtimeRoot 'strata-control-0.1.46.1-windows-x86_64.zip'
            $expected = 'c2d422081eb72c44cf1b23e7f20c506a2fed371e0e614ead48be7045b7798848'
            if (-not (Test-Path -LiteralPath $terminalRoot)) {
                if (-not (Test-Path -LiteralPath $archive)) { Invoke-WebRequest "$feed/strata-control-0.1.46.1-windows-x86_64.zip" -OutFile $archive -UseBasicParsing }
                if ((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expected) { throw 'Terminal SHA-256 mismatch; file preserved for diagnosis.' }
                Expand-Archive -LiteralPath $archive -DestinationPath $terminalRoot
            }
            Need-Strata
            if ((Get-Content -LiteralPath (Join-Path $terminalRoot 'VERSION') -Raw).Trim() -ne '0.1.46.1') { throw 'Different existing Strata version preserved; reconcile manually.' }
            Prepare-ModelRuntime
            $savedProfile = Join-Path $env:STRATA_PROFILE_DIR 'launch-elec5620-ba.json'
            if (Test-Path -LiteralPath $savedProfile) {
                Write-Output 'Reusing the installed model and saved profile; no configuration or weights are overwritten.'
                Start-InstalledModel
                break
            }
            if ((Get-Item -LiteralPath $runtimeRoot).PSDrive.Free -lt 110GB) {
                throw 'Keep at least 110 GiB free before model preparation. No files were replaced.'
            }
            Write-Output 'Downloads 58.49 GB model plus 0.58 GB engine. Reserve 110 GB. Local only, 8K, int8 KV, one request, no pictures/MTP.'
            & $strataPython $strataScript update --check --feed $feed
            Check-Exit 'Signed feed verification'
            & $strataPython $strataScript launch --family gyro --model gyro-s --context 8k --kv int8 --vision off --mtp off --parallel 1 --access local --port 8080 --data-dir (Join-Path $runtimeRoot 'models') --feed $feed --save-preset elec5620-ba --no-tui --yes
            Check-Exit 'Model installation/start'
            $models = Invoke-RestMethod 'http://127.0.0.1:8080/v1/models' -TimeoutSec 10
            Write-Output "Model service ready. Copy exact ID into $LlmConfig without changing other local settings:"
            $models.data | Select-Object id
        }
        'StartModel' {
            Prepare-ModelRuntime
            Start-InstalledModel
        }
        'StopModel' {
            Prepare-ModelRuntime
            & $strataPython $strataScript runtime stop --profile launch-elec5620-ba
            Check-Exit 'Model stop'
        }
        'RepairModel' {
            Prepare-ModelRuntime
            Write-Output 'Model runtime repaired. Downloaded weights and model choices were preserved; use StartModel next.'
        }
        'SmokeTest' {
            Need-Python
            & $pythonPath scripts/smoke_llm.py --port $Port --expect-mode $Mode
            Check-Exit 'Actual HTTP BA probe'
        }
    }
} finally { Pop-Location }
