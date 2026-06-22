
import os

PASTA_CSV = r"C:\Investimentos\Proventos\csv"

PASTA_BACKUP = r"C:\Investimentos\Proventos\backup"

PASTA_RELATORIOS = r"C:\Investimentos\Proventos\relatorios"

PASTA_TEMP = r"C:\Investimentos\Proventos\temp"

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

