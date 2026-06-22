
import sqlite3
import os

PASTA_DB = r"C:\Investimentos\Proventos\database"

os.makedirs(
    PASTA_DB,
    exist_ok=True
)

BANCO = os.path.join(
    PASTA_DB,
    "proventos.db"
)

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

