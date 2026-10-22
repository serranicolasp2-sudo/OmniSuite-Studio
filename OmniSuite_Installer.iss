; Inno Setup 6 Script — OmniSuite Studio
; Suite Audiovisual para Creadores & Editores — Tu Tiendita IA (https://tutiendita-ia.store)

#define AppName "OmniSuite Studio"
#define AppVersion "1.0"
#define AppPublisher "Tu Tiendita IA"
#define AppURL "https://tutiendita-ia.store"
#define Raiz ".."

[Setup]
AppId={{9B7F1C4E-62A8-4D91-8D03-5E1C3A7B9F02}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion} — Edición Creadores (Tu Tiendita IA)
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}
PrivilegesRequired=lowest
DefaultDirName={localappdata}\Programs\Tu Tiendita IA\OmniSuite Studio
DefaultGroupName=Tu Tiendita IA\OmniSuite Studio
DisableProgramGroupPage=no
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
OutputDir={#Raiz}\Instaladores\00 OmniSuite Studio\Instalador
OutputBaseFilename=OmniSuite Studio Instalador Completo 1.0
Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes
LZMANumBlockThreads=1
LZMADictionarySize=131072
DiskSpanning=no
WizardStyle=modern
SetupIconFile={#Raiz}\iconos\omnisuite.ico
UninstallDisplayIcon={app}\OmniSuite Studio.exe
UninstallDisplayName={#AppName}

[Types]
Name: "full"; Description: "Instalación Completa (All-in-One — Recomendado para Creadores & Estudios)"
Name: "videotools"; Description: "Solo Herramientas de Video (Booster, Flow, Scale)"
Name: "compact"; Description: "Instalación Básica (OmniSuite Hub)"
Name: "custom"; Description: "Instalación Personalizada"; Flags: iscustom

[Components]
Name: "hub"; Description: "OmniSuite Hub — Centro de Control y Lanzador Rápido"; Types: full videotools compact custom; Flags: fixed
Name: "omniboost"; Description: "OmniBoost Studio — Video Booster Ultra (Restauración, CAS FidelityFX & Anti-Banding)"; Types: full videotools custom
Name: "omniflow"; Description: "OmniFlow FPS Booster — Interpolación HFR 60/120 FPS"; Types: full videotools custom
Name: "omniscale"; Description: "OmniScale Studio — Upscaler 1080p / 2K / 4K (Adaptativo Vertical 9:16 y 16:9)"; Types: full videotools custom
Name: "transcriptor"; Description: "Transcriptor Local — Diarización 4 Hablantes + Whisper large-v3-turbo (100% Offline)"; Types: full custom

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
; 1. Centro de Control (Hub)
Source: "{#Raiz}\OmniSuite Studio\dist\OmniSuite Studio\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: hub
Source: "{#Raiz}\OmniSuite Studio\LEEME.md"; DestDir: "{app}"; Flags: ignoreversion; Components: hub
Source: "{#Raiz}\OmniSuite Studio\INSTRUCTIVO.md"; DestDir: "{app}"; Flags: ignoreversion; Components: hub

; 2. OmniBoost Studio
Source: "{#Raiz}\Instaladores\01 Video Booster\Portable\OmniBoost Studio Portable\*"; DestDir: "{app}\OmniBoost Studio"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: omniboost

; 3. OmniFlow FPS Booster (reutiliza los binarios de FFmpeg para deduplicación óptima)
Source: "{#Raiz}\Instaladores\02 FPS Booster\Portable\OmniFlow FPS Booster Portable\*"; DestDir: "{app}\OmniFlow FPS Booster"; Excludes: "\bin\*"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: omniflow
Source: "{#Raiz}\Instaladores\01 Video Booster\Portable\OmniBoost Studio Portable\bin\*"; DestDir: "{app}\OmniFlow FPS Booster\bin"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: omniflow

; 4. OmniScale Studio (reutiliza los binarios de FFmpeg para deduplicación óptima)
Source: "{#Raiz}\Instaladores\03 Upscaler\Portable\OmniScale Studio Portable\*"; DestDir: "{app}\OmniScale Studio"; Excludes: "\bin\*"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: omniscale
Source: "{#Raiz}\Instaladores\01 Video Booster\Portable\OmniBoost Studio Portable\bin\*"; DestDir: "{app}\OmniScale Studio\bin"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: omniscale

; 5. Transcriptor Local
Source: "{#Raiz}\Instaladores\04_Transcriptor\Portable\Transcriptor_Portable\*"; DestDir: "{app}\Transcriptor"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: transcriptor

[Icons]
; Menú Inicio
Name: "{group}\OmniSuite Studio"; Filename: "{app}\OmniSuite Studio.exe"; IconFilename: "{app}\iconos\omnisuite.ico"; Components: hub
Name: "{group}\OmniBoost Studio"; Filename: "{app}\OmniBoost Studio\OmniBoost Studio.exe"; IconFilename: "{app}\iconos\omniboost.ico"; Components: omniboost
Name: "{group}\OmniFlow FPS Booster"; Filename: "{app}\OmniFlow FPS Booster\OmniFlow FPS Booster.exe"; IconFilename: "{app}\iconos\omniflow.ico"; Components: omniflow
Name: "{group}\OmniScale Studio"; Filename: "{app}\OmniScale Studio\OmniScale Studio.exe"; IconFilename: "{app}\iconos\omniscale.ico"; Components: omniscale
Name: "{group}\Transcriptor Local"; Filename: "{app}\Transcriptor\Transcriptor.exe"; IconFilename: "{app}\iconos\transcriptor.ico"; Components: transcriptor
Name: "{group}\Guía de la Suite (LEEME)"; Filename: "{app}\LEEME.md"; Components: hub
Name: "{group}\Instructivo de Workflows"; Filename: "{app}\INSTRUCTIVO.md"; Components: hub
Name: "{group}\Sitio Web Oficial Tu Tiendita IA"; Filename: "{#AppURL}"

; Escritorio
Name: "{autodesktop}\OmniSuite Studio"; Filename: "{app}\OmniSuite Studio.exe"; IconFilename: "{app}\iconos\omnisuite.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\OmniSuite Studio.exe"; Description: "{cm:LaunchProgram,OmniSuite Studio}"; Flags: nowait postinstall skipifsilent
