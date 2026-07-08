; Script for Inno Setup
; http://www.jrsoftware.org/isinfo.php

[Setup]
AppName=Controle de Proventos
AppVersion=1.0
AppPublisher=Soto Company
DefaultDirName={autopf}\Controle de Proventos
DefaultGroupName=Controle de Proventos
DisableProgramGroupPage=yes
OutputBaseFilename=Proventos_Setup_v1.0
Compression=lzma
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\ProventosApp.exe

; --- ARQUIVOS ---
; Pega todos os arquivos da pasta 'dist/Proventos' gerada pelo PyInstaller
; e os coloca no diretório de instalação {app}.
[Files]
Source: "..\dist\Proventos\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\Proventos\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; --- ÍCONES E ATALHOS ---
[Icons]
; Atalho no Menu Iniciar
Name: "{group}\Controle de Proventos"; Filename: "{app}\ProventosApp.exe"

; Atalho na Área de Trabalho (opcional)
Name: "{autodesktop}\Controle de Proventos"; Filename: "{app}\ProventosApp.exe"; Tasks: desktopicon

; --- TAREFAS PÓS-INSTALAÇÃO ---
; Pergunta ao usuário se ele deseja criar um atalho na área de trabalho.
[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}";

; --- EXECUTAR APÓS A INSTALAÇÃO ---
; Abre o aplicativo automaticamente após a instalação ser concluída.
[Run]
Filename: "{app}\ProventosApp.exe"; Description: "{cm:LaunchProgram,Controle de Proventos}"; Flags: nowait postinstall skipifsilent

; --- REGISTRO DO DESINSTALADOR ---
; Garante que o aplicativo apareça em "Adicionar ou remover programas".
[UninstallDelete]
Type: filesandordirs; Name: "{app}"