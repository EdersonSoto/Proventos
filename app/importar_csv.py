
import pandas as pd
import glob
import os

from banco import conectar
from config import PASTA_CSV


def obter_ativo(texto):

    palavras = str(texto).split()

    for palavra in reversed(palavras):

        palavra = palavra.replace("/", "")

        if len(palavra) >= 5:
            return palavra

    return ""


def determinar_tipo(ativo):

    ativo = str(ativo).upper()

    if ativo.endswith("11"):
        return "FII"

    return "AÇÃO"


def importar_proventos():

    conn = conectar()

    arquivos = (
        glob.glob(
            os.path.join(
                PASTA_CSV,
                "*.xlsx"
            )
        )
        +
        glob.glob(
            os.path.join(
                PASTA_CSV,
                "*.csv"
            )
        )
    )

    total_importado = 0

    for arquivo in arquivos:

        try:

            print(
                f"Lendo: {os.path.basename(arquivo)}"
            )

            # =========================
            # XLSX CLEAR
            # =========================

            if arquivo.lower().endswith(".xlsx"):

                df = pd.read_excel(
                    arquivo,
                    header=None
                )

                df.columns = df.iloc[13]

                df = df.iloc[14:]

                df = df.dropna(
                    how="all"
                )

            # =========================
            # CSV
            # =========================

            else:

                df = pd.read_csv(
                    arquivo,
                    sep=None,
                    engine="python"
                )

            # =========================
            # LIMPEZA
            # =========================

            df.columns = [
                str(col).strip()
                for col in df.columns
            ]

            coluna_data = "Movimentação"
            coluna_descricao = "Lançamento"
            coluna_valor = "Valor (R$)"

            if coluna_valor not in df.columns:

                print(
                    f"Arquivo ignorado: {arquivo}"
                )

                continue

            df[coluna_valor] = pd.to_numeric(
                df[coluna_valor],
                errors="coerce"
            )

            df = df.dropna(
                subset=[coluna_valor]
            )

            df = df[
                df[coluna_descricao]
                .astype(str)
                .str.contains(
                    "DIVIDENDOS|RENDIMENTOS|JUROS",
                    case=False,
                    na=False
                )
            ]

            # =========================
            # IMPORTAÇÃO
            # =========================

            for _, linha in df.iterrows():

                try:

                    data_pagamento = (
                        pd.to_datetime(
                            linha[coluna_data]
                        )
                        .strftime("%Y-%m-%d")
                    )

                    descricao = str(
                        linha[coluna_descricao]
                    )

                    valor = float(
                        linha[coluna_valor]
                    )

                    ativo = obter_ativo(
                        descricao
                    )

                    tipo = determinar_tipo(
                        ativo
                    )

                    existe = conn.execute(
                        """
                        SELECT COUNT(*)
                        FROM proventos
                        WHERE
                            data_pagamento = ?
                            AND ativo = ?
                            AND valor = ?
                        """,
                        (
                            data_pagamento,
                            ativo,
                            valor
                        )
                    ).fetchone()[0]

                    if existe == 0:

                        conn.execute(
                            """
                            INSERT INTO proventos
                            (
                                data_pagamento,
                                ativo,
                                tipo,
                                valor,
                                origem
                            )
                            VALUES
                            (
                                ?, ?, ?, ?, ?
                            )
                            """,
                            (
                                data_pagamento,
                                ativo,
                                tipo,
                                valor,
                                os.path.basename(
                                    arquivo
                                )
                            )
                        )

                        total_importado += 1

                except Exception as erro_linha:

                    print(
                        f"Erro linha: {erro_linha}"
                    )

        except Exception as erro_arquivo:

            print(
                f"Erro no arquivo: {arquivo}"
            )

            print(
                erro_arquivo
            )

    conn.commit()

    conn.close()

    return total_importado


if __name__ == "__main__":

    qtd = importar_proventos()

    print()

    print(
        f"{qtd} registros importados."
    )
