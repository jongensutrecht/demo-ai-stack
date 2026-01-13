$ErrorActionPreference = "Stop"

$root = $PSScriptRoot
$preflight = Join-Path $root "preflight_claude.ps1"
$fixtures = Join-Path $root "fixtures_claude"
$proc = "demo_proc"

function Run-Ok([string]$name) {
    $repo = Join-Path $fixtures $name
    $out = pwsh -NoProfile -File $preflight -RepoRoot $repo -Process $proc 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw ("Fixture '{0}' expected OK but failed:`n{1}" -f $name, ($out | Out-String))
    }
}

function Run-Bad([string]$name, [string]$mustMatch) {
    $repo = Join-Path $fixtures $name
    $out = pwsh -NoProfile -File $preflight -RepoRoot $repo -Process $proc 2>&1
    if ($LASTEXITCODE -eq 0) { throw ("Fixture '{0}' expected non-zero exit" -f $name) }
    if (($out | Out-String) -notmatch $mustMatch) {
        throw ("Fixture '{0}' expected output to match '{1}' but got:`n{2}" -f $name, $mustMatch, ($out | Out-String))
    }
}

Run-Ok -name "ok_hyphen"
Run-Ok -name "ok_dot"

$tmp = Join-Path $env:TEMP ("preflight_selfcheck_" + [Guid]::NewGuid() + ".json")
$out = pwsh -NoProfile -File $preflight -RepoRoot (Join-Path $fixtures "ok_hyphen") -Process $proc -JsonOutput $tmp 2>&1
if ($LASTEXITCODE -ne 0) { throw ("JsonOutput run failed:`n{0}" -f ($out | Out-String)) }
$j = Get-Content -Raw $tmp | ConvertFrom-Json
foreach ($k in @("repo_root", "process", "results")) {
    if (-not ($j.PSObject.Properties.Name -contains $k)) { throw ("Missing JSON key: {0}" -f $k) }
}
Remove-Item -Force $tmp

Run-Bad -name "bad_missing_expected" -mustMatch "Missing Expected"

$out = pwsh -NoProfile -File $preflight -RepoRoot (Join-Path $fixtures "ambiguous_process") 2>&1
if ($LASTEXITCODE -eq 0) { throw "Fixture 'ambiguous_process' expected non-zero exit" }
if (($out | Out-String) -notmatch "could not be auto-detected") {
    throw ("Fixture 'ambiguous_process' expected fail-closed message but got:`n{0}" -f ($out | Out-String))
}

Write-Host "SELF-CHECK OK"

