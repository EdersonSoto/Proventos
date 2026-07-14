# =====================================================
# Build completo do Controle de Proventos
# 1) Instala dependencias
# 2) Gera o executavel com PyInstaller (build.spec)
# 3) Gera o instalador com Inno Setup (proventos_setup.iss)
#
# Uso:
#   .\build.ps1
#   .\build.ps1 -PularInstalacaoDependencias
# =====================================================

param(
    [switch]$PularInstalacaoDependencias
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

function Write-Etapa($mensagem) {
    Write-Host ""
    Write-Host "==> $mensagem" -ForegroundColor Cyan
}

# ---------------------------------------------------
# 1) Dependencias Python
# ---------------------------------------------------
if (-not $PularInstalacaoDependencias) {
    Write-Etapa "Instalando dependencias (requirements.txt)"
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
}

# ---------------------------------------------------
# 2) Limpar builds anteriores
# ---------------------------------------------------
Write-Etapa "Limpando builds anteriores (build/, dist/)"
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue build
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue dist

# ---------------------------------------------------
# 3) PyInstaller
# ---------------------------------------------------
Write-Etapa "Gerando executavel com PyInstaller"
python -m PyInstaller build.spec --noconfirm

if (-not (Test-Path "dist\Proventos\ProventosApp.exe")) {
    throw "Falha ao gerar dist\Proventos\ProventosApp.exe"
}

# ---------------------------------------------------
# 4) Inno Setup
# ---------------------------------------------------
Write-Etapa "Procurando o compilador do Inno Setup (ISCC.exe)"

$candidatosIscc = @(
    "$env:ProgramFiles(x86)\Inno Setup 6\ISCC.exe",
    "$env:ProgramFiles\Inno Setup 6\ISCC.exe",
    "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe"
)

$iscc = $candidatosIscc | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $iscc) {
    $comando = Get-Command ISCC.exe -ErrorAction SilentlyContinue
    if ($comando) {
        $iscc = $comando.Source
    }
}

if (-not $iscc) {
    Write-Host ""
    Write-Host "Inno Setup (ISCC.exe) nao foi encontrado neste computador." -ForegroundColor Yellow
    Write-Host "Instale o Inno Setup 6 (https://jrsoftware.org/isdl.php) e rode este script novamente," -ForegroundColor Yellow
    Write-Host "ou compile manualmente abrindo proventos_setup.iss no Inno Setup Compiler." -ForegroundColor Yellow
    exit 1
}

Write-Etapa "Gerando instalador com Inno Setup"
& $iscc "proventos_setup.iss"

Write-Etapa "Build concluido: Output\Controle_de_Proventos_Setup.exe"
