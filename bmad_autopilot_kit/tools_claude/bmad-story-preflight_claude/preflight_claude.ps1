param(
    [string]$RepoRoot = (Get-Location).Path,
    [string]$Process = "",
    [string]$StoriesDir = "",
    [string]$ProcessFile = "",
    [string]$JsonOutput = "",
    [switch]$AllowDrafted,
    [switch]$WarnOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Try-ResolveGitTopLevel {
    param([string]$Path)
    try {
        $top = (git -C $Path rev-parse --show-toplevel 2>$null).Trim()
        if ($LASTEXITCODE -eq 0 -and $top) { return $top }
    } catch { }
    return $null
}

function Normalize-RepoRoot {
    param([string]$Path)
    $top = Try-ResolveGitTopLevel -Path $Path
    if ($top) { return $top }
    return (Resolve-Path -LiteralPath $Path).Path
}

function Normalize-PathMaybeRelative {
    param([string]$Root, [string]$Path)
    if (-not $Path) { return "" }
    $p = $Path.Trim()
    if (-not $p) { return "" }
    if ([System.IO.Path]::IsPathRooted($p)) { return $p }
    return (Join-Path $Root $p)
}

function Detect-Process {
    param([string]$Root, [string]$ExplicitStoriesDir, [string]$ExplicitProcess)

    if (-not [string]::IsNullOrWhiteSpace($ExplicitProcess)) { return $ExplicitProcess.Trim() }

    if (-not [string]::IsNullOrWhiteSpace($ExplicitStoriesDir)) {
        $sd = Normalize-PathMaybeRelative -Root $Root -Path $ExplicitStoriesDir
        if (Test-Path -LiteralPath $sd) { return (Split-Path -Leaf $sd) }
    }

    $procBase = Join-Path $Root (Join-Path "docs" "processes")
    if (Test-Path -LiteralPath $procBase) {
        $dirs = @(Get-ChildItem -LiteralPath $procBase -Directory -ErrorAction SilentlyContinue)
        if ($dirs.Count -eq 1) { return $dirs[0].Name }
    }

    $storiesBase = Join-Path $Root "stories_claude"
    if (Test-Path -LiteralPath $storiesBase) {
        $dirs = @(Get-ChildItem -LiteralPath $storiesBase -Directory -ErrorAction SilentlyContinue)
        if ($dirs.Count -eq 1) { return $dirs[0].Name }
    }

    return ""
}

function Get-CanonicalOrder {
    param(
        [Parameter(Mandatory = $true)][string]$ProcessFilePath
    )
    if (-not (Test-Path -LiteralPath $ProcessFilePath)) { return @() }

    $lines = Get-Content -LiteralPath $ProcessFilePath
    $startIndex = -1
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match '^## Canonical Story Order \(Sequential Default\)\s*$') {
            $startIndex = $i + 1
            break
        }
    }
    if ($startIndex -lt 0) { return @() }

    $ids = @()
    for ($j = $startIndex; $j -lt $lines.Count; $j++) {
        if ($lines[$j] -match '^##\s+') { break }
        if ($lines[$j] -match '^\s*\d+[.)]\s+([A-Z][A-Z0-9_]*[\.-]\d{3})\b') { $ids += $Matches[1] }
    }
    return $ids
}

