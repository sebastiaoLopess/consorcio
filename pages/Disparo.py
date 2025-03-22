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

st.set_page_config(
    page_title="Szabo Consorcios",
    page_icon="📊",
    layout="wide",  # Habilita o Wide Mode
    initial_sidebar_state="expanded"  # Opções: "expanded", "collapsed", "auto"
)

def main():

    url = "https://api.w-api.app/v1/message/send-text?instanceId=1S7TKN-BDR9ZI-3F420Z"

    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer jHIIJfFjt3Im5RaW3HdoJ1HPEZkCbJnqt'
    }

    # cota, modelo, amortizado, falta_quitar

    def disparoWhats(numero, nome, valor,modelo,assembleia):

        data_formatada = datetime.strptime(assembleia, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")

        mensagem = f"Ola {nome}, tudo bem com você? 😁 Temos uma proposta imperdível para você, com apenas R$ {valor} você quita o seu consórcio e contempla a sua {modelo}, aproveita que a sua próxima assembleia será no dia {data_formatada}"

        payload = json.dumps({
        "phone": numero,
        "message": mensagem,
        "delayMessage": 15
        })


        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

    carteira = pd.read_excel("carteiraAtiva.xlsx") # carrega o dado
    carteira["quantidade"] = 1

    def classificar(amortizado):
        if amortizado >= 80 and amortizado <= 200:
            return "ENTRE 80% E 100%"
        elif amortizado >= 50 and amortizado <= 79:
            return "ENTRE 50% E 79%"
        elif amortizado >= 30 and amortizado <= 49:
            return "ENTRE 30% E 49%"
        else:
            return "ATÉ 29%"

    carteira["classificacao_amortizado"] = carteira["% Amortizado"].apply(classificar)

    # ----- SIDEBAR ----- #

    lojas = carteira["loja"].unique() 
    loja = st.sidebar.selectbox("Loja", lojas)
    status_unique = carteira["Status Contrato"].unique()
    status = st.sidebar.selectbox("Status", status_unique)
    classificacoes = carteira["classificacao_amortizado"].unique()
    classificacao = st.sidebar.selectbox("Classificação de Amortização", classificacoes)
    modelos = carteira["Modelo"].unique()
    modelo = st.sidebar.selectbox("Modelo", modelos)

    # ----- TRATAMENTO DE DADOS ---- #

    carteira["% Amortizado real"] = carteira["% Amortizado"] / 100

    carteira["% Quitação real"] = carteira["% Quitação"] / 100

    carteira["valor_total_cota"] = ((carteira["Valor para Quitação"] * carteira["% Amortizado"]) / carteira["% Quitação"])

    carteira["valor_total_cota"] = carteira["valor_total_cota"].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    carteira["Telefone_disparo"] = carteira["Telefone"].str.replace(r"[^\d]", "", regex=True)  # Remove caracteres não numéricos
    carteira["Telefone_disparo"] = "55" + carteira["Telefone_disparo"]

    #carteira["Valor para Quitação"] = carteira["Valor para Quitação"].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    carteira_loja = carteira[carteira["loja"] == loja]

    carteira_normal = carteira[carteira["Status Contrato"] == status]

    carteira_normal = carteira_normal[carteira_normal["classificacao_amortizado"] == classificacao]

    carteira_normal = carteira_normal[carteira_normal["Modelo"] == modelo]

    assembleias_agg = carteira_normal.groupby("Próxima Assembleia")["quantidade"].sum().reset_index()



    #assembleias_agg_categorias = carteira_normal.groupby(["Próxima Assembleia", "Grupo"]).agg({"Maior Lance": "mean", "Menor Lance": "mean"}).reset_index()

    categorias_agg = carteira_normal.groupby("classificacao_amortizado")["quantidade"].sum().reset_index()

    categorias_agg_quitacao = carteira_normal.groupby("classificacao_amortizado")["Valor para Quitação"].mean().reset_index()

    categorias_agg_quitacao["Valor para Quitação"] = categorias_agg_quitacao["Valor para Quitação"].apply(lambda x: f"{x:,.0f}")

    cols = ['Cliente','Telefone','Grupo','Cota', 'R', 'D','% Amortizado', '% Quitação', 'Valor para Quitação', 	'Maior Lance','Menor Lance','Modelo','UF', 'Município','Próxima Assembleia','classificacao_amortizado','Telefone_disparo']

    tabela = carteira_normal[cols]

    modelo_categoria_agg = carteira_normal.groupby(["Modelo", "classificacao_amortizado"])["quantidade"].sum().reset_index()


    # ---- CRIAÇÃO DE MEDIDAS ---- #

    total_carteira = carteira_normal["quantidade"].sum()

    valor_carteira = carteira_normal["Valor para Quitação"].sum()

    # ---- DASHBOARD ---- #

    #modelo_categoria_agg = carteira_normal.groupby(["Modelo", "classificacao_amortizado"])["quantidade"].sum().reset_index()

    st.header("Criação de Oportunidades", divider="gray")

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
                <h4>💰 Valor Total para Quitação</h4>
                <p style="font-size: 22px; font-weight: bold; color: #007bff;">R$ {valor_carteira:,.0f}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <style>
            .tabela-container {
                width: 100%;
                border-radius: 8px;
                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                border: 1px solid #ddd;
                font-size: 10px;
            }
            .tabela-header, .tabela-row {
                display: grid;
                grid-template-columns: 1.5fr 1.5fr 1fr 1fr 1fr 1.5fr 1fr 1fr; /* Ajusta a largura das colunas */
                align-items: center;
                padding: 8px;
            }
            .tabela-header {
                background-color: #008CBA;
                color: white;
                font-weight: bold;
                text-align: center;
            }
            .tabela-row {
                border-bottom: 1px solid #ddd;
            }
            .tabela-row:last-child {
                border-bottom: none;
            }
            .tabela-col {
                text-align: left;
                padding: 6px;
            }
            .tabela-col-btn {
                text-align: center;
            }
            .botao-enviar {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 6px 10px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 10px;
            }
            .botao-enviar:hover {
                background-color: #218838;
            }

        </style>
        """,
        unsafe_allow_html=True
    )

    # Criando a tabela com o cabeçalho corretamente alinhado
    st.markdown('<div class="tabela-container">', unsafe_allow_html=True)

    # Cabeçalho fixo corretamente alinhado
    st.markdown(
        '<div class="tabela-header">'
        '<div class="tabela-col">Cliente</div>'
        '<div class="tabela-col">Telefone</div>'
        '<div class="tabela-col">Grupo</div>'
        '<div class="tabela-col">Cota</div>'
        '<div class="tabela-col">% Amortizado</div>'
        '<div class="tabela-col">Valor Quitação</div>'
        '<div class="tabela-col">Modelo</div>'
        '<div class="tabela-col-btn">Ação</div>'
        '</div>',
        unsafe_allow_html=True
    )



    # Criar a tabela com botões para cada linha
    for index, row in tabela.iterrows():
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1,1,1,1,1,1,1,1])  # Ajusta o layout das colunas
        
        with col1:
            #st.write(row["Cliente"])
            st.markdown(f'<div class="tabela-row">{row["Cliente"]}</div>', unsafe_allow_html=True)
        
        with col2:
            #st.write(row["Telefone"])
            st.markdown(f'<div class="tabela-row">{row["Telefone"]}</div>', unsafe_allow_html=True)

        with col3:
            #st.write(row["Telefone"])
            st.markdown(f'<div class="tabela-row">{row["Grupo"]}</div>', unsafe_allow_html=True)

        with col4:
            #st.write(row["Telefone"])
            st.markdown(f'<div class="tabela-row">{row["Cota"]}</div>', unsafe_allow_html=True)

        with col5:
            #st.write(row["Telefone"])
            st.markdown(f'<div class="tabela-row">{row["% Amortizado"]}</div>', unsafe_allow_html=True)

        with col6:
            #st.write(row["Telefone"])
            st.markdown(f'<div class="tabela-row">{row["Valor para Quitação"]}</div>', unsafe_allow_html=True)

        with col7:
            #st.write(row["Telefone"])
            st.markdown(f'<div class="tabela-row">{row["Modelo"]}</div>', unsafe_allow_html=True)
                
        
        with col8:
            if st.button(f"Enviar Whatsapp", key=row["Cliente"]):  # Cada botão tem um ID único
                disparoWhats(str(row['Telefone_disparo']),str(row['Cliente']),str(row['Valor para Quitação']),str(row['Modelo']),str(row['Próxima Assembleia']))
                st.success(f"Mensagem enviada para {row['Cliente']} com sucesso!")


if __name__ == "__main__":
    main()