# ================================================================
# GOOGLE CHROME LOCKDOWN - PHOTOBOOTH PC
# ================================================================
# Stribt Chrome af tot een kale browser (alleen zoeken/navigeren).
# Schakelt alle achtergrondprocessen, extensies, sync, notificaties,
# autofill, wachtwoorden, vertalingen, AI features etc. uit.
#
# VOER UIT ALS ADMINISTRATOR (na cleanup-photobooth-pc.ps1)
# ================================================================

#Requires -RunAsAdministrator

$ErrorActionPreference = "SilentlyContinue"

Write-Host @"

  ╔══════════════════════════════════════════════╗
  ║     CHROME LOCKDOWN - PHOTOBOOTH MODE       ║
  ╚══════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

$chromePolicyPath = "HKLM:\SOFTWARE\Policies\Google\Chrome"

# Maak policy key aan als die niet bestaat
if (-not (Test-Path $chromePolicyPath)) {
    New-Item -Path $chromePolicyPath -Force | Out-Null
}

Write-Host "Chrome policies instellen..." -ForegroundColor Yellow

# --- Achtergrondprocessen uit ---
Set-ItemProperty -Path $chromePolicyPath -Name "BackgroundModeEnabled" -Value 0 -Type DWord
Set-ItemProperty -Path $chromePolicyPath -Name "StartupBoostEnabled" -Value 0 -Type DWord
Set-ItemProperty -Path $chromePolicyPath -Name "HardwareAccelerationModeEnabled" -Value 1 -Type DWord

# --- Sync volledig uit ---
Set-ItemProperty -Path $chromePolicyPath -Name "SyncDisabled" -Value 1 -Type DWord
Set-ItemProperty -Path $chromePolicyPath -Name "BrowserSignin" -Value 0 -Type DWord  # 0 = sign-in uitgeschakeld

# --- Wachtwoorden & autofill uit ---
Set-ItemProperty -Path $chromePolicyPath -Name "PasswordManagerEnabled" -Value 0 -Type DWord
Set-ItemProperty -Path $chromePolicyPath -Name "AutofillAddressEnabled" -Value 0 -Type DWord
Set-ItemProperty -Path $chromePolicyPath -Name "AutofillCreditCardEnabled" -Value 0 -Type DWord
Set-ItemProperty -Path $chromePolicyPath -Name "PaymentMethodQueryEnabled" -Value 0 -Type DWord

# --- Notificaties uit ---
Set-ItemProperty -Path $chromePolicyPath -Name "DefaultNotificationsSetting" -Value 2 -Type DWord  # 2 = blokkeer alles

# --- Vertalingen uit ---
Set-ItemProperty -Path $chromePolicyPath -Name "TranslateEnabled" -Value 0 -Type DWord

# --- AI / Gemini / Smart features uit ---
Set-ItemProperty -Path $chromePolicyPath -Name "GenAIDefaultSettings" -Value 2 -Type DWord  # Disable generative AI
Set-ItemProperty -Path $chromePolicyPath -Name "CreateThemesSettings" -Value 2 -Type DWord
Set-ItemProperty -Path $chromePolicyPath -Name "HelpMeWriteSettings" -Value 2 -Type DWord
Set-ItemProperty -Path $chromePolicyPath -Name "TabOrganizerSettings" -Value 2 -Type DWord
Set-ItemProperty -Path $chromePolicyPath -Name "DevToolsGenAiSettings" -Value 2 -Type DWord

# --- Side panel / shopping / reviews uit ---
Set-ItemProperty -Path $chromePolicyPath -Name "ShoppingListEnabled" -Value 0 -Type DWord
Set-ItemProperty -Path $chromePolicyPath -Name "GoogleSearchSidePanelEnabled" -Value 0 -Type DWord

# --- Extensies blokkeren (geen enkele extensie toestaan) ---
$extPolicyPath = "$chromePolicyPath\ExtensionInstallBlocklist"
if (-not (Test-Path $extPolicyPath)) {
    New-Item -Path $extPolicyPath -Force | Out-Null
}
Set-ItemProperty -Path $extPolicyPath -Name "1" -Value "*" -Type String  # Blokkeer alle extensies

# --- Popups en redirects blokkeren ---
Set-ItemProperty -Path $chromePolicyPath -Name "DefaultPopupsSetting" -Value 2 -Type DWord

# --- Automatische downloads voorkomen ---
Set-ItemProperty -Path $chromePolicyPath -Name "AutoOpenFileTypes" -Value "" -Type String