function Parse-Verifications {
    param(
        [Parameter(Mandatory = $true)][string]$StoryFilePath,
        [Parameter(Mandatory = $true)][string]$RepoRootPath
    )

    $lines = Get-Content -LiteralPath $StoryFilePath

    $acStart = -1
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match '^##\s+Acceptance Criteria\s*$') { $acStart = $i + 1; break }
    }
    if ($acStart -lt 0) { throw "Acceptance Criteria section not found" }

    $acEnd = $lines.Count
    for ($j = $acStart; $j -lt $lines.Count; $j++) {
        if ($lines[$j] -match '^##\s+') { $acEnd = $j; break }
    }

    $verifications = @()
    $current = $null
    $acCount = 0
    $currentAc = ""
    $currentAcVerificationCount = 0
    $currentAcExpectedCount = 0

    function Flush-CurrentAc {
        if (-not $currentAc) { return }
        if ($null -ne $current) { throw "Missing Expected line after verification" }
        if ($currentAcVerificationCount -eq 0) { throw "No verification commands found" }
        if ($currentAcVerificationCount -gt 1) { throw "Multiple verification commands found" }
        if ($currentAcExpectedCount -gt 1) { throw "Multiple Expected lines found" }
        if ($currentAcExpectedCount -eq 0) { throw "Missing Expected line after verification" }
    }

    for ($k = $acStart; $k -lt $acEnd; $k++) {
        $line = $lines[$k]

        if ($line -match '^\s*-\s+\*\*AC(\d+)\b') {
            Flush-CurrentAc
            $currentAc = ("AC{0}" -f $Matches[1])
            $acCount += 1
            $currentAcVerificationCount = 0
            $currentAcExpectedCount = 0
            $current = $null
            continue
        }
        if (-not $currentAc) { continue }

        if ($line -match '^\s*-\s+\*\*Verification \(repo-root\):\*\*\s+(.+?)\s*$') {
            if ($null -ne $current) { throw "Missing Expected line after verification" }
            if ($currentAcVerificationCount -ge 1) { throw "Multiple verification commands found" }
            $cmd = $Matches[1].Trim()
            if ($cmd.StartsWith('`') -and $cmd.EndsWith('`') -and $cmd.Length -ge 2) { $cmd = $cmd.Substring(1, $cmd.Length - 2) }
            $current = [pscustomobject]@{ Cwd = $RepoRootPath; Command = $cmd; Expected = $null }
            $currentAcVerificationCount += 1
            continue
        }
        if ($line -match '^\s*-\s+Verification \(repo-root\):\s+(.+?)\s*$') {
            if ($null -ne $current) { throw "Missing Expected line after verification" }
            if ($currentAcVerificationCount -ge 1) { throw "Multiple verification commands found" }
            $cmd = $Matches[1].Trim()
            if ($cmd.StartsWith('`') -and $cmd.EndsWith('`') -and $cmd.Length -ge 2) { $cmd = $cmd.Substring(1, $cmd.Length - 2) }
            $current = [pscustomobject]@{ Cwd = $RepoRootPath; Command = $cmd; Expected = $null }
            $currentAcVerificationCount += 1
            continue
        }
        if ($line -match '^\s*-\s+\*\*Verification \(cwd=([^)]+)\):\*\*\s+(.+?)\s*$') {
            if ($null -ne $current) { throw "Missing Expected line after verification" }
            if ($currentAcVerificationCount -ge 1) { throw "Multiple verification commands found" }
            $cwdRaw = $Matches[1].Trim()
            $cwd = if ([System.IO.Path]::IsPathRooted($cwdRaw)) { $cwdRaw } else { Join-Path $RepoRootPath $cwdRaw }
            $cmd = $Matches[2].Trim()
            if ($cmd.StartsWith('`') -and $cmd.EndsWith('`') -and $cmd.Length -ge 2) { $cmd = $cmd.Substring(1, $cmd.Length - 2) }
            $current = [pscustomobject]@{ Cwd = $cwd; Command = $cmd; Expected = $null }
            $currentAcVerificationCount += 1
            continue
        }
        if ($line -match '^\s*-\s+Verification \(cwd=([^)]+)\):\s+(.+?)\s*$') {
            if ($null -ne $current) { throw "Missing Expected line after verification" }
            if ($currentAcVerificationCount -ge 1) { throw "Multiple verification commands found" }
            $cwdRaw = $Matches[1].Trim()
            $cwd = if ([System.IO.Path]::IsPathRooted($cwdRaw)) { $cwdRaw } else { Join-Path $RepoRootPath $cwdRaw }
            $cmd = $Matches[2].Trim()
            if ($cmd.StartsWith('`') -and $cmd.EndsWith('`') -and $cmd.Length -ge 2) { $cmd = $cmd.Substring(1, $cmd.Length - 2) }
            $current = [pscustomobject]@{ Cwd = $cwd; Command = $cmd; Expected = $null }
            $currentAcVerificationCount += 1
            continue
        }
        if ($line -match '^\s*-\s+\*\*Expected:\*\*\s+(.+?)\s*$') {
            if ($null -eq $current) { throw "Expected line without prior verification" }
            if ($currentAcExpectedCount -ge 1) { throw "Multiple Expected lines found" }
            $exp = $Matches[1].Trim()
            if ($exp.StartsWith('`') -and $exp.EndsWith('`') -and $exp.Length -ge 2) { $exp = $exp.Substring(1, $exp.Length - 2) }
            $current.Expected = $exp
            $verifications += $current
            $current = $null
            $currentAcExpectedCount += 1
            continue
        }
        if ($line -match '^\s*-\s+Expected:\s+(.+?)\s*$') {
            if ($null -eq $current) { throw "Expected line without prior verification" }
            if ($currentAcExpectedCount -ge 1) { throw "Multiple Expected lines found" }
            $exp = $Matches[1].Trim()
            if ($exp.StartsWith('`') -and $exp.EndsWith('`') -and $exp.Length -ge 2) { $exp = $exp.Substring(1, $exp.Length - 2) }
            $current.Expected = $exp
            $verifications += $current
            $current = $null
            $currentAcExpectedCount += 1
            continue
        }
    }

    Flush-CurrentAc
    if ($acCount -eq 0) { throw "No AC bullets found in Acceptance Criteria" }
    if ($verifications.Count -eq 0) { throw "No verification commands found" }
    return $verifications
}

