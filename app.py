import streamlit as st
from graph_drawing import desenhar_grafo
from example_graphs import EXAMPLE_1

# Inicializa o estado da aplicação com o grafo de exemplo
if 'grafo' not in st.session_state:
    st.session_state.grafo = EXAMPLE_1["grafo"]
    st.session_state.posicoes_nos = EXAMPLE_1["posicoes"]

# Configuração da página
st.set_page_config(layout="wide")
st.title("Visualizador de Dijkstra")

# Layout principal
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Visualização do Grafo")
    if st.session_state.grafo:
        # Chama a função de desenho e exibe a figura
        figura = desenhar_grafo(st.session_state.grafo, st.session_state.posicoes_nos)
        st.pyplot(figura)

with col2:
    st.header("Controles")
    st.info("Interface de animação será implementada em breve.")