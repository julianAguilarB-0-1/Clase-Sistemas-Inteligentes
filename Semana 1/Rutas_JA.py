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
