# %% ##################### IMPORTACIÓN DE MÓDULOS #####################
from random import randint
import numpy as np

# %% ##################### FUNCIONES ADICIONALES #####################

def crear_entrada(valor_entrada, nuevo_peso):
    if nuevo_peso == -1 : 
        nuevo_peso = randint(1, 10) / 10

    return dict(
        valor = valor_entrada,
        peso = nuevo_peso
    )

def mostrar_entradas(lista_entradas, wbias):
    for i, entrada in enumerate(lista_entradas):
        print("Valor ({}): {}".format(i+1, entrada["valor"]))
        print("Peso ({}): {}".format(i+1, entrada["peso"]))

    print("Wbias: {}".format(wbias))

def transformar_notas(nota) :
    if nota > 11: 
        return 1
    else:
        return 0

def llenar_datos(tabla) :
    entradas = []
    entrada_fila = []

    peso = [-1, -1, -1]

    for fila in tabla :
        for a, iterar in enumerate(fila) :
            entrada_fila.append(crear_entrada(
                transformar_notas(iterar), peso[a]))
                
            if a <= 2 : 
                peso[a] = entrada_fila[a]["peso"]

        entradas.append(entrada_fila)
        entrada_fila = []

    print(entradas)
    return entradas

def ingresar_notas() :
    existe_error = True
    notas = []

    while existe_error:
        try:
            for iterar in range(3) :
                valor = -1
                while valor < 0 or valor > 20:
                    valor = int(input("Ingrese la nota N° {} | ".format(iterar + 1)))

                if valor >= 0 and valor <= 20:
                    notas.append(transformar_notas(valor))

                existe_error = False
        except ValueError:
            notas = []
            print("Solo se permiten números")
            existe_error = True

    return notas

# %% ##################### FUNCIONES PARA ENTRENAR LA NEURONA #####################

def funcion_de_activacion(net):
    if net >= 0:
        return 1
    else:
        return 0

def calcular_error(yd, y):
    return yd - y

def modificar_pesos(entradas, error):
    nuevas_entradas = []
    for entrada in entradas:
        nueva_entrada = dict(
            valor = entrada["valor"],
            peso = entrada["peso"] + FA * error * entrada["valor"]
        )
        
        nuevas_entradas.append(nueva_entrada)
    
    return nuevas_entradas


# %% ##################### ENTRENAMIENTO #####################

def entrenamiento():
    entradas = llenar_datos(tabla)

    cont = 1
    cont_final = 1
    reinicio = True

    while reinicio :
        for a, fila in enumerate(entradas) :
            cont = 1
            error = -1
            net = 0

            while error != 0:
                for entrada in fila:
                    net += entrada["valor"] * entrada["peso"]

                net += wbias["valor"] * wbias["peso"]
                y = funcion_de_activacion(net)
                error = calcular_error(esperado[a], y)

                print("\n::::: FILA {} :::::".format(a + 1))
                mostrar_entradas(fila, wbias)
                print("Error: {} ({})".format(error, cont))
                print("------------------------------------------")

                if error != 0:
                    fila = modificar_pesos(fila, error)
                    wbias["peso"] = wbias["peso"] + FA * error * wbias["valor"]
                    entradas[a] = fila

                    for it_1 in range(8) :
                        for it_2, it_3 in enumerate(fila) :
                            entradas[it_1][it_2]["peso"] = it_3["peso"]
                    
                    reinicio = True
                    break

                else:
                    print("Y: {}".format(y))
                    reinicio = False

                cont += 1
            
            cont_final += 1

            if reinicio : break

        print("##########################################")

    for filas in entradas :
        print()
        mostrar_entradas(filas, wbias)

    print("\nTotal de interaciones : {}".format(cont_final))
    print("\n:::::::::::::::::::::::::::::::::::::::::\n")

    return entradas

# %% ##################### COMPROBAR ENTRENAMIENTO #####################

def comprobar_neurona(entradas):
    net = 0

    notas = ingresar_notas()

    for it in range(3) :

        net += notas[it] * entradas[0][it]["peso"]
        
    net += wbias["peso"] 

    if funcion_de_activacion(net):
        print("RESULTADO: -------> Aprobaste")
    else:
        print("RESULTADO: -------> Reprobaste")

# %%  ##################### VARIABLES GLOBALES #####################

error = -1
net = 0
wbias = {"valor": 1.0, "peso": 1.5}
FA = 0.9

tabla = [[4, 0, 4], [20, 7, 3], [5, 18, 3], 
         [16, 19, 0], [10, 6, 15], [19, 1, 19],
         [2, 17, 14], [19, 16, 20]]

esperado = [0, 0, 0, 1, 0, 1, 1, 1]


# %% ##################### MAIN #####################

def main():
    entradas = entrenamiento()
    comprobar_neurona(entradas)

if __name__ == "__main__":
    main()