# Os grafos de exemplo agora são explicitamente direcionados.
EXAMPLE_1 = {
    "grafo": {
        0: {1: 2, 2: 4},
        1: {2: 1, 3: 7},
        2: {4: 3},
        3: {5: 1},
        4: {3: 2, 5: 5},
        5: {}
    },
    "posicoes": {
        0: (0, 1), 1: (1, 2), 2: (1, 0),
        3: (2, 2), 4: (2, 0), 5: (3, 1)
    },
    "proximo_id": 6
}

EXAMPLE_2 = {
    "grafo": {
        0: {1: 2, 2: 5, 5: 15},
        1: {3: 3},
        2: {3: 6},
        3: {4: 2, 5: 8},
        4: {5: 1, 7: 10},
        5: {6: 2},
        6: {7: 3},
        7: {}
    },
    "posicoes": {
        0: (0, 1), 1: (1, 2), 2: (1, 0), 3: (2, 1),
        4: (3, 2), 5: (3, 0), 6: (4, 0), 7: (5, 1)
    },
    "proximo_id": 8
}

def get_example(number):
    """Retorna o grafo de exemplo escolhido."""
    if number == 1:
        return EXAMPLE_1
    elif number == 2:
        return EXAMPLE_2
    return EXAMPLE_1 # Retorna o primeiro por padrão