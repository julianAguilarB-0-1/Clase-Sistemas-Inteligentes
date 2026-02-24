import Grafo1_JA

def inicio_fin_2(valor_origen,valor_destino):
    indice_origen=busca_indice(migrafo.nodos,valor_origen)
    indice_destino=busca_indice(migrafo.nodos,valor_destino)
    return(indice_origen,indice_destino)

op=1
migrafo=Grafo1_JA.iniciarGrapho1()
migrafo2=Grafo1_JA.grapho()

def busca_indice(g,v):
    for i,n in enumerate(g):
        if(v==n.valor):
            return i

dataset1=[]
inifin=[]   # <-- agregado

while(op!=10):
    print("Menu de grafos")
    print("1.Crear Grafo")
    print("2.-imprimir Grafo ")
    print("3.-Trayectoria")
    print("4.-Euristica Grado")
    print("5.-LLenar inicios fines ")
    print("6.-LLenar e imprimir dataset ")
    print("7.-Dataset que pidio el profe")
    print("8.-Vecino mas cercano")
    print("9.-BFS")
    print("10.-Salir")
    

    op=int(input("Teclea una opcion"))

    if(op==1):
        num_nodos=int(input("Cuantos nodos tiene el grafo"))
        num_aristas=int(input("Cuantas aristas tiene el grafo"))
        for i in range(0,num_nodos,1):
            valor_nodo=input("Teclea el valor del nodo ")
            migrafo.agregar_nodo(valor_nodo)
        for i in range(0,num_aristas,1):
            valor_origen=input("Teclea el valor del origen ")
            indice_origen=busca_indice(migrafo.nodos,valor_origen)
            valor_destino=input("Teclea el valor del destino ")
            indice_destino=busca_indice(migrafo.nodos,valor_destino)
            migrafo.agregar_arista(migrafo.nodos[indice_origen],migrafo.nodos[indice_destino])
        migrafo.actualizar_conexiones()
    elif(op==2):
        print("Nodos ",migrafo.nodos)
        print("Aristas",migrafo.aristas)
        for n in migrafo.nodos:
            print("Conexiones nodo",n.valor," ",n.conexiones)
    elif(op==3):
        indice_origen,indice_destino=inicio_fin()
        aver=migrafo.trayectoria(migrafo.nodos[indice_origen],migrafo.nodos[indice_destino])
        print(aver)

    elif(op==4):
        indice_origen,indice_destino=inicio_fin()
        aver=migrafo.trayectoria_grado(
            migrafo.nodos[indice_origen],
            migrafo.nodos[indice_destino]
        )
        print(aver)

    elif(op==5):
        inifin,c=migrafo.obtener_lista_iniciosfines(migrafo.nodos)

    elif(op==6):
        dataset1=[]  # <-- agregado
        for i,n in enumerate(inifin):
            indice_origen,indice_destino=inicio_fin_2(
                n[0].valor,n[1].valor
            )

            if indice_origen!=None and indice_destino!=None:  # <-- agregado
                aver=migrafo.trayectoria_grado(
                    migrafo.nodos[indice_origen],
                    migrafo.nodos[indice_destino]
                )
            else:
                aver=None

            if aver!=None:
                llego=1
                score=10-len(aver)
            else:
                llego=0
                score=0

            dataset1.append([
                i,n[0],n[1],
                len(n[0].conexiones),
                len(n[1].conexiones),
                llego,score
            ])

        for i,n in enumerate(dataset1):
            print(n)
    elif(op==7):
        for indice, nodo_inicio, nodo_final, grado_inicio, grado_final, llego, score in dataset1:
             print(indice," | ", grado_inicio," | ", grado_final)
    elif(op==8):
        Gi_nuevo = int(input("grado inicial: "))
        GF_nuevo = int(input("grado final: "))

        # grafica
        migrafo.graficar_knn_y_recta(dataset1, Gi_nuevo, GF_nuevo)
    elif op == 9:
        valor_origen = input("Nodo inicio BFS: ")
        valor_destino = input("Nodo fin BFS: ")

        indice_origen = busca_indice(migrafo.nodos, valor_origen)
        indice_destino = busca_indice(migrafo.nodos, valor_destino)

        if indice_origen is not None and indice_destino is not None:
            resultado = migrafo.bfs_con_ruta(
                migrafo.nodos[indice_origen],
                migrafo.nodos[indice_destino]
            )
            if resultado:
                print("Camino BFS:", [n.valor for n in resultado])
            else:
                print("No hay camino entre esos nodos")
        else:
            print("Nodo inicio o fin no encontrado")
    elif(op==10):
        print("Bye bye baby")