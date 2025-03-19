import streamlit as st
from database import registrar_usuario

def main():
    st.title("Registrar Usuário")

    nome = st.text_input("Nome Completo")
    novo_usuario = st.text_input("Usuário")
    nova_senha = st.text_input("Senha", type="password", key="senha_registro")
    confirmar_senha = st.text_input("Confirme a Senha", type="password", key="conf_senha")

    if st.button("Registrar"):
        if nova_senha != confirmar_senha:
            st.error("As senhas não coincidem!")
        elif not nome or not novo_usuario or not nova_senha:
            st.error("Todos os campos são obrigatórios!")
        else:
            sucesso = registrar_usuario(nome, novo_usuario, nova_senha)
            if sucesso:
                st.success("Usuário registrado com sucesso!")
            else:
                st.error("Usuário já existe!")