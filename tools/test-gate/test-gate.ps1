<#
.SYNOPSIS
    Test Gate - Validates that required tests exist for changed files.

.DESCRIPTION
    This script reads test-requirements.yaml and checks that all required
    test types exist for files that have been changed (based on git diff).

.PARAMETER RepoRoot
    The root directory of the repository. Defaults to current directory.

.PARAMETER ConfigFile
    Path to test-requirements.yaml. Defaults to RepoRoot/test-requirements.yaml.

.PARAMETER DiffBase
    Git ref to compare against. Defaults to HEAD~1.

.PARAMETER JsonOutput
    Write JSON report to file.

.PARAMETER DryRun
    Show what would be checked without actually failing.

.EXAMPLE
    pwsh test-gate.ps1 -RepoRoot .
    pwsh test-gate.ps1 -RepoRoot . -DiffBase main
#>

param(
    [string]$RepoRoot = (Get-Location).Path,
    [string]$ConfigFile = "",
    [string]$DiffBase = "HEAD~1",
    [string]$JsonOutput = "",
    [switch]$DryRun,
    [switch]$Verbose
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ============================================================================
# Helper Functions
# ============================================================================

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Get-GitChangedFiles {
    param([string]$Base)

    try {
        $files = git diff --name-only $Base 2>$null
        if ($LASTEXITCODE -ne 0) {
            # Fallback: check staged files
            $files = git diff --name-only --staged 2>$null
        }
        if (-not $files) {
            # Fallback: check all tracked files
            $files = git ls-files 2>$null
        }
        return $files | Where-Object { $_ -and $_.Trim() }
    }
    catch {
        Write-Warning "Could not get git diff, checking all files"
        return @()
    }
}

function Test-PathMatchesPattern {
    param(
        [string]$Path,
        [string]$Pattern
    )

    # Convert glob pattern to regex
    $regex = $Pattern -replace '\*\*', '<<<DOUBLESTAR>>>'
    $regex = $regex -replace '\*', '[^/]*'
    $regex = $regex -replace '<<<DOUBLESTAR>>>', '.*'
    $regex = "^$regex$"

    return $Path -match $regex
}

function Find-TestFiles {
    param(
        [string]$RepoRoot,
        [string]$TestType,
        [hashtable]$TestPatterns
    )

    $patterns = $TestPatterns[$TestType]
    if (-not $patterns) {
        return @()
    }

    $testFiles = @()
    foreach ($pattern in $patterns) {
        $found = Get-ChildItem -Path $RepoRoot -Recurse -File -ErrorAction SilentlyContinue |
            Where-Object {
                $relativePath = $_.FullName.Replace($RepoRoot, "").TrimStart("/\")
                Test-PathMatchesPattern -Path $relativePath -Pattern $pattern
            }
        $testFiles += $found
    }

    return $testFiles | Select-Object -Unique
}

function Get-RequiredTestsForFile {
    param(
        [string]$FilePath,
        [array]$Rules
    )

    foreach ($rule in $Rules) {
        $pattern = $rule.pattern
        if (Test-PathMatchesPattern -Path $FilePath -Pattern $pattern) {
            return $rule.required
        }
    }

    return @()
}

function Test-FileHasTestOfType {
    param(
        [string]$SourceFile,
        [string]$TestType,
        [string]$RepoRoot,
        [hashtable]$TestPatterns
    )

    # Get base name without extension
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($SourceFile)

    # Find all test files of this type
    $testFiles = Find-TestFiles -RepoRoot $RepoRoot -TestType $TestType -TestPatterns $TestPatterns

    # Check if any test file relates to this source file
    foreach ($testFile in $testFiles) {
        $testName = $testFile.Name.ToLower()
        $baseNameLower = $baseName.ToLower()

        # Various naming conventions
        if ($testName -match $baseNameLower) {
            return $true
        }
        # test_button.py for Button.tsx
        if ($testName -match "test_$baseNameLower") {
            return $true
        }
        # button_test.py for Button.tsx
        if ($testName -match "${baseNameLower}_test") {
            return $true
        }
        # button.test.ts for Button.tsx
        if ($testName -match "${baseNameLower}\.test") {
            return $true
        }
        # button.spec.ts for Button.tsx
        if ($testName -match "${baseNameLower}\.spec") {
            return $true
        }
    }

    return $false
}

# ============================================================================
# Main Logic
# ============================================================================

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  TEST GATE - Required Tests Checker     " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Resolve paths
$RepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
if (-not $ConfigFile) {
    $ConfigFile = Join-Path $RepoRoot "test-requirements.yaml"
}

Write-Info "RepoRoot: $RepoRoot"
Write-Info "Config: $ConfigFile"
Write-Info "Diff base: $DiffBase"
Write-Host ""

# Check if config exists
if (-not (Test-Path $ConfigFile)) {
    Write-Error "test-requirements.yaml not found at: $ConfigFile"
    Write-Host "FAIL-CLOSED: test gate vereist een config. Maak test-requirements.yaml aan."
    if ($JsonOutput) {
        $jsonPath = (Resolve-Path -LiteralPath $JsonOutput -ErrorAction SilentlyContinue)
        if (-not $jsonPath) {
            $jsonPath = $JsonOutput
        } else {
            $jsonPath = $jsonPath.Path
        }
        $dir = Split-Path -Parent $jsonPath
        if ($dir -and -not (Test-Path -LiteralPath $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
        $report = [ordered]@{
            tool = "test-gate"
            repo_root = $RepoRoot
            config = $ConfigFile
            error = "missing_config"
            exit_code = 2
        }
        ($report | ConvertTo-Json -Depth 10) | Set-Content -LiteralPath $jsonPath -Encoding UTF8
    }
    exit 2
}

# Parse YAML config (simple parser)
$configContent = Get-Content $ConfigFile -Raw

# Extract test patterns
$testPatterns = @{
    "unit" = @()
    "integration" = @()
    "playwright" = @()
    "e2e" = @()
    "contract" = @()
}

# Simple YAML parsing for test_patterns section
$inTestPatterns = $false
$currentType = ""
foreach ($line in $configContent -split "`n") {
    if ($line -match "^test_patterns:") {
        $inTestPatterns = $true
        continue
    }
    if ($inTestPatterns -and $line -match "^[a-z]") {
        $inTestPatterns = $false
    }
    if ($inTestPatterns) {
        if ($line -match "^\s+(\w+):") {
            $currentType = $Matches[1]
        }
        elseif ($line -match '^\s+-\s+"(.+)"' -and $currentType) {
            $testPatterns[$currentType] += $Matches[1]
        }
        elseif ($line -match "^\s+-\s+'(.+)'" -and $currentType) {
            $testPatterns[$currentType] += $Matches[1]
        }
    }
}

# Extract rules
$rules = @()
$inRules = $false
$currentRule = $null
foreach ($line in $configContent -split "`n") {
    if ($line -match "^rules:") {
        $inRules = $true
        continue
    }
    if ($inRules -and $line -match "^[a-z]" -and $line -notmatch "^\s") {
        $inRules = $false
    }
    if ($inRules) {
        if ($line -match '^\s+-\s+pattern:\s+"(.+)"') {
            if ($currentRule) {
                $rules += $currentRule
            }
            $currentRule = @{
                pattern = $Matches[1]
                required = @()
            }
        }
        elseif ($line -match "^\s+-\s+pattern:\s+'(.+)'") {
            if ($currentRule) {
                $rules += $currentRule
            }
            $currentRule = @{
                pattern = $Matches[1]
                required = @()
            }
        }
        elseif ($line -match "^\s+required:\s+\[(.+)\]" -and $currentRule) {
            $reqList = $Matches[1] -split "," | ForEach-Object { $_.Trim() }
            $currentRule.required = $reqList
        }
    }
}
if ($currentRule) {
    $rules += $currentRule
}

# Extract exclusions
$exclusions = @()
$inExclusions = $false
foreach ($line in $configContent -split "`n") {
    if ($line -match "^exclusions:") {
        $inExclusions = $true
        continue
    }
    if ($inExclusions -and $line -match "^[a-z]" -and $line -notmatch "^\s") {
        $inExclusions = $false
    }
    if ($inExclusions) {
        if ($line -match '^\s+-\s+"(.+)"') {
            $exclusions += $Matches[1]
        }
        elseif ($line -match "^\s+-\s+'(.+)'") {
            $exclusions += $Matches[1]
        }
    }
}

Write-Info "Loaded $($rules.Count) rules from config"
Write-Info "Loaded $($exclusions.Count) exclusion patterns"
Write-Host ""

# Get changed files
$changedFiles = Get-GitChangedFiles -Base $DiffBase
Write-Info "Found $($changedFiles.Count) changed files"
Write-Host ""

# Check each changed file
$violations = @()
$checked = 0
$skipped = 0

foreach ($file in $changedFiles) {
    # Skip if matches exclusion pattern
    $isExcluded = $false
    foreach ($exclusion in $exclusions) {
        if (Test-PathMatchesPattern -Path $file -Pattern $exclusion) {
            $isExcluded = $true
            break
        }
    }
    if ($isExcluded) {
        if ($Verbose) {
            Write-Info "Skipped (excluded): $file"
        }
        $skipped++
        continue
    }

    # Skip test files themselves
    $isTestFile = $false
    foreach ($type in $testPatterns.Keys) {
        foreach ($pattern in $testPatterns[$type]) {
            if (Test-PathMatchesPattern -Path $file -Pattern $pattern) {
                $isTestFile = $true
                break
            }
        }
        if ($isTestFile) { break }
    }
    if ($isTestFile) {
        if ($Verbose) {
            Write-Info "Skipped (test file): $file"
        }
        $skipped++
        continue
    }

    # Get required tests for this file
    $requiredTests = Get-RequiredTestsForFile -FilePath $file -Rules $rules
    if ($requiredTests.Count -eq 0) {
        if ($Verbose) {
            Write-Info "Skipped (no rules match): $file"
        }
        $skipped++
        continue
    }

    $checked++

    # Check each required test type
    foreach ($testType in $requiredTests) {
        $hasTest = Test-FileHasTestOfType -SourceFile $file -TestType $testType -RepoRoot $RepoRoot -TestPatterns $testPatterns

        if (-not $hasTest) {
            $violations += @{
                File = $file
                MissingTestType = $testType
            }
        }
    }
}

# Report results
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  RESULTS                                 " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Files checked: $checked"
Write-Host "Files skipped: $skipped"
Write-Host "Violations found: $($violations.Count)"
Write-Host ""

if ($violations.Count -gt 0) {
    Write-Host "MISSING TESTS:" -ForegroundColor Red
    Write-Host ""

    $violations | Group-Object -Property File | ForEach-Object {
        $file = $_.Name
        $missing = ($_.Group | ForEach-Object { $_.MissingTestType }) -join ", "
        Write-Host "  $file" -ForegroundColor Yellow
        Write-Host "    Missing: $missing" -ForegroundColor Red
    }

    Write-Host ""

    if ($DryRun) {
        Write-Warning "DRY RUN - Would fail with exit code 1"
        $exitCode = 0
    }
    else {
        Write-Error "TEST GATE FAILED - Required tests are missing"
        Write-Host ""
        Write-Host "To fix:"
        Write-Host "  1. Create the missing test files"
        Write-Host "  2. Follow naming convention: <source>_test.py or <source>.test.ts"
        Write-Host "  3. Re-run test-gate"
        Write-Host ""
        $exitCode = 1
    }
}
else {
    Write-Success "TEST GATE PASSED - All required tests present"
    $exitCode = 0
}

if ($JsonOutput) {
    $jsonPath = (Resolve-Path -LiteralPath $JsonOutput -ErrorAction SilentlyContinue)
    if (-not $jsonPath) {
        $jsonPath = $JsonOutput
    } else {
        $jsonPath = $jsonPath.Path
    }
    $dir = Split-Path -Parent $jsonPath
    if ($dir -and -not (Test-Path -LiteralPath $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }

    $report = [ordered]@{
        tool = "test-gate"
        repo_root = $RepoRoot
        config = $ConfigFile
        diff_base = $DiffBase
        changed_files = $changedFiles
        rules_count = $rules.Count
        exclusions_count = $exclusions.Count
        files_checked = $checked
        files_skipped = $skipped
        violations = $violations
        exit_code = $exitCode
        dry_run = [bool]$DryRun
    }

    ($report | ConvertTo-Json -Depth 50) | Set-Content -LiteralPath $jsonPath -Encoding UTF8
}

exit $exitCode
