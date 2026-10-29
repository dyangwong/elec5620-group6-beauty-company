[CmdletBinding()]
param(
    [ValidateSet('Setup','Diagnose')][string]$Action = 'Diagnose',
    [string]$Config = 'var/media.template.json'
)
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
if (-not [IO.Path]::IsPathRooted($Config)) { $Config = Join-Path $repoRoot $Config }
$Config = [IO.Path]::GetFullPath($Config)
$toolRoot = Join-Path $repoRoot 'var/media-tools'
$installRoot = Join-Path $toolRoot 'ffmpeg-9.0.2-essentials_build'
$archive = Join-Path $toolRoot 'ffmpeg-9.0.2-essentials_build.zip'
$expected = '60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba'
if ($Action -eq 'Setup') {
    if (Test-Path -LiteralPath $Config) {
        Write-Output "Existing video configuration preserved: $Config"
        return
    }
    New-Item -ItemType Directory -Force -Path $toolRoot | Out-Null
    if (-not (Test-Path -LiteralPath $archive)) {
        Invoke-WebRequest 'https://github.com/GyanD/codexffmpeg/releases/download/9.0.2/ffmpeg-9.0.2-essentials_build.zip' -OutFile $archive -UseBasicParsing
    }
    if ((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expected) {
        throw 'FFmpeg archive hash mismatch; file preserved. Inspect manually; nothing was installed.'
    }
    if (-not (Test-Path -LiteralPath $installRoot)) {
        Expand-Archive -LiteralPath $archive -DestinationPath $toolRoot
    }
    foreach ($exe in @('ffmpeg.exe','ffprobe.exe')) {
        if (-not (Test-Path -LiteralPath (Join-Path $installRoot "bin/$exe"))) {
            throw 'Existing incomplete tool directory preserved; inspect it manually.'
        }
    }
    $font = Join-Path $env:WINDIR 'Fonts/arial.ttf'
    if (-not (Test-Path -LiteralPath $font)) { throw 'Arial font missing; provide an explicit licensed local font in a local config.' }
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Config) | Out-Null
    $value = @{ffmpeg=(Join-Path $installRoot 'bin/ffmpeg.exe'); ffprobe=(Join-Path $installRoot 'bin/ffprobe.exe'); font=$font; output_dir='mc-media'; timeout_seconds=120} | ConvertTo-Json
    $stream = [IO.File]::Open($Config, 'CreateNew', 'Write', 'None')
    try { $bytes=[Text.Encoding]::UTF8.GetBytes($value); $stream.Write($bytes,0,$bytes.Length) } finally { $stream.Dispose() }
    Write-Output "Optional CPU renderer configured: $Config. No PATH/model/database changes. Binaries and outputs stay local."
} else {
    if (-not (Test-Path -LiteralPath $Config)) { throw 'No video configuration. Run this script with -Action Setup only if template MP4 is wanted.' }
    $value = Get-Content -Raw -LiteralPath $Config | ConvertFrom-Json
    foreach ($field in @('ffmpeg','ffprobe')) {
        $exe = $value.$field
        if (-not [IO.Path]::IsPathRooted($exe)) { $exe = Join-Path (Split-Path -Parent $Config) $exe }
        if (-not (Test-Path -LiteralPath $exe)) { throw "$field is missing. Existing configuration was preserved." }
        $versionLines = & $exe -version
        $versionExit = $LASTEXITCODE
        $versionLines | Select-Object -First 1
        if ($versionExit -ne 0) { throw "$field diagnostic failed." }
    }
    Write-Output 'Version output is not a successful render. Validate a current draft, its saved file/hash and playback separately.'
}
