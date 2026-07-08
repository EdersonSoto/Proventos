
import sqlite3
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PASTA_DB = BASE_DIR / "database"
PASTA_DB.mkdir(exist_ok=True)

BANCO = PASTA_DB / "proventos.db"

def conectar():

    conn = sqlite3.connect(
        BANCO
    )

    conn.execute("""
    CREATE TABLE IF NOT EXISTS proventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_pagamento TEXT,
        ativo TEXT,
        tipo TEXT,
        valor REAL,
        origem TEXT
    )
    """)

    conn.commit()

    return conn
