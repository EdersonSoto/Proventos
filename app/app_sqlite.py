
import streamlit as st
import pandas as pd
import plotly.express as px

from banco import conectar
from importar_csv import importar_proventos

st.set_page_config(
    page_title="Controle de Dividendos",
    layout="wide"
)

# ==================================
# IMPORTAÇÃO AUTOMÁTICA
# ==================================

importados = importar_proventos()

# ==================================
# LEITURA DO BANCO
# ==================================

conn = conectar()

dados = pd.read_sql(
    """
    SELECT
        data_pagamento,
        ativo,
        tipo,
        valor,
        origem
    FROM proventos
    ORDER BY data_pagamento
    """,
    conn
)

conn.close()

# ==================================
# PREPARAÇÃO
# ==================================

dados["data_pagamento"] = pd.to_datetime(
    dados["data_pagamento"]
)

dados["Mes"] = (
    dados["data_pagamento"]
    .dt.strftime("%Y-%m")
)


dados["Ano"] = (
    dados["data_pagamento"]
    .dt.year
)

dados["Valor (R$)"] = dados["valor"]

dados["Ativo"] = dados["ativo"]

dados["Tipo_Provento"] = dados["tipo"]


# ==================================
# FILTROS
# ==================================

st.sidebar.header("📂 Filtros")

anos = ["Todos"] + sorted(
    dados["Ano"].astype(str).unique().tolist()
)

ano_selecionado = st.sidebar.selectbox(
    "Ano",
    anos
)

tipos = ["Todos"] + sorted(
    dados["Tipo_Provento"].unique().tolist()
)

tipo_selecionado = st.sidebar.selectbox(
    "Tipo",
    tipos
)

ativos = ["Todos"] + sorted(
    dados["Ativo"].unique().tolist()
)

ativo_selecionado = st.sidebar.selectbox(
    "Ativo",
    ativos
)

if ano_selecionado != "Todos":

    dados = dados[
        dados["Ano"].astype(str)
        == ano_selecionado
    ]

if tipo_selecionado != "Todos":

    dados = dados[
        dados["Tipo_Provento"]
        == tipo_selecionado
    ]

if ativo_selecionado != "Todos":

    dados = dados[
        dados["Ativo"]
        == ativo_selecionado
    ]

# ==================================
# TÍTULO
# ==================================

st.title("📈 Controle de Dividendos")


st.success(
    f"{importados} novos registros importados."
)

# ==================================
# RESUMO
# ==================================

total = dados["Valor (R$)"].sum()

total_acoes = (
    dados[
        dados["Tipo_Provento"] == "AÇÃO"
    ]["Valor (R$)"]
    .sum()
)

total_fiis = (
    dados[
        dados["Tipo_Provento"] == "FII"
    ]["Valor (R$)"]
    .sum()
)

media_mensal = (
    dados.groupby("Mes")
    ["Valor (R$)"]
    .sum()
    .mean()
)

c1, c2, c3, c4 = st.columns(4)

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

c4.metric(
    "📅 Média Mensal",
    f"R$ {media_mensal:,.2f}"
)

META_MENSAL = 300

ultimo_mes = (
    dados.groupby("Mes")
    ["Valor (R$)"]
    .sum()
    .iloc[-1]
)

progresso = min(
    ultimo_mes / META_MENSAL,
    1.0
)

st.subheader(
    "🎯 Meta Mensal"
)

st.progress(
    progresso
)

st.write(
    f"R$ {ultimo_mes:,.2f} / R$ {META_MENSAL:,.2f}"
)

st.divider()

# ==================================
# EVOLUÇÃO
# ==================================

col1, col2 = st.columns(2)

with col1:

    st.subheader(
        "Proventos por mês"
    )

    resumo_mes = (
        dados.groupby("Mes")
        ["Valor (R$)"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        resumo_mes,
        x="Mes",
        y="Valor (R$)",
        text_auto=".2f"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    st.subheader(
        "Proventos por ano"
    )

    resumo_ano = (
        dados.groupby("Ano")
        ["Valor (R$)"]
        .sum()
        .reset_index()
    )
    resumo_ano["Ano"] = ( resumo_ano["Ano"] .astype(str) )

    fig = px.bar(
        resumo_ano,
        x="Ano",
        y="Valor (R$)",
        text_auto=".2f"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()


# ==================================
# ACUMULADO
# ==================================

st.subheader(
    "📈 Evolução Acumulada"
)

acumulado = (
    dados.groupby("Mes")
    ["Valor (R$)"]
    .sum()
    .reset_index()
)

acumulado = acumulado.sort_values("Mes")

acumulado["Acumulado"] = (
    acumulado["Valor (R$)"]
    .cumsum()
)

fig = px.line(
    acumulado,
    x="Mes",
    y="Acumulado",
    markers=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)





# ==================================
# AÇÕES X FIIS
# ==================================

st.subheader(
    "📊 Ações x FIIs por mês")

st.subheader(
    "🥧 Distribuição Ações x FIIs"
)

pizza = (
    dados.groupby(
        "Tipo_Provento"
    )["Valor (R$)"]
    .sum()
    .reset_index()
)

fig_pizza = px.pie(
    pizza,
    names="Tipo_Provento",
    values="Valor (R$)",
    hole=0.4
)

st.plotly_chart(
    fig_pizza,
    use_container_width=True
)




resumo_tipo = (
    dados.groupby(
        ["Mes", "Tipo_Provento"]
    )["Valor (R$)"]
    .sum()
    .reset_index()
)

st.write("DEBUG RESUMO TIPO")
st.dataframe(resumo_tipo)

resumo_tipo["Mes"] = (
    resumo_tipo["Mes"]
    .astype(str)
)

fig = px.bar(
    resumo_tipo,
    x="Mes",
    y="Valor (R$)",
    color="Tipo_Provento",
    barmode="group",
    text_auto=".2f"
)

fig.update_xaxes(
    type="category"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ==================================
# RANKING
# ==================================

st.subheader(
    "🏆 Ranking de Ativos"
)

ranking = (
    dados.groupby("Ativo")
    ["Valor (R$)"]
    .sum()
    .reset_index()
    .sort_values(
        "Valor (R$)",
        ascending=False
    )
)

st.dataframe(
    ranking,
    use_container_width=True
)

fig = px.bar(
    ranking,
    x="Ativo",
    y="Valor (R$)",
    text_auto=".2f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ==================================
# LANÇAMENTOS
# ==================================

st.subheader(
    "📋 Lançamentos"
)

st.dataframe(
    dados.astype(str),
    use_container_width=True
)

st.caption(
    f"Total de registros: {len(dados)}"
)


st.markdown("<br><br><br>", unsafe_allow_html=True)

st.markdown(
    "<p style='text-align:center; color:gray; font-size:0.875rem;'>******* By Soto Company *******</p>",
    unsafe_allow_html=True
)