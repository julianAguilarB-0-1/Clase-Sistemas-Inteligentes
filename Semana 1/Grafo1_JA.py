import math
import matplotlib.pyplot as plt


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
    def __repr__(self):
         return "Nodos " + self.nodos +" " + "Aristas "+ self.Arista
   
    def agregar_nodo(self, valor):
        nodo = self.Nodo(valor)
        self.nodos.append(nodo)
        return nodo

   
    def agregar_arista(self, origen, destino):
        arista = self.Arista(origen, destino)
        self.aristas.append(arista)
    def actualizar_conexiones(self):
         for i,n in enumerate(self.nodos):
              for a in self.aristas:
                   if(n==a.origen or n==a.destino):
                        self.nodos[i].conexiones.append(a)
    
    def imprimir_grafo(self):
        print("Nodos ", self.nodos)
        print("Aristas", self.aristas)
        for n in self.nodos:
            print("Conexiones nodo", n.valor, " ", n.conexiones)
    
    def trayectoria_grado(self, inicio, fin, modo="max"):
        if inicio == fin:
            return [inicio]

        camino = [inicio]
        actual = inicio
        usadas = set()  # aristas ya usadas (para no repetir)

        while actual != fin:
            # aristas disponibles desde el nodo actual
            candidatas=self.obtener_candidatas(actual,usadas)#candidatas = [ar for ar in actual.conexiones if ar not in usadas]
            if not candidatas:
                print("Trayectoria inconclusa", camino)
                return None
            # elegir la mejor arista según la heurística de grado
            mejor_arista = None
            mejor_valor = None
            print("CAN ",candidatas," USADAS ",usadas)

            for ar in candidatas:
                # grafo no dirigido: tomar el otro extremo
                #siguiente = ar.destino if ar.origen == actual else ar.origen
                siguiente = self.obtener_siguiente(ar,actual)
                valor = self.grado_restante(siguiente,usadas)  # heurística
                mejor_arista,mejor_valor = self.mejor_arista(ar,valor,mejor_arista,mejor_valor)
            # aplicar el paso elegido
            print("valor=",valor,"Mejor valor =",mejor_valor," ",ar," ",mejor_arista)
            usadas.add(mejor_arista)
            siguiente = self.obtener_siguiente(mejor_arista,actual)
            camino.append(siguiente)
            actual = siguiente

        return camino
  #return sum(1 for ar in nodo.conexiones if ar not in usadas)
    def grado_restante(self,nodo,usadas):
        contador = 0
        for arista in nodo.conexiones:
            esta_usada = arista in usadas
            if esta_usada == False:
                contador = contador + 1
        return contador
   
    def obtener_candidatas(self,nodo, usadas):
        candidatas = []
        for arista in nodo.conexiones:
            if arista not in usadas:
                candidatas.append(arista)
        return candidatas
    def obtener_siguiente(self,arista, actual):
    # 1. Verificar si el nodo actual es el origen de la arista
        if arista.origen == actual:
            siguiente = arista.destino
        else:
            siguiente = arista.origen
        return siguiente
    def mejor_arista(self,ar,valor,mejor_arista,mejor_valor,modo="max"):              
                if mejor_arista is None:
                    mejor_arista = ar
                    mejor_valor = valor
                else:
                    if modo == "max":
                        if valor > mejor_valor:
                            mejor_arista = ar
                            mejor_valor = valor
                    else:  # modo == "min"
                        if valor < mejor_valor:
                            mejor_arista = ar
                            mejor_valor = valor
                print("valor=",valor,"Mejor valor =",mejor_valor," ",ar," ",mejor_arista)
                return mejor_arista,mejor_valor
    def obtener_lista_iniciosfines(self,nodos):
        rutas =[]
        cont=0
        for i in nodos:
            for j in nodos:
                if(i!=j):
                    rutas.append([i,j])
                    cont=cont+1
        print(rutas)
        return rutas,cont
    def llenar_dataset(self,inis_fins):
        for i in inis_fins:
            print(1)

    #KNN(Vecino mas cercano)
    def knn_clasificar(self,dataset, grado_inicio_nuevo, grado_fin_nuevo, k=3):
        nuevo = [grado_inicio_nuevo, grado_fin_nuevo]
        vecinos = []

        for fila in dataset:
            x = [fila[3], fila[4]]
            #print("Aqui ",x)
            d=math.sqrt((x[0] - nuevo[0])**2 + (x[1] - nuevo[1])**2)
            #d = distancia_euclidiana(x, nuevo)
            vecinos.append((d, fila[4]))

        # Ordenar por distancia (menor = más cercano)
        vecinos.sort(key=lambda x: x[0])#ordenamiento de la burbuja

        # Tomar los k vecinos más cercanos
        k_vecinos = vecinos[:k]

        # Votación mayoritaria
        votos = 0  # inicializamos el contador de votos
        for v in k_vecinos:
            etiqueta = v[1]     # segundo elemento de la tupla (llego_al_final)
            votos = votos + etiqueta

        if votos > k/2:
            return 1
        else:
            return 0
    def graficar_knn_y_recta(self,dataset, Gi_nuevo, GF_nuevo, umbral=6):
        # Separar puntos por clase (llego)
        Gi_1, GF_1 = [], []
        Gi_0, GF_0 = [], []

        for fila in dataset:
            Gi = fila[3]
            GF = fila[4]
            llego = fila[5]

            if llego == 1:
                Gi_1.append(Gi); GF_1.append(GF)
            else:
                Gi_0.append(Gi); GF_0.append(GF)

        # --- imprimir la ecuación de la recta heurística ---
        # Gi + GF = umbral  ->  GF = umbral - Gi
        print(f"Recta heurística: Gi + GF = {umbral}")
        print(f"En forma despejada: GF = {umbral} - Gi")

        # --- graficar puntos ---
        plt.figure()
        plt.scatter(Gi_1, GF_1, marker='o', label="llego = 1")
        plt.scatter(Gi_0, GF_0, marker='x', label="llego = 0")

        # Punto nuevo
        plt.scatter([Gi_nuevo], [GF_nuevo], marker='*', s=200, label="Nuevo punto")

        # --- graficar la recta ---
        # rango de Gi, para que la recta cubra tu nube de puntos
        gi_min = min([fila[3] for fila in dataset])
        gi_max = max([fila[3] for fila in dataset])

        x_vals = [gi_min, gi_max]
        y_vals = [umbral - x for x in x_vals]
        plt.plot(x_vals, y_vals, linestyle='--', label="Recta heurística")

        plt.xlabel("Gi")
        plt.ylabel("GF")
        plt.title("Plano Gi-GF: Dataset + Recta heurística")
        plt.legend()
        plt.grid(True)
        plt.show()

#grafo 7 y otro que no me acuerdo el numero

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

def iniciarGrapho2():
    grafo = grapho()
    nA = grafo.agregar_nodo("A")
    nB = grafo.agregar_nodo("B")
    nC = grafo.agregar_nodo("C")
    nD = grafo.agregar_nodo("D")
    grafo.agregar_arista(nA, nB)
    grafo.agregar_arista(nB, nC)
    grafo.agregar_arista(nC, nD)
    grafo.agregar_arista(nD, nA)
    grafo.actualizar_conexiones()
    return grafo
