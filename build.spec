# -*- mode: python ; coding: utf-8 -*-

import os

from PyInstaller.utils.hooks import collect_all

datas = []
binaries = []
hiddenimports = []

# NOTA: run.py so importa o streamlit.web.cli; os modulos em app/ (config.py,
# banco.py, backup.py, importar_csv.py) sao executados dinamicamente pelo
# Streamlit e NAO sao vistos pela Analysis. Por isso todo pacote que eles
# importam precisa ser listado aqui manualmente.
for pkg in [
    "streamlit",
    "pandas",
    "plotly",
    "openpyxl",
    "dotenv",
    "googleapiclient",
    "google_auth_oauthlib",
    "google_auth_httplib2",
]:
    d, b, h = collect_all(pkg)
    datas += d
    binaries += b
    hiddenimports += h

hiddenimports += [
    "google.auth",
    "google.auth.transport.requests",
    "google.oauth2.credentials",
]

# envie.env (ID da pasta do Google Drive, metas, etc.) precisa ir junto para o
# app se comportar no computador de destino exatamente como neste PC.
if os.path.isfile("envie.env"):
    datas.append(("envie.env", "."))


a = Analysis(
    ["run.py"],
    pathex=["."],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="ProventosApp",
    console=True,
    icon="assets/icon.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,

    # COPIAR A PASTA app
    Tree("app", prefix="app", excludes=["__pycache__"]),

    # COPIAR O BANCO
    Tree("database", prefix="database"),

    # CONFIGURAÇÕES
    Tree("config", prefix="config"),

    # CSV
    Tree("csv", prefix="csv"),

    name="Proventos",
)