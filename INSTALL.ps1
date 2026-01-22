# Demo AI Stack - Installer
# Gebruik: .\INSTALL.ps1 [-ProjectPath <pad>]

param(
    [string]$ProjectPath = ""
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Demo AI Stack Installer v1.0.0" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Installeer global skills
$globalSkillsPath = Join-Path $env:USERPROFILE ".claude\skills"
$skillsRoot = Join-Path $PSScriptRoot "skills"

if (-not (Test-Path $skillsRoot)) {
    Write-Host "[-] Skills folder niet gevonden: $skillsRoot" -ForegroundColor Red
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

    if (Test-Path $source) {
        Write-Host "[+] Installeer skill: $skill" -ForegroundColor Green
        Copy-Item -Recurse -Force $source $dest
    } else {
        Write-Host "[-] Skill niet gevonden: $skill" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "[OK] Global skills geinstalleerd in: $globalSkillsPath" -ForegroundColor Green
Write-Host "[OK] Aantal skills: $($skills.Count)" -ForegroundColor Green
Write-Host ""

# 2. Kopieer kit naar project (optioneel)
if ($ProjectPath -ne "") {
    if (-not (Test-Path $ProjectPath)) {
        Write-Host "[-] Project path bestaat niet: $ProjectPath" -ForegroundColor Red
        exit 1
    }

    Write-Host "[+] Kopieer BMAD kit naar project..." -ForegroundColor Yellow

    $kitSource = Join-Path $PSScriptRoot "bmad_autopilot_kit"
    $kitDest = Join-Path $ProjectPath "bmad_autopilot_kit"
    Copy-Item -Recurse -Force $kitSource $kitDest

    $docsSource = Join-Path $PSScriptRoot "docs"
    $docsDest = Join-Path $ProjectPath "docs"
    if (-not (Test-Path $docsDest)) {
        New-Item -ItemType Directory -Path $docsDest -Force | Out-Null
    }
    Copy-Item -Force (Join-Path $docsSource "CTO_RULES.md") $docsDest

    Write-Host "[OK] BMAD kit gekopieerd naar: $ProjectPath" -ForegroundColor Green
} else {
    Write-Host "[INFO] Geen project opgegeven. Kopieer handmatig:" -ForegroundColor Yellow
    Write-Host "  Copy-Item -Recurse .\bmad_autopilot_kit\ <jouw-project>\" -ForegroundColor Gray
    Write-Host "  Copy-Item .\docs\CTO_RULES.md <jouw-project>\docs\" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Installatie voltooid!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Beschikbare skills:" -ForegroundColor White
Write-Host "  (Zie ~/.claude/skills voor alle geïnstalleerde skills)" -ForegroundColor Gray
Write-Host ""
