inicios = ["A","B","C","D","E","F","G","H"]
fines = ["A","B","C","D","E","F","G","H"]
rutas = []
cont = 0
contA = 0

for i in inicios:
    for j in fines:
        if i != j:
            rutas.append((i, j))
            cont = cont + 1

            if i == "A":
                contA = contA + 1
                

print(rutas)
print("El numero de rutas es:", cont)


#busqueda por anchura
from collections import deque

def bfs(grafo, inicio):
    visitados = set()
    cola = deque([inicio])
    visitados.add(inicio)

    while cola:
        nodo = cola.popleft()
        print(nodo)

        for vecino in grafo[nodo]:
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino)

# Grafo como diccionario
grafo = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B'],
    'F': ['C']
}

bfs(grafo, 'A')

