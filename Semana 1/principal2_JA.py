import Grafo2_JA

def inicio_fin_2(valor_origen,valor_destino):
    indice_origen=busca_indice(migrafo.nodos,valor_origen)
    indice_destino=busca_indice(migrafo.nodos,valor_destino)
    return(indice_origen,indice_destino)

def busca_indice(g,v):
    for i,n in enumerate(g):
        if(v==n.valor):
            return i

op=1
migrafo=Grafo2_JA.iniciarGrapho1()

dataset1=[]
inifin=[]

while(op!=10):
    print("\nMenu de grafos")
    print("1.Crear Grafo")
    print("2.Imprimir Grafo")
    print("3.Trayectoria")
    print("4.Heuristica Grado")
    print("5.Generar inicios-fines")
    print("6.Generar dataset completo")
    print("7.Imprimir dataset")
    print("8.Grafica dispersion")
    print("9.BFS")
    print("10.Salir")

    op=int(input("Teclea una opcion: "))

    if(op==1):
        num_nodos=int(input("Cuantos nodos tiene el grafo: "))
        num_aristas=int(input("Cuantas aristas tiene el grafo: "))

        for i in range(num_nodos):
            valor_nodo=input("Valor del nodo: ")
            migrafo.agregar_nodo(valor_nodo)

        for i in range(num_aristas):
            vo=input("Origen: ")
            vd=input("Destino: ")

            io=busca_indice(migrafo.nodos,vo)
            id=busca_indice(migrafo.nodos,vd)

            migrafo.agregar_arista(migrafo.nodos[io],migrafo.nodos[id])

        migrafo.actualizar_conexiones()

    elif(op==2):
        print("Nodos:", migrafo.nodos)
        print("Aristas:", migrafo.aristas)
        for n in migrafo.nodos:
            print("Nodo", n.valor, "->", n.conexiones)

    elif(op==4):
        vo=input("Inicio: ")
        vd=input("Fin: ")

        io=busca_indice(migrafo.nodos,vo)
        id=busca_indice(migrafo.nodos,vd)

        camino=migrafo.trayectoria_grado(
            migrafo.nodos[io],
            migrafo.nodos[id]
        )

        print([n.valor for n in camino] if camino else "No hay camino")

    elif(op==5):
        inifin,c=migrafo.obtener_lista_iniciosfines(migrafo.nodos)

    elif(op==6):
        dataset1=[]

        for i,n in enumerate(inifin):
            nodo_inicio=n[0]
            nodo_fin=n[1]

            grado_inicio=len(nodo_inicio.conexiones)
            grado_fin=len(nodo_fin.conexiones)

            # BFS
            resultado=migrafo.bfs_con_ruta(nodo_inicio,nodo_fin)

            if resultado:
                dist_bfs=len(resultado)-1
                llego=1
            else:
                dist_bfs=-1
                llego=0

            # Vecinos comunes
            vec_comunes=migrafo.vecinos_comunes(nodo_inicio,nodo_fin)

            # Score
            if llego==1:
                score=10-dist_bfs
            else:
                score=0

            dataset1.append([
                i,
                nodo_inicio,
                nodo_fin,
                grado_inicio,
                grado_fin,
                dist_bfs,
                vec_comunes,
                llego,
                score
            ])

        print("\nDataset generado correctamente")

    elif(op==7):
        print("\nID | Ni | Nf | Gi | Gf | Dist | Vecinos | Llego | Score")

        for fila in dataset1:
            print(
                fila[0], "|",
                fila[1].valor, "|",
                fila[2].valor, "|",
                fila[3], "|",
                fila[4], "|",
                fila[5], "|",
                fila[6], "|",
                fila[7], "|",
                fila[8]
            )

    elif(op==8):
        migrafo.graficar_plano(dataset1,6,8,"Vecinos","Score")

    elif(op==9):
        vo=input("Nodo inicio BFS: ")
        vd=input("Nodo fin BFS: ")

        io=busca_indice(migrafo.nodos,vo)
        id=busca_indice(migrafo.nodos,vd)

        if io is not None and id is not None:
            camino=migrafo.bfs_con_ruta(
                migrafo.nodos[io],
                migrafo.nodos[id]
            )

            if camino:
                print("Camino:", [n.valor for n in camino])
                print("Distancia mínima:", len(camino)-1)
            else:
                print("No hay camino")
        else:
            print("Nodo no encontrado")

    elif(op==10):
        print("Bye bye baby")