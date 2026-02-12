import Grafo1_JA

grafo1 = Grafo1_JA.iniciarGrapho1()
grafo1.imprimir_grafo()
grafo1.agregar_nodo("I")
camino = grafo1.trayectoria(grafo1.nodos[0],grafo1.nodos[6])
if camino:
    print(camino)
else:
    print("no se puede llegar")


#el otro
grafo2 = Grafo1_JA.iniciarGrapho2()
grafo2.imprimir_grafo()
print(grafo2.trayectoria(grafo2.nodos[0],grafo2.nodos[2]))