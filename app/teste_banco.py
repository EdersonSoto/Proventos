
from banco import conectar
import pandas as pd

conn = conectar()

df = pd.read_sql(
    "SELECT * FROM proventos",
    conn
)

print(df.head(20))

print()
print("Total registros:", len(df))

conn.close()

