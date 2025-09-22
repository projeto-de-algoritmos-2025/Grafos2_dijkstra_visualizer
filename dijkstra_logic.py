import heapq

def dijkstra_gerar_passos(grafo, no_inicial):
    """
    Executa o algoritmo de Dijkstra e retorna uma lista com o estado em cada passo.
    Recebe o grafo e o nó inicial como argumentos para ser uma função pura.
    """
    passos = []
    distancias = {no: float('infinity') for no in grafo}
    # Adiciona nós que podem ser destinos mas não fontes
    for no_origem in grafo:
        for no_destino in grafo[no_origem]:
            if no_destino not in distancias:
                distancias[no_destino] = float('infinity')

    if no_inicial not in distancias:
        return [] # Retorna vazio se o nó inicial não estiver no grafo

    distancias[no_inicial] = 0
    
    predecessores = {no: None for no in distancias}
    visitados, fila_prioridade = set(), [(0, no_inicial)]

    while fila_prioridade:
        distancia_atual, no_atual = heapq.heappop(fila_prioridade)
        if no_atual in visitados:
            continue
        visitados.add(no_atual)
        
        passos.append({
            'no_atual': no_atual, 'distancias': distancias.copy(), 
            'visitados': visitados.copy(), 'fronteira': {no for _, no in fila_prioridade}
        })

        if no_atual not in grafo: continue
            
        for vizinho, peso in grafo[no_atual].items():
            distancia = distancia_atual + peso
            if distancia < distancias[vizinho]:
                distancias[vizinho], predecessores[vizinho] = distancia, no_atual
                heapq.heappush(fila_prioridade, (distancia, vizinho))

    passos.append({
        'no_atual': None, 'distancias': distancias, 'visitados': visitados, 
        'fronteira': set(), 'predecessores': predecessores
    })
    return passos