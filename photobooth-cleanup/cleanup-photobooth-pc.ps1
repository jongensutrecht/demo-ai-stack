# ================================================================
# WINDOWS 11 AGGRESSIVE BLOATWARE REMOVAL - PHOTOBOOTH PC
# ================================================================
# Doel: Alleen het absolute minimum behouden voor:
#   - Windows OS (kernel, networking, shell)
#   - Darkroom Booth
#   - Print Spooler + printer drivers
#   - Google Chrome (als kale browser)
#
# VOER UIT ALS ADMINISTRATOR
# Maak EERST een herstelpunt: Checkpoint-Computer -Description "Pre-cleanup"
# ================================================================

#Requires -RunAsAdministrator

$ErrorActionPreference = "SilentlyContinue"

Write-Host @"

  ╔══════════════════════════════════════════════╗
  ║  PHOTOBOOTH PC - AGGRESSIVE CLEANUP SCRIPT  ║
  ╠══════════════════════════════════════════════╣
  ║  Behoudt: Windows Core, Darkroom Booth,     ║
  ║           Print Spooler, Chrome (kaal)       ║
  ╚══════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

# ----------------------------------------------------------------
# 1. VERWIJDER ALLE APPX PAKKETTEN (behalve essentieel)
# ----------------------------------------------------------------
Write-Host "[1/8] Alle niet-essentiële AppX pakketten verwijderen..." -ForegroundColor Yellow

# Whitelist: alleen deze mogen blijven
$whitelist = @(
    "Microsoft.WindowsStore"              # Nodig voor systeem-updates
    "Microsoft.VCLibs"                    # Visual C++ runtime (dependencies)
    "Microsoft.UI.Xaml"                   # UI framework (nodig voor OS)
    "Microsoft.NET"                       # .NET runtime
    "Microsoft.DesktopAppInstaller"       # App installer
    "Microsoft.WindowsTerminal"           # Terminal (handig voor beheer)
    "Microsoft.SecHealthUI"               # Windows Security
    "Microsoft.Windows.ShellExperienceHost"
    "Microsoft.Windows.StartMenuExperienceHost"
    "windows.immersivecontrolpanel"       # Settings app
    "Microsoft.WindowsNotepad"            # Notepad (handig voor debug)
    "Microsoft.HEVCVideoExtension"        # Video codec
    "Microsoft.HEIFImageExtension"        # Image codec
    "Microsoft.WebpImageExtension"        # Image codec
    "Microsoft.RawImageExtension"         # RAW image support (foto's!)
    "Microsoft.StorePurchaseApp"          # Store dependency
)

# Verwijder alles dat NIET op de whitelist staat
Get-AppxPackage -AllUsers | ForEach-Object {
    $dominated = $false
    foreach ($w in $whitelist) {
        if ($_.Name -like "*$w*") { $dominated = $true; break }
    }
    if (-not $dominated) {
        Write-Host "  Verwijder: $($_.Name)" -ForegroundColor DarkGray
        Remove-AppxPackage -Package $_.PackageFullName -AllUsers -ErrorAction SilentlyContinue
    }
}

# Verwijder provisioned packages (voorkomt herinstallatie)
Get-AppxProvisionedPackage -Online | ForEach-Object {
    $dominated = $false
    foreach ($w in $whitelist) {
        if ($_.PackageName -like "*$w*") { $dominated = $true; break }
    }
    if (-not $dominated) {
        Write-Host "  Deprovision: $($_.PackageName)" -ForegroundColor DarkGray
        Remove-AppxProvisionedPackage -Online -PackageName $_.PackageName -ErrorAction SilentlyContinue
    }
}

Write-Host "  Klaar." -ForegroundColor Green

# ----------------------------------------------------------------
# 2. ONEDRIVE VOLLEDIG VERWIJDEREN
# ----------------------------------------------------------------
Write-Host "`n[2/8] OneDrive volledig verwijderen..." -ForegroundColor Yellow

Stop-Process -Name "OneDrive" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

