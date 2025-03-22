import streamlit.components.v1 as components
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import requests
import json
from datetime import datetime
import plotly.graph_objects as go

st.set_page_config(
    page_title="Szabo Consorcios",
    page_icon="📊",
    layout="wide",  # Habilita o Wide Mode
    initial_sidebar_state="expanded"  # Opções: "expanded", "collapsed", "auto"
)

def main():

    vendas = pd.read_excel("equipe_de_vendas.xlsx") # carrega o dado
    vendas["quantidade"] = 1

    metas = pd.read_excel("metas_lojas.xlsx")

    # ----- SIDEBAR ----- #

    # ----- TRATAMENTO DE DADOS ---- #

    # tratamento base vendas
    vendas["ano"] = vendas["Data_da_Venda"].dt.year
    vendas["mes"] = vendas["Data_da_Venda"].dt.month
    vendas["codigoEmpresa"] = vendas["codigoEmpresa"].astype(str)
    vendas["ano_mes"] = vendas["ano"].astype(str) + "-" + vendas["mes"].astype(str).str.zfill(2)
    df_agg_ano_emp = vendas.groupby(["ano_mes","codigoEmpresa"])["quantidade"].sum().reset_index()
    df_agg = vendas.groupby("Status")["quantidade"].sum().reset_index()
    df_agg = df_agg.sort_values(by="quantidade")
    df_agg_ano = vendas.groupby("ano_mes")["quantidade"].sum().reset_index()
    df_agg_vendedor = vendas.groupby("Nome_Vendedor")["quantidade"].sum().reset_index()
    df_agg_vendedor = df_agg_vendedor.sort_values(by="quantidade")
    df_agg_modelo = vendas.groupby("Modelo")["quantidade"].sum().reset_index()
    df_agg_modelo = df_agg_modelo.sort_values(by="quantidade")


    # tratamento base metas
    metas["ano_mes"] = metas["ano"].astype(str) + "-" + metas["mes"].astype(str).str.zfill(2)
    metas["empresa"] = metas["empresa"].astype(str)
    metas = metas[["ano_mes","empresa","meta"]]

    #base unica planejamento
    #df_final_metas = df_agg_ano_emp.merge(metas, left_on=["codigoEmpresa", "ano-mes"], right_on=["empresa", "ano_mes"])
    df_final_metas = df_agg_ano_emp.merge(metas, how = "left", on = "ano_mes")
    df_final_metas["realXorcado"] = (df_final_metas["quantidade"] / df_final_metas["meta"]) * 100

    
    # ---- CRIAÇÃO DE MEDIDAS ---- #




    # ---- DASHBOARD ---- #

    fig = px.line(df_final_metas, 
            x="ano_mes", 
            y=["quantidade", "meta"], 
            labels={"value": "Quantidade", "variable": "Legenda"}, 
            title="Comparação: Realizado vs Meta")
    st.plotly_chart(fig, use_container_width=True)



    st.header("Vendas de Cotas", divider="gray")


    fig_vendedor = px.bar(df_agg_vendedor, x="quantidade", y="Nome_Vendedor")

    fig_vendedor.update_traces(text=df_agg_modelo["quantidade"],  # Adiciona os números nas barras
                        textposition="inside",  # Posiciona os números dentro da barra
                        textfont=dict(family="Arial", size=12, color="white")) 

    fig_vendedor.update_layout(
        title="Quantidade de cotas por Modelo",
        title_font=dict(family="Arial", size=10, color="black"),
        height=600  
    )

    fig_vendedor.update_layout(
        yaxis=dict(categoryorder="total ascending"),  # 🔥 Ordena os vendedores pelo total de vendas
        height=800,  # 🔥 Aumenta a altura para caber todos os vendedores
        margin=dict(l=150, r=20, t=50, b=40),  # 🔥 Aumenta margem esquerda para nomes longos
)

    st.plotly_chart(fig_vendedor,use_container_width=True)

    fig_status = px.bar(df_agg, x="Status", y="quantidade")

    st.plotly_chart(fig_status,use_container_width=True)



if __name__ == "__main__":
    main()