# --- Geolocatie uit ---
Set-ItemProperty -Path $chromePolicyPath -Name "DefaultGeolocationSetting" -Value 2 -Type DWord

# --- Camera en microfoon via Chrome uit (photobooth gebruikt eigen software) ---
Set-ItemProperty -Path $chromePolicyPath -Name "VideoCaptureAllowed" -Value 0 -Type DWord
Set-ItemProperty -Path $chromePolicyPath -Name "AudioCaptureAllowed" -Value 0 -Type DWord

# --- USB, Bluetooth, Serial via Chrome uit ---
Set-ItemProperty -Path $chromePolicyPath -Name "DefaultWebUsbGuardSetting" -Value 2 -Type DWord
Set-ItemProperty -Path $chromePolicyPath -Name "DefaultWebBluetoothGuardSetting" -Value 2 -Type DWord
Set-ItemProperty -Path $chromePolicyPath -Name "DefaultSerialGuardSetting" -Value 2 -Type DWord

# --- Rapportage en metrics uit ---
Set-ItemProperty -Path $chromePolicyPath -Name "MetricsReportingEnabled" -Value 0 -Type DWord
Set-ItemProperty -Path $chromePolicyPath -Name "UrlKeyedAnonymizedDataCollectionEnabled" -Value 0 -Type DWord
Set-ItemProperty -Path $chromePolicyPath -Name "SpellCheckServiceEnabled" -Value 0 -Type DWord

# --- Promoties en "what's new" uit ---
Set-ItemProperty -Path $chromePolicyPath -Name "PromotionalTabsEnabled" -Value 0 -Type DWord
Set-ItemProperty -Path $chromePolicyPath -Name "ShowFullUrlsInAddressBar" -Value 1 -Type DWord

# --- Zoekprovider suggesties uit ---
Set-ItemProperty -Path $chromePolicyPath -Name "SearchSuggestEnabled" -Value 0 -Type DWord

# --- Mededelingen na update uit ---
Set-ItemProperty -Path $chromePolicyPath -Name "SuppressUnsupportedOSWarning" -Value 1 -Type DWord

# --- Restore session na crash uit (clean start) ---
Set-ItemProperty -Path $chromePolicyPath -Name "RestoreOnStartup" -Value 5 -Type DWord  # 5 = open new tab page

# --- Chrome updates behouden (belangrijk voor security) ---
# We laten updates AAN - alleen de bloat gaat eruit

Write-Host "  Alle policies ingesteld." -ForegroundColor Green

# ----------------------------------------------------------------
# Chrome startup flags instellen voor minimal mode
# ----------------------------------------------------------------
Write-Host "`nChrome shortcut optimaliseren..." -ForegroundColor Yellow

$chromeShortcuts = @(
    "$env:PUBLIC\Desktop\Google Chrome.lnk"
    "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Google Chrome.lnk"
    "$env:PROGRAMDATA\Microsoft\Windows\Start Menu\Programs\Google Chrome.lnk"
)

$shell = New-Object -ComObject WScript.Shell

foreach ($shortcut in $chromeShortcuts) {
    if (Test-Path $shortcut) {
        $lnk = $shell.CreateShortcut($shortcut)
        $target = $lnk.TargetPath
        # Voeg flags toe voor minimale Chrome
        $lnk.Arguments = "--disable-background-networking --disable-component-update --disable-default-apps --disable-extensions --no-first-run --disable-infobars"
        $lnk.Save()
        Write-Host "  Aangepast: $shortcut" -ForegroundColor DarkGray
    }
}

Write-Host @"

  ╔══════════════════════════════════════════════╗
  ║        CHROME LOCKDOWN VOLTOOID!             ║
  ╠══════════════════════════════════════════════╣
  ║  Uitgeschakeld:                              ║
  ║    - Sync, Sign-in, Wachtwoorden            ║
  ║    - Autofill, Vertalingen, Notificaties    ║
  ║    - AI/Gemini features                      ║
  ║    - Extensies, Camera, Microfoon           ║
  ║    - Telemetrie, Shopping, Side panel       ║
  ║    - Achtergrondprocessen                    ║
  ║                                              ║
  ║  Actief:                                     ║
  ║    - Browsen & zoeken                        ║
  ║    - Chrome updates (security)               ║
  ║                                              ║
  ║  Herstart Chrome om policies te activeren.   ║
  ╚══════════════════════════════════════════════╝

"@ -ForegroundColor Cyan
