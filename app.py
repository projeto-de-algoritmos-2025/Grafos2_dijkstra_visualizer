import streamlit as st
from dijkstra_logic import dijkstra_gerar_passos
from graph_drawing import desenhar_grafo
from example_graphs import get_example

# --- Inicialização do Estado da Aplicação ---
if 'grafo' not in st.session_state:
    st.session_state.grafo = {}
    st.session_state.posicoes_nos = {}
    st.session_state.passo_atual = -1
    st.session_state.no_final = None
    st.session_state.proximo_no_id = 0

# --- Interface do Usuário (UI) ---
st.set_page_config(layout="wide")
st.title("Visualizador de Dijkstra para Grafos Direcionados")

# --- BARRA LATERAL COM ABAS ---
with st.sidebar:
    st.header("Controles Principais")

    if st.button("Carregar Grafo de Exemplo"):
        exemplo = get_example(2)
        st.session_state.grafo = exemplo["grafo"]
        st.session_state.posicoes_nos = exemplo["posicoes"]
        st.session_state.proximo_no_id = exemplo["proximo_id"]
        st.session_state.passo_atual = -1
        st.rerun()

    if st.button("🧹 Limpar Tudo"):
        keys_to_clear = list(st.session_state.keys())
        for key in keys_to_clear:
            del st.session_state[key]
        st.rerun()
    
    st.divider()

    tab_animacao, tab_edicao = st.tabs(["▶️ Animação", "✏️ Editar Grafo"])

    with tab_animacao:
        st.header("Opções de Animação")
        if st.session_state.grafo:
            lista_de_nos = sorted(list(st.session_state.grafo.keys()))
            no_inicial = st.selectbox("Nó de Partida", options=lista_de_nos, key="anim_no_inicial")
            no_final = st.selectbox("Nó de Destino", options=lista_de_nos, key="anim_no_final", index=len(lista_de_nos)-1 if lista_de_nos else 0)
            if st.button("Iniciar Animação"):
                if no_inicial in st.session_state.grafo:
                    st.session_state.passos_dijkstra = dijkstra_gerar_passos(st.session_state.grafo, no_inicial)
                    st.session_state.no_final = no_final
                    st.session_state.passo_atual = 0
                    st.rerun()
                else: st.error("O nó de partida selecionado não existe no grafo.")
            if st.button("Próximo Passo"):
                if 'passos_dijkstra' in st.session_state and 0 <= st.session_state.passo_atual < len(st.session_state.passos_dijkstra) - 1:
                    st.session_state.passo_atual += 1
                    st.rerun()
            if st.button("Passo Anterior"):
                if 'passos_dijkstra' in st.session_state and 1 <= st.session_state.passo_atual < len(st.session_state.passos_dijkstra):
                    st.session_state.passo_atual -= 1
                    st.rerun()
            if st.button("Pular para Passo Final"):
                if 'passos_dijkstra' in st.session_state:
                    st.session_state.passo_atual = len(st.session_state.passos_dijkstra) - 1
                    st.rerun()
        else: st.info("Crie um grafo na aba 'Editar Grafo' ou carregue um exemplo.")
            
    with tab_edicao:
        st.header("Montar o Grafo")
        with st.form("form_adicionar_no", clear_on_submit=True):
            st.write("**Adicionar Novo Nó**")
            novo_no_id = st.number_input("ID do Nó", min_value=0, value=st.session_state.proximo_no_id, step=1)
            c1, c2 = st.columns(2)
            pos_x = c1.number_input("Posição X", value=float(st.session_state.proximo_no_id))
            pos_y = c2.number_input("Posição Y", value=float(st.session_state.proximo_no_id % 2))
            if st.form_submit_button("Adicionar Nó"):
                if novo_no_id not in st.session_state.grafo:
                    st.session_state.grafo[novo_no_id] = {}
                    st.session_state.posicoes_nos[novo_no_id] = (pos_x, pos_y)
                    st.session_state.proximo_no_id = max(st.session_state.proximo_no_id, novo_no_id) + 1
                    st.rerun()
                else: st.warning(f"O nó com ID {novo_no_id} já existe.")
        if len(st.session_state.grafo) >= 2:
            with st.form("form_adicionar_aresta"):
                st.write("**Adicionar Nova Aresta (A → B)**")
                lista_nos = sorted(list(st.session_state.grafo.keys()))
                c1, c2 = st.columns(2)
                no_de = c1.selectbox("De (A):", options=lista_nos)
                no_para = c2.selectbox("Para (B):", options=lista_nos)
                peso = st.number_input("Peso", min_value=1, value=1, step=1)
                if st.form_submit_button("Adicionar Aresta"):
                    if no_de != no_para:
                        st.session_state.grafo[no_de][no_para] = peso
                        st.rerun()
                    else: st.warning("Selecione dois nós diferentes.")
        if st.session_state.grafo:
            st.divider()
            st.write("**Editar Posição de um Nó**")
            lista_nos_edit = sorted(list(st.session_state.grafo.keys()))
            no_para_editar = st.selectbox("Nó para Editar", options=lista_nos_edit, key="edit_selectbox")
            if no_para_editar is not None:
                pos_atual = st.session_state.posicoes_nos[no_para_editar]
                c1, c2 = st.columns(2)
                novo_x = c1.number_input("Nova Posição X", value=float(pos_atual[0]), key=f"x_{no_para_editar}")
                novo_y = c2.number_input("Nova Posição Y", value=float(pos_atual[1]), key=f"y_{no_para_editar}")
                if st.button("Atualizar Posição"):
                    st.session_state.posicoes_nos[no_para_editar] = (novo_x, novo_y)
                    st.rerun()

