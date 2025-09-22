import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def desenhar_grafo(grafo, posicoes_nos, estado_algoritmo, caminho_final):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.clear()

    # Dicionário de cores para a legenda e para os elementos do grafo
    cores = {'Padrão': '#007bff', 'Visitado': '#dc3545', 'Atual': '#ffc107', 'Fronteira': '#17a2b8', 'Caminho Final': '#28a745'}
    
    # Desenha as arestas
    for no, vizinhos in grafo.items():
        for vizinho, peso in vizinhos.items():
            # Evita desenhar arestas duplicadas
            if no < vizinho:
                pos_no = posicoes_nos[no]
                pos_vizinho = posicoes_nos[vizinho]
                
                eh_caminho = (no, vizinho) in caminho_final or (vizinho, no) in caminho_final
                cor_aresta = cores['Caminho Final'] if eh_caminho else 'gray'
                largura_linha = 2.5 if eh_caminho else 1.5
                
                ax.plot([pos_no[0], pos_vizinho[0]], [pos_no[1], pos_vizinho[1]], color=cor_aresta, linewidth=largura_linha, zorder=1)
                ax.text((pos_no[0] + pos_vizinho[0]) / 2, (pos_no[1] + pos_vizinho[1]) / 2, str(peso), color="black", ha='center', va='center',
                        bbox=dict(facecolor='white', edgecolor='none', pad=1))

    # Desenha os nós
    if posicoes_nos:
        x, y = zip(*posicoes_nos.values())
        cores_dos_nos = []
        for no in posicoes_nos.keys():
            cor = cores['Padrão']
            if estado_algoritmo:
                if no == estado_algoritmo.get('no_atual'): cor = cores['Atual']
                elif no in estado_algoritmo.get('visitados', set()): cor = cores['Visitado']
                elif no in estado_algoritmo.get('fronteira', set()): cor = cores['Fronteira']
            if caminho_final and no in [item for tupla in caminho_final for item in tupla]:
                cor = cores['Caminho Final']
            cores_dos_nos.append(cor)
            
        ax.scatter(x, y, s=600, c=cores_dos_nos, edgecolors='black', zorder=2)
        for no, pos in posicoes_nos.items():
            ax.text(pos[0], pos[1], str(no), ha='center', va='center', color='white', weight='bold', fontsize=12)

    # Legenda de cores
    patches = [mpatches.Patch(color=color, label=label) for label, color in cores.items()]
    ax.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.set_xticks([]); ax.set_yticks([]); plt.tight_layout()
    
    return fig