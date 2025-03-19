import streamlit.components.v1 as components
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import os

def main():

    vendas = pd.read_excel("equipe_de_vendas.xlsx")
    carteira = pd.read_excel("carteiraAtiva.xlsx") # carrega o dado
    carteira["quantidade"] = 1


    # ----- SIDEBAR ----- #

    lojas = carteira["loja"].unique() 
    loja = st.sidebar.selectbox("Loja", lojas)
    status_unique = carteira["Status Contrato"].unique()
    status = st.sidebar.selectbox("Status", status_unique)


    # ----- TRATAMENTO DE DADOS ---- #

    carteira_loja = carteira[carteira["loja"] == loja]

    carteira_filrada_status = carteira_loja[carteira_loja["Status Contrato"] == status]

    df_agg = carteira_loja.groupby("Status Contrato")["quantidade"].sum().reset_index()

    df_agg2 = carteira_loja.groupby("Status Contrato")["quantidade"].sum().reset_index()

    df_agg_modelo = carteira_loja.groupby("Modelo")["quantidade"].sum().reset_index()
    df_agg_modelo = df_agg_modelo.sort_values(by="quantidade")

    df_agg_tipo = carteira_loja.groupby("Tipo de Contrato")["quantidade"].sum().reset_index()
    df_agg_tipo = df_agg_tipo.sort_values(by="quantidade")

    resultado = carteira_loja.groupby("Modelo").agg({
            "quantidade": "sum"
        }).reset_index()

    resultado = resultado.sort_values(by="quantidade", ascending=False)


    # ---- NOVAS COLUNAS ---- #

    carteira["% Amortizado real"] = carteira["% Amortizado"] / 100

    carteira["% Quitação real"] = carteira["% Quitação"] / 100

    carteira["valor_total_cota"] = ((carteira["Valor para Quitação"] * carteira["% Amortizado"]) / carteira["% Quitação"])

    carteira["valor_total_cota"] = carteira["valor_total_cota"].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    resultado["Prospecção"] = (resultado["quantidade"] * 0.24).round().astype(int)
    resultado["Comtemplados"] = (resultado["Prospecção"] * 0.4).round().astype(int)
    resultado["Obetivo"] = (resultado["Comtemplados"] * 0.5).round().astype(int)


    # ---- CRIAÇÃO DE MEDIDAS ---- #

    total_carteira = carteira_loja["quantidade"].sum()

    valor_carteira = carteira_loja["Valor para Quitação"].sum()

    # ---- DASHBOARD ---- #

    st.header("🏍 Analise da Carteira Ativa", divider="gray")

    col3, col4 = st.columns(2)


    with col3:
        st.markdown(
            f"""
            <div style="padding: 15px; border-radius: 10px; background-color: #f0f2f6; 
                        box-shadow: 2px 2px 10px rgba(0,0,0,0.1); text-align: center;">
                <h4>📑 Quantidade de Cotas</h4>
                <p style="font-size: 22px; font-weight: bold; color: #007bff;">{total_carteira:,.0f}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div style="padding: 15px; border-radius: 10px; background-color: #f0f2f6; 
                        box-shadow: 2px 2px 10px rgba(0,0,0,0.1); text-align: center;">
                <h4>💰 Valor Total das Cotas</h4>
                <p style="font-size: 22px; font-weight: bold; color: #007bff;">R$ {valor_carteira:,.0f}</p>
            </div>
            """,
            unsafe_allow_html=True
        )


    col1, col2 = st.columns(2)

    with col1:

        fig2 = px.bar(df_agg, x="Status Contrato", y="quantidade", color="Status Contrato")
        fig2.update_layout(
            title="Quantidade de cotas por Status",
            title_font=dict(family="Arial", size=10, color="black"),
            showlegend=False  # Desabilita a legenda
        )
        st.plotly_chart(fig2)

    with col2:

        fig = px.pie(df_agg2, names="Status Contrato", values="quantidade")
        fig.update_layout(showlegend=True)
        fig.update_layout(
            title="Distribuição das cotas por Status",
            title_font=dict(family="Arial", size=10, color="black"),
            legend=dict(
                x=0.02,  # Mais à esquerda
                y=0.98,  # Mais próximo do topo
                bgcolor="rgba(255,255,255,0.6)"  # Fundo branco semi-transparente para melhor visibilidade
                )
        )
        st.plotly_chart(fig)

    col5, col6 = st.columns([1,1])

    with col5:

        fig_modelos = px.bar(df_agg_modelo, x="quantidade", y="Modelo")

        fig_modelos.update_traces(text=df_agg_modelo["quantidade"],  # Adiciona os números nas barras
                            textposition="inside",  # Posiciona os números dentro da barra
                            textfont=dict(family="Arial", size=12, color="white")) 

        fig_modelos.update_layout(
            title="Quantidade de cotas por Modelo",
            title_font=dict(family="Arial", size=10, color="black"),
            height=600  
        )

        st.plotly_chart(fig_modelos)

    with col6:

        fig_modelo_pie = px.pie(df_agg_tipo, names="Tipo de Contrato", values="quantidade",hole=.3)
        fig_modelo_pie.update_layout(showlegend=True)
        fig_modelo_pie.update_layout(
            title="Distribuição das cotas por Tipo de cota",
            title_font=dict(family="Arial", size=10, color="black"),
            legend=dict(
                x=0.08,  # Mais à esquerda
                y=1,  # Mais próximo do topo
                bgcolor="rgba(255,255,255,0.6)"  # Fundo branco semi-transparente para melhor visibilidade
                )
        )
        st.plotly_chart(fig_modelo_pie)

    st.header("🎯 Objetivos", divider="gray")

    st.text("")

    col1, col2 = st.columns([1, 1])  # 3 partes para a tabela, 1 parte para as premissas

    # Exibindo a tabela na primeira coluna
    with col1:
        st.write("### Tabela de Objetivos")
        st.dataframe(resultado)

    # Exibindo as premissas de cálculo na segunda coluna
    with col2:
        st.write("### Premissas de Cálculo")
        st.markdown("""
        - **Prospecção** = 24% do Total de Cotas Ativas
        - **Comtemplados** = 40% do Total de Prospecção
        - **Objetivo** = 50% do Total de Contemplados
        """)

if __name__ == "__main__":
    main()

