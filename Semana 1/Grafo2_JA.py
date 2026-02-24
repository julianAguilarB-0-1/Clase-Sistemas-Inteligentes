import math
import matplotlib.pyplot as plt
from collections import deque
import random


class grapho:

    def __init__(self):
        self.nodos=[]
        self.aristas=[]

    class Nodo:
        def __init__(self, valor):
            self.valor = valor
            self.conexiones = []

        def __repr__(self):
            return self.valor

    class Arista:
        def __init__(self, origen, destino):
            self.origen = origen
            self.destino = destino

        def __repr__(self):
            return self.origen.valor + "-" + self.destino.valor

    def agregar_nodo(self, valor):
        nodo = self.Nodo(valor)
        self.nodos.append(nodo)
        return nodo

    def agregar_arista(self, origen, destino):
        arista = self.Arista(origen, destino)
        self.aristas.append(arista)

    def actualizar_conexiones(self):
        for i,n in enumerate(self.nodos):
            self.nodos[i].conexiones = []
            for a in self.aristas:
                if(n==a.origen or n==a.destino):
                    self.nodos[i].conexiones.append(a)

    def imprimir_grafo(self):
        print("Nodos ", self.nodos)
        print("Aristas", self.aristas)
        for n in self.nodos:
            print("Conexiones nodo", n.valor, " ", n.conexiones)

    #bfs
    def bfs_con_ruta(self, inicio, fin):
        visitados = set()
        cola = deque([inicio])
        visitados.add(inicio)
        padres = {}

        while cola:
            nodo_actual = cola.popleft()

            if nodo_actual == fin:
                camino = [fin]
                while camino[-1] != inicio:
                    camino.append(padres[camino[-1]])
                camino.reverse()
                return camino

            for arista in nodo_actual.conexiones:
                vecino = self.obtener_siguiente(arista, nodo_actual)

                if vecino not in visitados:
                    visitados.add(vecino)
                    padres[vecino] = nodo_actual
                    cola.append(vecino)

        return None

    def distancia_bfs(self, inicio, fin):
        camino = self.bfs_con_ruta(inicio, fin)
        if camino:
            return len(camino) - 1
        return -1

    def obtener_siguiente(self, arista, actual):
        if arista.origen == actual:
            return arista.destino
        else:
            return arista.origen

    #vecinos
    def vecinos_comunes(self, nodo1, nodo2):
        vecinos1 = set()
        vecinos2 = set()

        for ar in nodo1.conexiones:
            vecinos1.add(self.obtener_siguiente(ar, nodo1))

        for ar in nodo2.conexiones:
            vecinos2.add(self.obtener_siguiente(ar, nodo2))

        interseccion = vecinos1.intersection(vecinos2)
        return len(interseccion)

    def obtener_lista_iniciosfines(self,nodos):
        rutas =[]
        cont=0
        for i in nodos:
            for j in nodos:
                if(i!=j):
                    rutas.append([i,j])
                    cont=cont+1
        return rutas,cont

    # lo de la grafica dos el regreso
    def graficar_plano(self, dataset, x_col, y_col, etiqueta_x="", etiqueta_y="",
                      x_nuevo=None, y_nuevo=None,
                      recta=None, jitter=False):

        if not dataset:
            print("Dataset vacío.")
            return

        x1, y1 = [], []
        x0, y0 = [], []

        for fila in dataset:
            x = fila[x_col]
            y = fila[y_col]
            llego = fila[7]

            if jitter:
                x = x + random.uniform(-0.05, 0.05)
                y = y + random.uniform(-0.05, 0.05)

            if llego == 1:
                x1.append(x); y1.append(y)
            else:
                x0.append(x); y0.append(y)

        plt.figure()
        plt.scatter(x1, y1, marker='o', label="llego = 1")
        plt.scatter(x0, y0, marker='x', label="llego = 0")

        if x_nuevo is not None and y_nuevo is not None:
            plt.scatter([x_nuevo], [y_nuevo], marker='*', s=200, label="Nuevo punto")

        if recta is not None:
            x_min = min(fila[x_col] for fila in dataset)
            x_max = max(fila[x_col] for fila in dataset)
            xs = [x_min, x_max]
            ys = [recta(x) for x in xs]
            plt.plot(xs, ys, linestyle='--', label="Recta heurística")

        plt.xlabel(etiqueta_x if etiqueta_x else f"Columna {x_col}")
        plt.ylabel(etiqueta_y if etiqueta_y else f"Columna {y_col}")
        plt.title("Diagrama de dispersión del dataset")
        plt.legend()
        plt.grid(True)
        plt.show()


#gafo el 7
def iniciarGrapho1():
    grafo = grapho()
    nA = grafo.agregar_nodo("A")
    nB = grafo.agregar_nodo("B")
    nC = grafo.agregar_nodo("C")
    nD = grafo.agregar_nodo("D")
    nE = grafo.agregar_nodo("E")
    nF = grafo.agregar_nodo("F")
    nG = grafo.agregar_nodo("G")
    nH = grafo.agregar_nodo("H")

    grafo.agregar_arista(nA, nB)
    grafo.agregar_arista(nA, nC)
    grafo.agregar_arista(nA, nD)
    grafo.agregar_arista(nA, nG)
    grafo.agregar_arista(nC, nB)
    grafo.agregar_arista(nC, nD)
    grafo.agregar_arista(nC, nE)
    grafo.agregar_arista(nE, nF)
    grafo.agregar_arista(nE, nH)
    grafo.agregar_arista(nE, nG)
    grafo.agregar_arista(nG, nF)
    grafo.agregar_arista(nG, nH)

    grafo.actualizar_conexiones()
    return grafo