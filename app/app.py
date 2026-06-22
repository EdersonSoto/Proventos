import streamlit as st
import pandas as pd
import plotly.express as px
import glob
import os

st.set_page_config(
    page_title="Controle de Proventos",
    layout="wide"
)

PASTA_DADOS = r"C:\Investimentos\Proventos\csv"


def obter_ativo(texto):

    palavras = str(texto).split()

    for palavra in reversed(palavras):

        palavra = palavra.replace("/", "")

        if len(palavra) >= 5:
            return palavra

    return ""


def carregar_arquivos():

    arquivos = (
        glob.glob(os.path.join(PASTA_DADOS, "*.xlsx"))
        + glob.glob(os.path.join(PASTA_DADOS, "*.csv"))
    )

    lista = []

    for arquivo in arquivos:

        try:

            if arquivo.lower().endswith(".xlsx"):

                df = pd.read_excel(
                    arquivo,
                    header=None
                )

                df.columns = df.iloc[13]
                df = df.iloc[14:]
                df = df.dropna(how="all")

            else:

                df = pd.read_csv(
                    arquivo,
                    sep=None,
                    engine="python"
                )

            lista.append(df)

        except Exception as e:

            st.error(f"Erro ao ler {arquivo}")
            st.write(e)

    if len(lista) == 0:
        return None

    dados = pd.concat(
        lista,
        ignore_index=True
    )

    return dados


def tratar_dados(dados):

    dados.columns = [str(col).strip() for col in dados.columns]

    dados = dados.loc[
        :,
        dados.columns.astype(str).str.lower() != "nan"
    ]

    dados = dados.loc[
        :,
        ~dados.columns.duplicated()
    ]

    coluna_data = "Movimentação"
    coluna_descricao = "Lançamento"
    coluna_valor = "Valor (R$)"

    dados[coluna_valor] = pd.to_numeric(
        dados[coluna_valor],
        errors="coerce"
    )

    dados = dados.dropna(
        subset=[coluna_valor]
    )

    dados = dados[
        dados[coluna_descricao]
        .astype(str)
        .str.contains(
            "DIVIDENDOS|RENDIMENTOS|JUROS",
            case=False,
            na=False
        )
    ]

    dados[coluna_data] = pd.to_datetime(
        dados[coluna_data],
        errors="coerce"
    )

    dados["Mes"] = dados[coluna_data].dt.strftime("%Y-%m")
    dados["Ano"] = dados[coluna_data].dt.year

    dados["Ativo"] = dados[
        coluna_descricao
    ].apply(obter_ativo)

    dados["Tipo_Provento"] = "FII"

    dados.loc[
        dados[coluna_descricao]
        .str.contains(
            "DIVIDENDOS|JUROS",
            case=False,
            na=False
        ),
        "Tipo_Provento"
    ] = "Ação"

    return dados


def mostrar_resumo(dados):

    coluna_valor = "Valor (R$)"

    total = dados[coluna_valor].sum()

    total_acoes = dados.loc[
        dados["Tipo_Provento"] == "Ação",
        coluna_valor
    ].sum()

    total_fiis = dados.loc[
        dados["Tipo_Provento"] == "FII",
        coluna_valor
    ].sum()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "💰 Total Geral",
        f"R$ {total:,.2f}"
    )

    c2.metric(
        "📈 Ações",
        f"R$ {total_acoes:,.2f}"
    )

    c3.metric(
        "🏢 FIIs",
        f"R$ {total_fiis:,.2f}"
    )


def mostrar_evolucao(dados):


    coluna_valor = "Valor (R$)"

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Proventos por mês")

        resumo_mes = (
            dados.groupby("Mes")[coluna_valor]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            resumo_mes,
            x="Mes",
            y=coluna_valor,
            text_auto=".2f"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader("Proventos por ano")

        resumo_ano = (
            dados.groupby("Ano")[coluna_valor]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            resumo_ano,
            x="Ano",
            y=coluna_valor,
            text_auto=".2f"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
def mostrar_barras_total_por_tipo(dados):

    st.subheader("📊 Ações x FIIs — mês a mês")

    resumo = (
        dados.groupby(["Mes", "Tipo_Provento"])["Valor (R$)"]
        .sum()
        .reset_index()
    )

    total_mes = (
        dados.groupby("Mes")["Valor (R$)"]
        .sum()
        .reset_index()
        .rename(columns={"Valor (R$)": "Total_Mes"})
    )

    fig = px.bar(
        resumo,
        x="Mes",
        y="Valor (R$)",
        color="Tipo_Provento",
        barmode="group",
        color_discrete_map={
            "Ação": "#378ADD",
            "FII":  "#1D9E75"
        },
        labels={
            "Mes": "Mês",
            "Valor (R$)": "Valor (R$)",
            "Tipo_Provento": "Tipo"
        }
    )

    for _, row in total_mes.iterrows():
        fig.add_annotation(
            x=row["Mes"],
            y=row["Total_Mes"],
            text=f"R$ {row['Total_Mes']:,.0f}",
            showarrow=False,
            yshift=10,
            font=dict(size=11, color="#5F5E5A"),
            xanchor="center"
        )

    fig.update_layout(
        xaxis_tickangle=-45,
        legend_title_text="Tipo",
        yaxis_title="Valor (R$)",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        bargap=0.25,
        bargroupgap=0.05
    )

    fig.update_traces(
        textposition="outside",
        texttemplate="R$ %{y:,.2f}"
    )

    st.plotly_chart(fig, use_container_width=True)

def mostrar_acoes(dados):

    st.subheader("📈 Proventos de Ações")

    resumo = (
        dados[dados["Tipo_Provento"] == "Ação"]
        .groupby("Ativo")["Valor (R$)"]
        .sum()
        .reset_index()
        .sort_values(
            "Valor (R$)",
            ascending=False
        )
    )

    st.dataframe(
        resumo,
        use_container_width=True
    )

    fig = px.bar(
        resumo,
        x="Ativo",
        y="Valor (R$)",
        text_auto=".2f"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def mostrar_fiis(dados):

    st.subheader("🏢 Proventos de FIIs")

    resumo = (
        dados[dados["Tipo_Provento"] == "FII"]
        .groupby("Ativo")["Valor (R$)"]
        .sum()
        .reset_index()
        .sort_values(
            "Valor (R$)",
            ascending=False
        )
    )

    st.dataframe(
        resumo,
        use_container_width=True
    )

    fig = px.bar(
        resumo,
        x="Ativo",
        y="Valor (R$)",
        text_auto=".2f"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def mostrar_lancamentos(dados):

    st.subheader("📋 Lançamentos")

    dados = dados.astype(str)

    st.dataframe(
        dados,
        use_container_width=True
    )


st.title("📈 Controle de Proventos")

dados = carregar_arquivos()

if dados is not None:

    dados = tratar_dados(dados)

    mostrar_resumo(dados)

    st.divider()

    mostrar_evolucao(dados)

    st.divider()

    mostrar_barras_total_por_tipo(dados)  

    st.divider()

    mostrar_acoes(dados)

    st.divider()

    mostrar_fiis(dados)

    st.divider()

    mostrar_lancamentos(dados)

