import matplotlib.pyplot as plt

def desenhar_grafo(grafo, posicoes_nos):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.clear()

    # Desenha as arestas como linhas simples
    for no, vizinhos in grafo.items():
        for vizinho, peso in vizinhos.items():
            if no < vizinho:
                pos_no = posicoes_nos[no]
                pos_vizinho = posicoes_nos[vizinho]
                ax.plot([pos_no[0], pos_vizinho[0]], [pos_no[1], pos_vizinho[1]], color='gray', zorder=1)
                ax.text(
                    (pos_no[0] + pos_vizinho[0]) / 2, 
                    (pos_no[1] + pos_vizinho[1]) / 2, 
                    str(peso), color="black", ha='center', va='center',
                    bbox=dict(facecolor='white', edgecolor='none', pad=1)
                )

    # Desenha os nós
    if posicoes_nos:
        x, y = zip(*posicoes_nos.values())
        ax.scatter(x, y, s=600, c='#007bff', edgecolors='black', zorder=2)
        for no, pos in posicoes_nos.items():
            ax.text(pos[0], pos[1], str(no), ha='center', va='center', color='white', weight='bold')

    ax.set_xticks([]); ax.set_yticks([]); plt.tight_layout()
    return fig