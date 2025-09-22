import heapq

def dijkstra_gerar_passos(grafo, no_inicial):
    passos = []
    distancias = {no: float('infinity') for no in grafo}
    distancias[no_inicial] = 0
    predecessores = {no: None for no in grafo}
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