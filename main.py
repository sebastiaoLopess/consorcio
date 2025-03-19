import streamlit as st
import importlib

st.set_page_config(
    page_title="Szabo Consorcios",
    page_icon="📊",
    layout="wide",  # Habilita o Wide Mode
    initial_sidebar_state="expanded"  # Opções: "expanded", "collapsed", "auto"
)

# Criar sessão para autenticação
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# Páginas disponíveis no sistema
paginas_publicas = {
    "Login": "Login",
    "Registrar": "Registrar"
}
paginas_privadas = {
    "Home": "Home",
    "Disparo": "Disparo",
    "Vendas": "VendasCotas"
}

# Escolher quais páginas aparecem no menu
if st.session_state.autenticado:
    paginas_disponiveis = paginas_privadas
else:
    paginas_disponiveis = paginas_publicas

pagina = st.sidebar.selectbox("Menu", list(paginas_disponiveis.keys()))

# Importar dinamicamente a página correta
modulo = importlib.import_module(paginas_disponiveis[pagina])
modulo.main()  # Agora a função main() existe

# Botão de Logout para usuários logados
if st.session_state.autenticado:
    if st.sidebar.button("Logout"):
        st.session_state.autenticado = False
        st.experimental_rerun()