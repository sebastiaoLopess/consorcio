import streamlit as st
from database import validar_usuario

def main():  # Função principal da página
    st.title("Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password", key="senha_login")

    if st.button("Entrar"):
        if validar_usuario(usuario, senha):
            st.session_state.autenticado = True
            st.session_state.usuario = usuario
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos!")