if (Test-Path "$env:SystemRoot\SysWOW64\OneDriveSetup.exe") {
    & "$env:SystemRoot\SysWOW64\OneDriveSetup.exe" /uninstall
} elseif (Test-Path "$env:SystemRoot\System32\OneDriveSetup.exe") {
    & "$env:SystemRoot\System32\OneDriveSetup.exe" /uninstall
}
Start-Sleep -Seconds 3

# Verwijder restanten
Remove-Item -Path "$env:USERPROFILE\OneDrive" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$env:LOCALAPPDATA\Microsoft\OneDrive" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$env:PROGRAMDATA\Microsoft OneDrive" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "C:\OneDriveTemp" -Recurse -Force -ErrorAction SilentlyContinue

# Voorkom dat OneDrive terugkomt
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\OneDrive" /v "DisableFileSyncNGSC" /t REG_DWORD /d 1 /f | Out-Null

Write-Host "  Klaar." -ForegroundColor Green

# ----------------------------------------------------------------
# 3. EDGE NEUTRALISEREN (kan niet volledig verwijderd, maar uitschakelen)
# ----------------------------------------------------------------
Write-Host "`n[3/8] Edge neutraliseren..." -ForegroundColor Yellow

# Stop Edge achtergrondprocessen
reg add "HKLM\SOFTWARE\Policies\Microsoft\Edge" /v "BackgroundModeEnabled" /t REG_DWORD /d 0 /f | Out-Null
reg add "HKLM\SOFTWARE\Policies\Microsoft\Edge" /v "StartupBoostEnabled" /t REG_DWORD /d 0 /f | Out-Null
reg add "HKLM\SOFTWARE\Policies\Microsoft\Edge" /v "HubsSidebarEnabled" /t REG_DWORD /d 0 /f | Out-Null

# Voorkom Edge als standaard PDF/HTML handler
reg add "HKLM\SOFTWARE\Policies\Microsoft\Edge" /v "DefaultBrowserSettingEnabled" /t REG_DWORD /d 0 /f | Out-Null

# Disable Edge scheduled tasks
Get-ScheduledTask -TaskPath "\Microsoft\EdgeUpdate\*" -ErrorAction SilentlyContinue |
    Disable-ScheduledTask -ErrorAction SilentlyContinue
Get-ScheduledTask | Where-Object { $_.TaskName -like "*MicrosoftEdge*" } |
    Disable-ScheduledTask -ErrorAction SilentlyContinue

Write-Host "  Klaar." -ForegroundColor Green

# ----------------------------------------------------------------
# 4. SERVICES UITSCHAKELEN (agressief)
# ----------------------------------------------------------------
Write-Host "`n[4/8] Onnodige services uitschakelen..." -ForegroundColor Yellow

$disableServices = @(
    # Telemetrie & diagnostiek
    "DiagTrack"                    # Connected User Experiences and Telemetry
    "dmwappushservice"             # WAP Push
    "diagnosticshub.standardcollector.service"

    # Xbox (alles)
    "XblAuthManager"
    "XblGameSave"
    "XboxNetApiSvc"
    "XboxGipSvc"

    # Niet-nodig voor photobooth
    "WSearch"                      # Windows Search
    "MapsBroker"                   # Kaarten
    "lfsvc"                        # Geolocatie
    "SharedAccess"                 # Internet Connection Sharing
    "WMPNetworkSvc"                # Windows Media Player Sharing
    "wisvc"                        # Windows Insider Service
    "RetailDemo"                   # Retail Demo
    "MessagingService"             # SMS/MMS
    "PcaSvc"                       # Program Compatibility Assistant
    "SysMain"                      # Superfetch (SSD bespaart)
    "TabletInputService"           # Tablet toetsenbord
    "PhoneSvc"                     # Telefonie
    "TapiSrv"                      # Telephony API
    "Fax"                          # Fax
    "WerSvc"                       # Windows Error Reporting
    "wercplsupport"                # Error Reporting Control Panel
    "WbioSrvc"                     # Biometrie (geen fingerprint op photobooth)
    "SEMgrSvc"                     # Payments and NFC
    "icssvc"                       # Mobile Hotspot
    "WlanSvc"                      # WiFi (als je ethernet gebruikt)
    "RemoteRegistry"               # Remote Registry
    "RemoteAccess"                 # Routing and Remote Access
    "SCardSvr"                     # Smart Card
    "ScDeviceEnum"                 # Smart Card Device Enumeration
    "SCPolicySvc"                  # Smart Card Removal Policy
    "NaturalAuthentication"        # Proximity-based auth
    "AJRouter"                     # AllJoyn Router
    "ALG"                          # Application Layer Gateway
    "BDESVC"                       # BitLocker (als niet gebruikt)
    "wlidsvc"                      # Microsoft Account Sign-in Assistant
    "OneSyncSvc"                   # Sync Host
    "CDPSvc"                       # Connected Devices Platform
    "CDPUserSvc"                   # Connected Devices Platform User
    "WpnService"                   # Push Notifications (niet nodig)
    "WpnUserService"               # Push Notifications User
    "DsSvc"                        # Data Sharing Service
    "DusmSvc"                      # Data Usage
    "TokenBroker"                  # Web Account Manager
)

