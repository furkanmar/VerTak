[Setup]
AppName=Veresiye Takip Sistemi
AppVersion=1.0
DefaultDirName={autopf}\Veresiye Takip Sistemi
DefaultGroupName=Veresiye Takip Sistemi
UninstallDisplayIcon={app}\VERTAK.exe
OutputDir=.
OutputBaseFilename=VeresiyeTakipKurulum
Compression=lzma
SolidCompression=yes

[Languages]
Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"

[Files]
Source: "InstallerBuild\VERTAK.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "InstallerBuild\data\*"; DestDir: "{app}\data"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "InstallerBuild\resources\poppler\*"; DestDir: "{app}\resources\poppler"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "InstallerBuild\logo.png"; DestDir: "{app}"; Flags: ignoreversion  ; <-- LOGO EKLENDİ

[Icons]
Name: "{group}\Veresiye Takip Sistemi"; Filename: "{app}\VERTAK.exe"
Name: "{commondesktop}\Veresiye Takip Sistemi"; Filename: "{app}\VERTAK.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Masaüstü simgesi oluştur"; GroupDescription: "Ek görevler:"
