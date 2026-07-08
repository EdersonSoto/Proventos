
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / "envie.env")

PASTA_CSV = BASE_DIR / "csv"

PASTA_BACKUP = BASE_DIR / "backup"

PASTA_RELATORIOS = BASE_DIR / "relatorios"

PASTA_TEMP = BASE_DIR / "temp"

for pasta in [
    PASTA_CSV,
    PASTA_BACKUP,
    PASTA_RELATORIOS,
    PASTA_TEMP
]:
    os.makedirs(
        pasta,
        exist_ok=True
    )