foreach ($svc in $disableServices) {
    $service = Get-Service -Name $svc -ErrorAction SilentlyContinue
    if ($service) {
        Stop-Service -Name $svc -Force -ErrorAction SilentlyContinue
        Set-Service -Name $svc -StartupType Disabled -ErrorAction SilentlyContinue
        Write-Host "  Uit: $svc" -ForegroundColor DarkGray
    }
}

# BELANGRIJK: Print Spooler actief houden!
Set-Service -Name "Spooler" -StartupType Automatic
Start-Service -Name "Spooler"
Write-Host "  AAN: Spooler (Print Spooler)" -ForegroundColor Green

Write-Host "  Klaar." -ForegroundColor Green

# ----------------------------------------------------------------
# 5. GEPLANDE TAKEN UITSCHAKELEN (telemetrie, updates, reclame)
# ----------------------------------------------------------------
Write-Host "`n[5/8] Telemetrie en onnodige geplande taken uitschakelen..." -ForegroundColor Yellow

$disableTasks = @(
    "\Microsoft\Windows\Application Experience\Microsoft Compatibility Appraiser"
    "\Microsoft\Windows\Application Experience\ProgramDataUpdater"
    "\Microsoft\Windows\Application Experience\StartupAppTask"
    "\Microsoft\Windows\Customer Experience Improvement Program\Consolidator"
    "\Microsoft\Windows\Customer Experience Improvement Program\UsbCeip"
    "\Microsoft\Windows\DiskDiagnostic\Microsoft-Windows-DiskDiagnosticDataCollector"
    "\Microsoft\Windows\Feedback\Siuf\DmClient"
    "\Microsoft\Windows\Feedback\Siuf\DmClientOnScenarioDownload"
    "\Microsoft\Windows\Maps\MapsToastTask"
    "\Microsoft\Windows\Maps\MapsUpdateTask"
    "\Microsoft\Windows\Windows Error Reporting\QueueReporting"
    "\Microsoft\Windows\WindowsUpdate\Scheduled Start"
    "\Microsoft\Windows\CloudExperienceHost\CreateObjectTask"
    "\Microsoft\Windows\DiskFootprint\Diagnostics"
    "\Microsoft\Windows\PI\Sqm-Tasks"
    "\Microsoft\Windows\NetTrace\GatherNetworkInfo"
)

