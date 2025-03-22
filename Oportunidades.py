import streamlit.components.v1 as components
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff

carteira = pd.read_excel("carteiraAtiva.xlsx") # carrega o dado
carteira["quantidade"] = 1

# ----- SIDEBAR ----- #

lojas = carteira["loja"].unique() 
loja = st.sidebar.selectbox("Loja", lojas)
status_unique = carteira["Status Contrato"].unique()
status = st.sidebar.selectbox("Status", status_unique)

# ----- TRATAMENTO DE DADOS ---- #

carteira["% Amortizado real"] = carteira["% Amortizado"] / 100

carteira["% Quitação real"] = carteira["% Quitação"] / 100

carteira["valor_total_cota"] = ((carteira["Valor para Quitação"] * carteira["% Amortizado"]) / carteira["% Quitação"])

carteira["valor_total_cota"] = carteira["valor_total_cota"].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

#carteira["Valor para Quitação"] = carteira["Valor para Quitação"].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

carteira_loja = carteira[carteira["loja"] == loja]

carteira_normal = carteira[carteira["Status Contrato"] == status]

assembleias_agg = carteira_normal.groupby("Próxima Assembleia")["quantidade"].sum().reset_index()


def classificar(amortizado):
    if amortizado >= 80 and amortizado <= 200:
        return "ENTRE 80% E 100%"
    elif amortizado >= 50 and amortizado <= 79:
        return "ENTRE 50% E 79%"
    elif amortizado >= 30 and amortizado <= 49:
        return "ENTRE 30% E 49%"
    else:
        return "ATÉ 29%"

carteira_normal["classificacao_amortizado"] = carteira_normal["% Amortizado"].apply(classificar)

#assembleias_agg_categorias = carteira_normal.groupby(["Próxima Assembleia", "Grupo"]).agg({"Maior Lance": "mean", "Menor Lance": "mean"}).reset_index()

categorias_agg = carteira_normal.groupby("classificacao_amortizado")["quantidade"].sum().reset_index()

categorias_agg_quitacao = carteira_normal.groupby("classificacao_amortizado")["Valor para Quitação"].mean().reset_index()

categorias_agg_quitacao["Valor para Quitação"] = categorias_agg_quitacao["Valor para Quitação"].apply(lambda x: f"{x:,.0f}")

cols = ['Cliente','Telefone','Grupo','Cota', 'R', 'D','% Amortizado', '% Quitação', 'Valor para Quitação', 	'Maior Lance','Menor Lance','Modelo','UF', 'Município','Próxima Assembleia','classificacao_amortizado']

tabela = carteira_normal[cols]

modelo_categoria_agg = carteira_normal.groupby(["Modelo", "classificacao_amortizado"])["quantidade"].sum().reset_index()


# ---- CRIAÇÃO DE MEDIDAS ---- #

total_carteira = carteira_loja["quantidade"].sum()

valor_carteira = carteira_loja["Valor para Quitação"].sum()

# ---- DASHBOARD ---- #


st.header("OPORTUNIDADE DE COTEMPLAÇÃO ✅", divider="gray")

col3, col4 = st.columns([1,1])

with col3:

    fig_funil_categoria = px.funnel(categorias_agg, x="quantidade", y="classificacao_amortizado", title="Gráfico de Funil")

    st.plotly_chart(fig_funil_categoria, use_container_width=True)

with col4:

    fig_categoria_quitacao = px.bar(categorias_agg_quitacao, x="classificacao_amortizado", y="Valor para Quitação",text="Valor para Quitação",title="Média de quitação por Categoria")

    fig_categoria_quitacao.update_traces(textposition="inside")  

    st.plotly_chart(fig_categoria_quitacao,use_container_width=True)


fig_sca = px.scatter(modelo_categoria_agg, x="classificacao_amortizado", y="Modelo", size="quantidade", title="Dispersão entre Quantidade e Outra Variável")

st.plotly_chart(fig_sca,use_container_width=True)

#modelo_categoria_agg = carteira_normal.groupby(["Modelo", "classificacao_amortizado"])["quantidade"].sum().reset_index()

st.dataframe(tabela)









