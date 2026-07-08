# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

# Coleta todos os data files, metadata, e binaries do streamlit e suas dependências
datas, binaries, hiddenimports = collect_all('streamlit')
datas.extend(collect_all('pandas')[0])
datas.extend(collect_all('plotly')[0])
datas.extend(collect_all('openpyxl')[0])


a = Analysis(
    ['run.py'], # Script principal que executa o app
    pathex=['c:\\Investimentos\\Proventos'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ProventosApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True, # Mantenha True para ver logs do streamlit/erros
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Proventos', # Nome da pasta que será criada em 'dist'
)