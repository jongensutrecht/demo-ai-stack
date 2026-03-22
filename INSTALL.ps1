# Demo AI Stack - Installer
# Gebruik: .\INSTALL.ps1 [-ProjectPath <pad>]

param(
    [string]$ProjectPath = ""
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Demo AI Stack Installer v1.1.0" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$repoRoot = $PSScriptRoot

# 1. Installeer global skills vanuit de canonieke repo-bron
$globalSkillsPath = Join-Path $env:USERPROFILE ".claude\skills"
$skillsRoot = Join-Path $repoRoot "skills"

if (-not (Test-Path $skillsRoot)) {
    Write-Host "[-] Canonieke skills folder niet gevonden: $skillsRoot" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $globalSkillsPath)) {
    Write-Host "[+] Maak global skills folder aan..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $globalSkillsPath -Force | Out-Null
}

$skills = Get-ChildItem -Path $skillsRoot -Directory | Select-Object -ExpandProperty Name
foreach ($skill in $skills) {
    $source = Join-Path $skillsRoot $skill
    $dest = Join-Path $globalSkillsPath $skill
    Write-Host "[+] Installeer skill: $skill" -ForegroundColor Green
    Copy-Item -Recurse -Force $source $dest
}

Write-Host ""
Write-Host "[OK] Global skills geinstalleerd vanuit: $skillsRoot" -ForegroundColor Green
Write-Host "[OK] Doelpad: $globalSkillsPath" -ForegroundColor Green
Write-Host "[OK] Aantal skills: $($skills.Count)" -ForegroundColor Green
Write-Host ""

# 2. Kopieer governance-kit naar project (optioneel)
if ($ProjectPath -ne "") {
    if (-not (Test-Path $ProjectPath)) {
        Write-Host "[-] Project path bestaat niet: $ProjectPath" -ForegroundColor Red
        exit 1
    }

    Write-Host "[+] Kopieer BMAD kit + governance contract naar project..." -ForegroundColor Yellow

    $copyTargets = @(
        @{ Source = "bmad_autopilot_kit"; Destination = "bmad_autopilot_kit" },
        @{ Source = "docs\CTO_RULES.md"; Destination = "docs\CTO_RULES.md" },
        @{ Source = "docs\UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md"; Destination = "docs\UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md" },
        @{ Source = "docs\START_HERE.md"; Destination = "docs\START_HERE.md" },
        @{ Source = "docs\SOURCES_OF_TRUTH.md"; Destination = "docs\SOURCES_OF_TRUTH.md" },
        @{ Source = "docs\FILE_LIMITS_EXCEPTIONS.md"; Destination = "docs\FILE_LIMITS_EXCEPTIONS.md" },
        @{ Source = "SECURITY.md"; Destination = "SECURITY.md" },
        @{ Source = "scripts\validate_cto_rules_registry.py"; Destination = "scripts\validate_cto_rules_registry.py" },
        @{ Source = "scripts\quality_gates.py"; Destination = "scripts\quality_gates.py" },
        @{ Source = "scripts\check_repo_contract.py"; Destination = "scripts\check_repo_contract.py" },
        @{ Source = "scripts\check_repo_10x_contract.py"; Destination = "scripts\check_repo_10x_contract.py" },
        @{ Source = "scripts\check_search_hygiene.py"; Destination = "scripts\check_search_hygiene.py" },
        @{ Source = "scripts\check_file_limits.py"; Destination = "scripts\check_file_limits.py" },
        @{ Source = "config\golden_queries.txt"; Destination = "config\golden_queries.txt" },
        @{ Source = "config\repo_root_allowlist.txt"; Destination = "config\repo_root_allowlist.txt" },
        @{ Source = ".ignore"; Destination = ".ignore" }
    )

    foreach ($target in $copyTargets) {
        $source = Join-Path $repoRoot $target.Source
        $destination = Join-Path $ProjectPath $target.Destination
        $destDir = Split-Path -Parent $destination
        if ($destDir -and -not (Test-Path $destDir)) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }
        Copy-Item -Recurse -Force $source $destination
    }

    Write-Host "[OK] BMAD kit + governance files gekopieerd naar: $ProjectPath" -ForegroundColor Green
} else {
    Write-Host "[INFO] Geen project opgegeven. Handmatige installatiestappen:" -ForegroundColor Yellow
    Write-Host "  Copy-Item -Recurse .\skills\* $env:USERPROFILE\.claude\skills\" -ForegroundColor Gray
    Write-Host "  .\INSTALL.ps1 -ProjectPath <jouw-project>" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Installatie voltooid!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Zie docs/START_HERE.md voor gates en troubleshooting." -ForegroundColor White