# --- ÁREA PRINCIPAL DA APLICAÇÃO ---
col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("Visualização do Grafo")
    if st.session_state.grafo:
        estado_algoritmo, caminho_final = {}, []
        if 'passos_dijkstra' in st.session_state and 0 <= st.session_state.passo_atual < len(st.session_state.passos_dijkstra):
            estado_algoritmo = st.session_state.passos_dijkstra[st.session_state.passo_atual]
            if st.session_state.passo_atual == len(st.session_state.passos_dijkstra) - 1:
                predecessores = estado_algoritmo.get('predecessores')
                no_final = st.session_state.no_final
                if predecessores and no_final is not None and predecessores.get(no_final) is not None:
                    passo = no_final
                    while passo is not None:
                        predecessor = predecessores.get(passo)
                        if predecessor is not None:
                            caminho_final.append((predecessor, passo))
                        passo = predecessor
        figura = desenhar_grafo(st.session_state.grafo, st.session_state.posicoes_nos, estado_algoritmo, caminho_final)
        st.pyplot(figura)
    else: st.info("Use a barra lateral para carregar um exemplo ou criar um novo grafo na aba 'Editar Grafo'.")

with col2:
    st.subheader("Estado do Algoritmo")
    if 'passos_dijkstra' in st.session_state and 0 <= st.session_state.passo_atual < len(st.session_state.passos_dijkstra):
        estado = st.session_state.passos_dijkstra[st.session_state.passo_atual]
        st.write(f"**Passo {st.session_state.passo_atual + 1}/{len(st.session_state.passos_dijkstra)}**")
        st.metric(label="Nó Sendo Processado", value=str(estado.get('no_atual', 'Nenhum')))
        distancias_atuais = {k: v for k, v in estado['distancias'].items() if v != float('infinity')}
        st.json(distancias_atuais, expanded=True)
        if st.session_state.passo_atual == len(st.session_state.passos_dijkstra) - 1:
            st.divider()
            no_final_selecionado = st.session_state.no_final
            distancia_final = estado['distancias'][no_final_selecionado]
            if distancia_final == float('infinity'):
                st.error(f"Não há caminho alcançável para o nó {no_final_selecionado}.")
            else: st.success(f"Custo final para o nó {no_final_selecionado}: {distancia_final}")
    elif not st.session_state.grafo:
        st.info("Aguardando a criação ou carregamento de um grafo...")
    else: st.info("Selecione os nós na aba 'Animação' e clique em 'Iniciar Animação'.")