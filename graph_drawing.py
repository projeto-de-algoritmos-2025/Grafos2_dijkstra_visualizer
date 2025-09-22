import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def desenhar_grafo(grafo, posicoes_nos, estado_algoritmo, caminho_final):
    """
    Desenha o grafo na tela, usando setas para representar as arestas direcionadas.
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.clear()

    cores = {'Padrão': '#007bff', 'Visitado': '#dc3545', 'Atual': '#ffc107', 'Fronteira': '#17a2b8', 'Caminho Final': '#28a745'}
    
    # --- MUDANÇA PRINCIPAL: DESENHA SETAS ---
    for no, vizinhos in grafo.items():
        for vizinho, peso in vizinhos.items():
            pos_no = posicoes_nos[no]
            pos_vizinho = posicoes_nos[vizinho]
            
            eh_caminho = (no, vizinho) in caminho_final
            cor_aresta = cores['Caminho Final'] if eh_caminho else 'gray'
            largura_linha = 1.5 if eh_caminho else 1.0

            # Usamos ax.annotate para desenhar setas em vez de ax.plot
            ax.annotate("",
                        xy=pos_vizinho, xycoords='data',
                        xytext=pos_no, textcoords='data',
                        arrowprops=dict(arrowstyle="->", color=cor_aresta,
                                        shrinkA=15, shrinkB=15, # Encolhe a seta para não sobrepor os nós
                                        linewidth=largura_linha,
                                        connectionstyle="arc3,rad=0.1")) # Leve curvatura para arestas de volta
            
            # Desenha o peso no meio da aresta
            ax.text((pos_no[0] * 0.6 + pos_vizinho[0] * 0.4),
                    (pos_no[1] * 0.6 + pos_vizinho[1] * 0.4),
                    str(peso), color="black", fontsize=10, ha='center', va='center',
                    bbox=dict(facecolor='white', edgecolor='none', pad=1))

    # Desenha os nós (lógica inalterada)
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
            ax.text(pos[0], pos[1], str(no), ha='center', va='center', color='white', weight='bold', fontsize=12)

    patches = [mpatches.Patch(color=color, label=label) for label, color in cores.items()]
    ax.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.set_xticks([]); ax.set_yticks([]); plt.tight_layout()
    
    
    return fig