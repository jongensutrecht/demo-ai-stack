<#
.SYNOPSIS
    Invariant Check - Validates that all invariants have NEVER-tests.

.DESCRIPTION
    This script reads invariants.md and checks that each invariant has a
    corresponding NEVER-test file.

.PARAMETER RepoRoot
    The root directory of the repository. Defaults to current directory.

.PARAMETER InvariantsFile
    Path to invariants.md. Defaults to RepoRoot/invariants.md.

.PARAMETER TestsDir
    Directory containing invariant tests. Defaults to RepoRoot/tests/invariants.

.PARAMETER DryRun
    Show what would be checked without actually failing.

.EXAMPLE
    pwsh invariant-check.ps1 -RepoRoot .
    pwsh invariant-check.ps1 -RepoRoot . -InvariantsFile docs/invariants.md
#>

param(
    [string]$RepoRoot = (Get-Location).Path,
    [string]$InvariantsFile = "",
    [string]$TestsDir = "",
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

function Parse-InvariantsFile {
    param([string]$FilePath)

    $content = Get-Content $FilePath -Raw
    $lines = Get-Content $FilePath

    $invariants = @()
    $currentCategory = ""

    foreach ($line in $lines) {
        # Detect category headers
        if ($line -match "^##\s+(Security|Business|Performance|Reliability)\s+Invariants") {
            $currentCategory = $Matches[1]
            continue
        }

        # Parse invariant lines: - [ ] **INV-XXX-NNN**: Description
        # or: - [x] **INV-XXX-NNN**: Description
        if ($line -match "^\s*-\s+\[([ x])\]\s+\*\*([A-Z]+-[A-Z]+-\d{3})\*\*:\s*(.+)") {
            $hasTest = $Matches[1] -eq "x"
            $id = $Matches[2]
            $description = $Matches[3].Trim()

            $invariants += @{
                Id = $id
                Description = $description
                HasTestMarked = $hasTest
                Category = $currentCategory
                TestFile = ""
            }
        }

        # Parse test file line (comes after invariant)
        if ($line -match "^\s+-\s+Test:\s+`(.+)`" -and $invariants.Count -gt 0) {
            $invariants[-1].TestFile = $Matches[1]
        }
    }

    return $invariants
}

function Find-NeverTests {
    param(
        [string]$RepoRoot,
        [string]$TestsDir
    )

    $neverTests = @()

    # Search in tests/invariants/ directory
    if (Test-Path $TestsDir) {
        $files = Get-ChildItem -Path $TestsDir -Recurse -File -Filter "*.py" -ErrorAction SilentlyContinue
        $files += Get-ChildItem -Path $TestsDir -Recurse -File -Filter "*.ts" -ErrorAction SilentlyContinue

        foreach ($file in $files) {
            $relativePath = $file.FullName.Replace($RepoRoot, "").TrimStart("/\")
            $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue

            # Look for NEVER test patterns
            if ($content -match "test_NEVER|NEVER.*test|INVARIANT|INV-[A-Z]+-\d{3}") {
                $neverTests += @{
                    Path = $relativePath
                    FullPath = $file.FullName
                    Content = $content
                }
            }
        }
    }

    # Also search in general test directories
    $generalTestDirs = @("tests", "test", "__tests__")
    foreach ($dir in $generalTestDirs) {
        $testPath = Join-Path $RepoRoot $dir
        if ((Test-Path $testPath) -and $testPath -ne $TestsDir) {
            $files = Get-ChildItem -Path $testPath -Recurse -File -Include "*.py", "*.ts" -ErrorAction SilentlyContinue

            foreach ($file in $files) {
                $relativePath = $file.FullName.Replace($RepoRoot, "").TrimStart("/\")

                # Skip if already processed
                if ($neverTests | Where-Object { $_.Path -eq $relativePath }) {
                    continue
                }

                $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue

                # Look for NEVER test patterns
                if ($content -match "test_NEVER|NEVER.*test|INVARIANT|INV-[A-Z]+-\d{3}") {
                    $neverTests += @{
                        Path = $relativePath
                        FullPath = $file.FullName
                        Content = $content
                    }
                }
            }
        }
    }

    return $neverTests
}

function Test-InvariantHasTest {
    param(
        [hashtable]$Invariant,
        [array]$NeverTests,
        [string]$RepoRoot
    )

    $id = $Invariant.Id
    $expectedTestFile = $Invariant.TestFile

    # Check if the specified test file exists
    if ($expectedTestFile) {
        $fullPath = Join-Path $RepoRoot $expectedTestFile
        if (Test-Path $fullPath) {
            return @{
                HasTest = $true
                TestFile = $expectedTestFile
            }
        }
    }

    # Search for tests that reference this invariant ID
    foreach ($test in $NeverTests) {
        if ($test.Content -match $id) {
            return @{
                HasTest = $true
                TestFile = $test.Path
            }
        }
    }

    # Search for tests with matching NEVER pattern
    $idParts = $id -split "-"
    $category = $idParts[1].ToLower()  # SEC, BIZ, PERF, REL
    $number = $idParts[2]

    foreach ($test in $NeverTests) {
        $testPath = $test.Path.ToLower()
        $testContent = $test.Content.ToLower()

        # Match by path containing category and test content mentioning the invariant
        if ($testPath -match $category -and $testContent -match "never") {
            # Loose match - test exists in relevant category
            return @{
                HasTest = $true
                TestFile = $test.Path
                LooseMatch = $true
            }
        }
    }

    return @{
        HasTest = $false
        TestFile = $null
    }
}

# ============================================================================
# Main Logic
# ============================================================================

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  INVARIANT CHECK - NEVER-Test Coverage  " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Resolve paths
$RepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
if (-not $InvariantsFile) {
    $InvariantsFile = Join-Path $RepoRoot "invariants.md"
}
if (-not $TestsDir) {
    $TestsDir = Join-Path $RepoRoot "tests/invariants"
}

Write-Info "RepoRoot: $RepoRoot"
Write-Info "Invariants: $InvariantsFile"
Write-Info "Tests Dir: $TestsDir"
Write-Host ""

# Check if invariants file exists
if (-not (Test-Path $InvariantsFile)) {
    Write-Warning "invariants.md not found at: $InvariantsFile"
    Write-Warning "Skipping invariant check (no file)"
    Write-Host ""
    Write-Host "To create invariants.md, run: /invariant-discovery"
    exit 0
}

# Parse invariants
$invariants = Parse-InvariantsFile -FilePath $InvariantsFile
Write-Info "Found $($invariants.Count) invariants in file"

if ($invariants.Count -eq 0) {
    Write-Warning "No invariants found in file"
    Write-Warning "Invariants should be in format: - [ ] **INV-XXX-NNN**: Description"
    exit 0
}

# Find all NEVER tests
$neverTests = Find-NeverTests -RepoRoot $RepoRoot -TestsDir $TestsDir
Write-Info "Found $($neverTests.Count) potential NEVER-test files"
Write-Host ""

# Check each invariant
$covered = @()
$uncovered = @()

foreach ($inv in $invariants) {
    $result = Test-InvariantHasTest -Invariant $inv -NeverTests $neverTests -RepoRoot $RepoRoot

    if ($result.HasTest) {
        $covered += @{
            Invariant = $inv
            TestFile = $result.TestFile
            LooseMatch = $result.LooseMatch
        }
        if ($Verbose) {
            Write-Success "$($inv.Id): Covered by $($result.TestFile)"
        }
    }
    else {
        $uncovered += $inv
        if ($Verbose) {
            Write-Warning "$($inv.Id): No NEVER-test found"
        }
    }
}

# Report results
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  RESULTS                                 " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Total invariants: $($invariants.Count)"
Write-Host "Covered: $($covered.Count)"
Write-Host "Uncovered: $($uncovered.Count)"
Write-Host ""

# Group by category
if ($uncovered.Count -gt 0) {
    Write-Host "UNCOVERED INVARIANTS:" -ForegroundColor Red
    Write-Host ""

    $grouped = $uncovered | Group-Object -Property Category

    foreach ($group in $grouped) {
        Write-Host "  $($group.Name):" -ForegroundColor Yellow
        foreach ($inv in $group.Group) {
            Write-Host "    - $($inv.Id): $($inv.Description)" -ForegroundColor Red
            if ($inv.TestFile) {
                Write-Host "      Expected: $($inv.TestFile)" -ForegroundColor Gray
            }
        }
        Write-Host ""
    }
}

if ($covered.Count -gt 0 -and $Verbose) {
    Write-Host "COVERED INVARIANTS:" -ForegroundColor Green
    Write-Host ""

    foreach ($item in $covered) {
        $matchType = if ($item.LooseMatch) { "(loose match)" } else { "" }
        Write-Host "  - $($item.Invariant.Id): $($item.TestFile) $matchType" -ForegroundColor Green
    }
    Write-Host ""
}

# Calculate coverage percentage
$coveragePercent = if ($invariants.Count -gt 0) {
    [math]::Round(($covered.Count / $invariants.Count) * 100, 1)
} else {
    100
}

Write-Host "Coverage: $coveragePercent%" -ForegroundColor $(if ($coveragePercent -ge 80) { "Green" } elseif ($coveragePercent -ge 50) { "Yellow" } else { "Red" })
Write-Host ""

# Determine result
if ($uncovered.Count -gt 0) {
    if ($DryRun) {
        Write-Warning "DRY RUN - Would fail with exit code 1"
        exit 0
    }
    else {
        Write-Error "INVARIANT CHECK FAILED - Uncovered invariants found"
        Write-Host ""
        Write-Host "To fix:"
        Write-Host "  1. Create NEVER-test files for each uncovered invariant"
        Write-Host "  2. Use pattern: test_NEVER_<description>.py"
        Write-Host "  3. Place in: tests/invariants/<category>/"
        Write-Host "  4. Update invariants.md checkbox to [x] when done"
        Write-Host ""
        Write-Host "Example test structure:"
        Write-Host "  tests/invariants/"
        Write-Host "    auth/"
        Write-Host "      test_never_auth_bypass.py"
        Write-Host "    business/"
        Write-Host "      test_never_negative_invoice.py"
        Write-Host ""
        exit 1
    }
}
else {
    Write-Success "INVARIANT CHECK PASSED - All invariants have NEVER-tests"
    exit 0
}