function Parse-Allowlist {
    param(
        [Parameter(Mandatory = $true)][string]$StoryFilePath
    )

    $lines = Get-Content -LiteralPath $StoryFilePath
    $startIndex = -1
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match '^###\s+Touched paths allowlist' -or $lines[$i] -match '^##\s+Touched paths allowlist') {
            $startIndex = $i + 1
            break
        }
    }
    if ($startIndex -lt 0) { throw "Touched paths allowlist section not found" }

    $allowlist = @()
    for ($j = $startIndex; $j -lt $lines.Count; $j++) {
        $line = $lines[$j]
        if ($line -match '^##\s+' -or $line -match '^###\s+') { break }
        if ($line.Trim().Length -eq 0) { break }
        if ($line -match '^\s*-\s+(.+)$') {
            $item = $Matches[1].Trim()
            if ($item.StartsWith('`') -and $item.EndsWith('`')) { $item = $item.Trim('`') }
            if ($item) { $allowlist += $item }
        }
    }
    if ($allowlist.Count -eq 0) { throw "Touched paths allowlist is empty" }
    return $allowlist
}

function Parse-Status {
    param(
        [Parameter(Mandatory = $true)][string]$StoryFilePath
    )

    $txt = Get-Content -LiteralPath $StoryFilePath -Raw
    $m = [regex]::Match($txt, '(?ms)^##\s+Status\s*\r?\n(?<body>.*?)(^\#\#\s+|\z)')
    if (-not $m.Success) { return "" }
    $body = $m.Groups['body'].Value
    if ($body -match '(?i)\bready-for-dev\b') { return "ready-for-dev" }
    if ($body -match '(?i)\bdrafted\b') { return "drafted" }
    return ""
}

function Check-RequiredHeadings {
    param(
        [Parameter(Mandatory = $true)][string]$StoryFilePath
    )

    $txt = Get-Content -LiteralPath $StoryFilePath -Raw
    $required = @(
        '^##\s+Context\s*$',
        '^##\s+Story\s*$',
        '^##\s+Acceptance Criteria\s*$',
        '^##\s+Tasks\s*/\s*Subtasks\s*$',
        '^##\s+Dev Notes\s*$',
        '^##\s+Dev Agent Record\s*$',
        '^##\s+Status\s*$'
    )
    $missing = @()
    foreach ($re in $required) {
        if (-not ([regex]::IsMatch($txt, "(?m)$re"))) { $missing += $re }
    }
    return $missing
}

$RepoRoot = if ($PSBoundParameters.ContainsKey('RepoRoot')) {
    (Resolve-Path -LiteralPath $RepoRoot).Path
} else {
    Normalize-RepoRoot -Path $RepoRoot
}
$Process = Detect-Process -Root $RepoRoot -ExplicitStoriesDir $StoriesDir -ExplicitProcess $Process
if (-not $Process) {
    throw "Process not specified and could not be auto-detected. Pass -Process <name> (or -StoriesDir <path>)."
}

$StoriesDir = Normalize-PathMaybeRelative -Root $RepoRoot -Path $StoriesDir
if (-not $StoriesDir) { $StoriesDir = Join-Path $RepoRoot (Join-Path "stories_claude" $Process) }

$ProcessFile = Normalize-PathMaybeRelative -Root $RepoRoot -Path $ProcessFile
if (-not $ProcessFile) { $ProcessFile = Join-Path $RepoRoot (Join-Path "docs" (Join-Path "processes" (Join-Path $Process "PROCESS.md"))) }

if (-not (Test-Path -LiteralPath $StoriesDir)) {
    throw "StoriesDir not found: $StoriesDir"
}

$storyFiles = @(Get-ChildItem -LiteralPath $StoriesDir -File -Filter "*.md" | Sort-Object Name)
if ($storyFiles.Count -eq 0) { throw "No story files found in: $StoriesDir" }

$storyIds = @()
$storyById = @{}
$storyKeyById = @{}
$errors = @()
$warnings = @()

foreach ($f in $storyFiles) {
    if ($f.Name -match '^([A-Z][A-Z0-9_]*[\.-]\d{3})\.md$') {
        $id = $Matches[1]
        if ($storyById.ContainsKey($id)) {
            $errors += "Duplicate story id: $id ($($f.FullName))"
        } else {
            $storyById[$id] = $f.FullName
            $storyIds += $id
            $m = [regex]::Match($id, '^([A-Z][A-Z0-9_]*)([\.-])(\d{3})$')
            if ($m.Success) {
                $storyKeyById[$id] = [pscustomobject]@{ Prefix = $m.Groups[1].Value; Number = [int]$m.Groups[3].Value }
            } else {
                $storyKeyById[$id] = [pscustomobject]@{ Prefix = $id; Number = 0 }
            }
        }
    } else {
        $warnings += "Ignoring non-story markdown file in stories dir: $($f.Name)"
    }
}