foreach ($task in $disableTasks) {
    schtasks /Change /TN $task /Disable 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Uit: $($task.Split('\')[-1])" -ForegroundColor DarkGray
    }
}

Write-Host "  Klaar." -ForegroundColor Green

# ----------------------------------------------------------------
# 6. REGISTRY TWEAKS (telemetrie, visuele rommel, performance)
# ----------------------------------------------------------------
Write-Host "`n[6/8] Registry optimalisaties..." -ForegroundColor Yellow

# --- Telemetrie uit ---
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection" /v "AllowTelemetry" /t REG_DWORD /d 0 /f | Out-Null
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection" /v "AllowTelemetry" /t REG_DWORD /d 0 /f | Out-Null

# --- Advertising ID uit ---
reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\AdvertisingInfo" /v "Enabled" /t REG_DWORD /d 0 /f | Out-Null

# --- Cortana uit ---
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search" /v "AllowCortana" /t REG_DWORD /d 0 /f | Out-Null
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search" /v "AllowSearchToUseLocation" /t REG_DWORD /d 0 /f | Out-Null
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search" /v "AllowCloudSearch" /t REG_DWORD /d 0 /f | Out-Null

# --- Taakbalk volledig opschonen ---
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Search" /v "SearchboxTaskbarMode" /t REG_DWORD /d 0 /f | Out-Null
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v "TaskbarDa" /t REG_DWORD /d 0 /f | Out-Null           # Widgets uit
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v "TaskbarMn" /t REG_DWORD /d 0 /f | Out-Null           # Chat uit
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v "ShowCopilotButton" /t REG_DWORD /d 0 /f | Out-Null   # Copilot uit
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v "ShowTaskViewButton" /t REG_DWORD /d 0 /f | Out-Null  # Task View uit

# --- Start menu opschonen ---
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v "Start_TrackDocs" /t REG_DWORD /d 0 /f | Out-Null     # Recente bestanden uit
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v "Start_TrackProgs" /t REG_DWORD /d 0 /f | Out-Null    # Recente apps uit
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\Explorer" /v "HideRecentlyAddedApps" /t REG_DWORD /d 1 /f | Out-Null

# --- Suggesties en tips uit ---
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" /v "SubscribedContent-338389Enabled" /t REG_DWORD /d 0 /f | Out-Null
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" /v "SubscribedContent-310093Enabled" /t REG_DWORD /d 0 /f | Out-Null
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" /v "SubscribedContent-338388Enabled" /t REG_DWORD /d 0 /f | Out-Null
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" /v "SubscribedContent-353694Enabled" /t REG_DWORD /d 0 /f | Out-Null
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" /v "SubscribedContent-353696Enabled" /t REG_DWORD /d 0 /f | Out-Null
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" /v "SystemPaneSuggestionsEnabled" /t REG_DWORD /d 0 /f | Out-Null
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" /v "SoftLandingEnabled" /t REG_DWORD /d 0 /f | Out-Null
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" /v "SilentInstalledAppsEnabled" /t REG_DWORD /d 0 /f | Out-Null  # Voorkom auto-install apps
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" /v "ContentDeliveryAllowed" /t REG_DWORD /d 0 /f | Out-Null
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" /v "OemPreInstalledAppsEnabled" /t REG_DWORD /d 0 /f | Out-Null
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" /v "PreInstalledAppsEnabled" /t REG_DWORD /d 0 /f | Out-Null
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" /v "PreInstalledAppsEverEnabled" /t REG_DWORD /d 0 /f | Out-Null

# --- Lock screen spotlight/tips uit ---
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" /v "RotatingLockScreenEnabled" /t REG_DWORD /d 0 /f | Out-Null
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" /v "RotatingLockScreenOverlayEnabled" /t REG_DWORD /d 0 /f | Out-Null

# --- Privacy ---
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Privacy" /v "TailoredExperiencesWithDiagnosticDataEnabled" /t REG_DWORD /d 0 /f | Out-Null
reg add "HKCU\Software\Microsoft\Input\TIPC" /v "Enabled" /t REG_DWORD /d 0 /f | Out-Null  # Handwriting data uit
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\AppPrivacy" /v "LetAppsRunInBackground" /t REG_DWORD /d 2 /f | Out-Null  # Achtergrond-apps uit

# --- Performance: visuele effecten minimaliseren ---
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects" /v "VisualFXSetting" /t REG_DWORD /d 2 /f | Out-Null
reg add "HKCU\Control Panel\Desktop" /v "UserPreferencesMask" /t REG_BINARY /d 9012038010000000 /f | Out-Null

# --- Notificaties minimaliseren ---
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\PushNotifications" /v "ToastEnabled" /t REG_DWORD /d 0 /f | Out-Null
reg add "HKCU\Software\Policies\Microsoft\Windows\Explorer" /v "DisableNotificationCenter" /t REG_DWORD /d 1 /f | Out-Null

Write-Host "  Klaar." -ForegroundColor Green

# ----------------------------------------------------------------
# 7. WINDOWS OPTIONELE FEATURES VERWIJDEREN
# ----------------------------------------------------------------
Write-Host "`n[7/8] Onnodige Windows features verwijderen..." -ForegroundColor Yellow

$removeFeatures = @(
    "WindowsMediaPlayer"
    "WorkFolders-Client"
    "MathRecognizer"
    "Internet-Explorer-Optional-amd64"
    "MediaPlayback"
    "Microsoft-Windows-WordPad"
    "Printing-XPSServices-Features"      # XPS printer (normale printers blijven)
    "Recall"                              # Windows Recall (AI screenshot feature)
)

foreach ($feature in $removeFeatures) {
    $f = Get-WindowsOptionalFeature -Online -FeatureName $feature -ErrorAction SilentlyContinue
    if ($f -and $f.State -eq "Enabled") {
        Disable-WindowsOptionalFeature -Online -FeatureName $feature -NoRestart -ErrorAction SilentlyContinue | Out-Null
        Write-Host "  Uit: $feature" -ForegroundColor DarkGray
    }
}

# Verwijder Windows Capabilities
$removeCaps = @(
    "App.Support.QuickAssist*"
    "Browser.InternetExplorer*"
    "Hello.Face*"
    "MathRecognizer*"
    "Microsoft.Windows.MSPaint*"
    "Microsoft.Windows.PowerShell.ISE*"
    "Microsoft.Windows.WordPad*"
    "Media.WindowsMediaPlayer*"
    "App.StepsRecorder*"
    "Language.Handwriting*"
    "Language.OCR*"
    "Language.Speech*"
)

foreach ($cap in $removeCaps) {
    Get-WindowsCapability -Online | Where-Object { $_.Name -like $cap -and $_.State -eq "Installed" } | ForEach-Object {
        Remove-WindowsCapability -Online -Name $_.Name -ErrorAction SilentlyContinue | Out-Null
        Write-Host "  Verwijderd: $($_.Name)" -ForegroundColor DarkGray
    }
}

Write-Host "  Klaar." -ForegroundColor Green

# ----------------------------------------------------------------
# 8. OPRUIMEN
# ----------------------------------------------------------------
Write-Host "`n[8/8] Schijfruimte opschonen..." -ForegroundColor Yellow

# Temp bestanden
Remove-Item -Path "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "C:\Windows\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue

# Delivery Optimization cache
Delete-DeliveryOptimizationCache -Force -ErrorAction SilentlyContinue

# Windows Update cache (voorzichtig)
Stop-Service -Name "wuauserv" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "C:\Windows\SoftwareDistribution\Download\*" -Recurse -Force -ErrorAction SilentlyContinue
Start-Service -Name "wuauserv" -ErrorAction SilentlyContinue

Write-Host "  Klaar." -ForegroundColor Green

# ----------------------------------------------------------------
# SAMENVATTING
# ----------------------------------------------------------------
Write-Host @"

  ╔══════════════════════════════════════════════╗
  ║              CLEANUP VOLTOOID!               ║
  ╠══════════════════════════════════════════════╣
  ║  Behouden:                                   ║
  ║    - Windows Core + Shell                    ║
  ║    - Print Spooler (Automatic)               ║
  ║    - Darkroom Booth (onaangetast)            ║
  ║    - Google Chrome (kaal via policies)       ║
  ║    - Windows Store (systeem-updates)         ║
  ║                                              ║
  ║  Volgende stap:                              ║
  ║    1. Voer chrome-lockdown.ps1 uit           ║
  ║    2. Herstart de computer                   ║
  ╚══════════════════════════════════════════════╝

"@ -ForegroundColor Cyan