if ($storyIds.Count -eq 0) { throw "No story files matching <PREFIX>-<NNN>.md or <PREFIX>.<NNN>.md found in: $StoriesDir" }

$canonical = @(Get-CanonicalOrder -ProcessFilePath $ProcessFile)
if ($canonical.Count -gt 0) {
    foreach ($id in $canonical) {
        if (-not $storyById.ContainsKey($id)) {
            $errors += "PROCESS.md lists $id but file is missing: $StoriesDir\\$id.md"
        }
    }
    foreach ($id in $storyIds) {
        if (-not ($canonical -contains $id)) {
            $warnings += "Story file exists but is not listed in PROCESS.md canonical order: $id"
        }
    }
} else {
    $warnings += "PROCESS.md canonical order not found (ok). Order will be filename/numeric."
}

$results = @()
$orderedIds = if ($canonical.Count -gt 0) { $canonical } else { $storyIds | Sort-Object { $storyKeyById[$_].Prefix }, { $storyKeyById[$_].Number } }
foreach ($id in $orderedIds) {
    if (-not $storyById.ContainsKey($id)) { continue }
    $file = $storyById[$id]
    $rowErrors = @()
    $rowWarnings = @()
    $verCount = 0
    $allowCount = 0
    $status = ""

    try {
        $missingHeadings = @(Check-RequiredHeadings -StoryFilePath $file)
        if ($missingHeadings.Count -gt 0) {
            $rowWarnings += ("Missing required headings (regex): {0}" -f ($missingHeadings -join " | "))
        }
    } catch {
        $rowWarnings += "Heading check failed: $($_.Exception.Message)"
    }

    try {
        $ver = @(Parse-Verifications -StoryFilePath $file -RepoRootPath $RepoRoot)
        $verCount = $ver.Count
    } catch {
        $rowErrors += "Verifications invalid: $($_.Exception.Message)"
    }

    try {
        $allow = @(Parse-Allowlist -StoryFilePath $file)
        $allowCount = $allow.Count
        foreach ($p in $allow) {
            if ([System.IO.Path]::IsPathRooted($p)) {
                $rowWarnings += "Allowlist item is absolute path (should be repo-relative): $p"
            }
        }
    } catch {
        $rowErrors += "Allowlist invalid: $($_.Exception.Message)"
    }

    $status = Parse-Status -StoryFilePath $file
    if (-not $status) {
        $rowWarnings += "Status not found (expected 'ready-for-dev' or 'drafted')"
    } elseif ($status -eq "drafted" -and -not $AllowDrafted.IsPresent) {
        $rowErrors += "Status is drafted (runner will likely fail). Pass -AllowDrafted to only warn."
    }

    $ok = ($rowErrors.Count -eq 0)
    $results += [pscustomobject]@{
        Story = $id
        OK = $ok
        Status = ($status ? $status : "-")
        Verifications = $verCount
        Allowlist = $allowCount
        File = $file
        Errors = $rowErrors.Count
        Warnings = $rowWarnings.Count
    }

    foreach ($e in $rowErrors) { $errors += ("{0}: {1}" -f $id, $e) }
foreach ($w in $rowWarnings) { $warnings += ("{0}: {1}" -f $id, $w) }
}

if (-not [string]::IsNullOrWhiteSpace($JsonOutput)) {
    $jsonPath = Normalize-PathMaybeRelative -Root $RepoRoot -Path $JsonOutput
    $dir = Split-Path -Parent $jsonPath
    if ($dir -and -not (Test-Path -LiteralPath $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }

    $report = [ordered]@{
        repo_root = $RepoRoot
        process = $Process
        results = $results
        warnings = $warnings
        errors = $errors
    }

    ($report | ConvertTo-Json -Depth 50) | Set-Content -LiteralPath $jsonPath -Encoding UTF8
}

Write-Host ("RepoRoot:   {0}" -f $RepoRoot)
Write-Host ("Process:    {0}" -f $Process)
Write-Host ("StoriesDir: {0}" -f $StoriesDir)
Write-Host ("ProcessFile:{0}" -f $ProcessFile)
Write-Host ""

$results | Format-Table -AutoSize Story,OK,Status,Verifications,Allowlist,Errors,Warnings

if ($warnings.Count -gt 0) {
    Write-Host ""
    Write-Host "WARNINGS:"
    foreach ($w in $warnings) { Write-Host ("- {0}" -f $w) }
}

if ($errors.Count -gt 0) {
    Write-Host ""
    Write-Host "ERRORS:"
    foreach ($e in $errors) { Write-Host ("- {0}" -f $e) }
    if (-not $WarnOnly.IsPresent) { exit 2 }
}

exit 0
