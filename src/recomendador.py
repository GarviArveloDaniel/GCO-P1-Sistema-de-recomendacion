from cosine import coseno_similitud
from euclidea import similitud_euclidea
from pearson import pearson
import argparse
from colorama import Fore, Style, init



def cargar_matriz_utilidad(archivo):
    """
    Carga la matriz de utilidad desde un archivo.
    
    Args:
        archivo (str): Ruta al archivo que contiene la matriz.
    
    Returns:
        list: Matriz de utilidad con calificaciones de usuarios.
    """
    with open(archivo, 'r') as f:
        # Las dos primeras filas del fichero las ignoramos
        min_val = f.readline()
        max_val = f.readline()
        matriz = [line.strip().split() for line in f.readlines()]
        # Convertir los elementos a float o mantener el "-" para faltantes
        matriz = [[float(x) if x != '-' else '-' for x in fila] for fila in matriz]
    return matriz, float(min_val), float(max_val)



def calcular_similitud_matriz(matriz, metrica):
    """
    Calcula la similitud entre todos los usuarios usando la métrica elegida.
    
    Args:
        matriz (list): Matriz de utilidad con calificaciones de usuarios.
        metrica (str): Métrica de similitud ('pearson', 'coseno', 'euclidea').
    
    Returns:
        list: Matriz de similitud entre usuarios.
    """
    num_usuarios = len(matriz)
    matriz_similitud = [[0] * num_usuarios for _ in range(num_usuarios)]
    
    for i in range(num_usuarios):
        for j in range(i + 1, num_usuarios):
            if metrica == 'pearson':
                sim = pearson(matriz[i], matriz[j])
            elif metrica == 'coseno':
                sim = coseno_similitud(matriz[i], matriz[j])
            elif metrica == 'euclidea':
                sim = similitud_euclidea(matriz[i], matriz[j])
            matriz_similitud[i][j] = matriz_similitud[j][i] = sim
    
    return matriz_similitud


def seleccionar_vecinos(similitudes, k):
    """
    Selecciona los k vecinos más cercanos para cada usuario.
    
    Args:
        similitudes (list): Matriz de similitud entre usuarios.
        k (int): Número de vecinos a seleccionar.
    
    Returns:
        list: Lista de vecinos para cada usuario.
    """
    vecinos = []
    for i, sim in enumerate(similitudes):
        # Excluir al propio usuario
        vecinos_ordenados = sorted([(j, sim_j) for j, sim_j in enumerate(sim) if j != i], key=lambda x: x[1], reverse=True)
        # Seleccionar los k vecinos más cercanos
        vecinos.append([vecino[0] for vecino in vecinos_ordenados[:k]])
    return vecinos


def prediccion_simple(usuario, vecinos, matriz, similitudes, item, min_val):
    """
    Predice la calificación faltante de un usuario para un ítem, usando predicción simple.
    
    Args:
        usuario (int): Índice del usuario para el que se va a predecir.
        vecinos (list): Vecinos del usuario.
        matriz (list): Matriz de utilidad con calificaciones de usuarios.
        similitudes (list): Matriz de similitud entre usuarios.
        item (int): Índice del ítem a predecir.
        min_val (float): Valor mínimo de calificación.
        max_val (float): Valor máximo de calificación.
    
    Returns:
        float: Predicción de la calificación.
    """
    numerador = 0
    denominador = 0
    for vecino in vecinos:
        if vecino < len(matriz) and item < len(matriz[vecino]):  # Verificar que los índices sean válidos
            if matriz[vecino][item] != '-':
                numerador += similitudes[usuario][vecino] * matriz[vecino][item]
                denominador += abs(similitudes[usuario][vecino])
    
    if (denominador == 0):
        return min_val        
    return round((numerador / denominador), 2) if (numerador / denominador) >= min_val else min_val


def prediccion_con_media(usuario, vecinos, matriz, similitudes, item, min_val):
    """
    Predice la calificación faltante de un usuario para un ítem, usando la diferencia con la media.
    
    Args:
        usuario (int): Índice del usuario para el que se va a predecir.
        vecinos (list): Vecinos del usuario.
        matriz (list): Matriz de utilidad con calificaciones de usuarios.
        similitudes (list): Matriz de similitud entre usuarios.
        item (int): Índice del ítem a predecir.
    
    Returns:
        float: Predicción de la calificación.
    """
    numerador = 0
    denominador = 0
    media_usuario = sum([x for x in matriz[usuario] if x != '-']) / len([x for x in matriz[usuario] if x != '-'])
    
    for vecino in vecinos:
        if vecino < len(matriz) and item < len(matriz[vecino]):  # Verificar que los índices sean válidos
            if matriz[vecino][item] != '-':
                media_vecino = sum([x for x in matriz[vecino] if x != '-']) / len([x for x in matriz[vecino] if x != '-'])
                numerador += similitudes[usuario][vecino] * (matriz[vecino][item] - media_vecino)
                denominador += abs(similitudes[usuario][vecino])
    
    if denominador == 0:
        return media_usuario  # Evitar división por cero)
    
    return round((media_usuario + (numerador / denominador)), 2) if (media_usuario + (numerador / denominador)) >= min_val else min_val

# Inicializar colorama
init()
def imprimir_resultados(matriz, matriz_similitud, vecinos, predicciones):
    """
    Imprime la matriz de utilidad con las predicciones, las similitudes y los vecinos seleccionados.
    """
    print("Matriz de utilidad con predicciones:")
    for i, fila in enumerate(matriz):
        print("[", end=" ")
        for j, valor in enumerate(fila):
            if (i, j, valor) in predicciones:
                print(Fore.RED + str(valor) + Style.RESET_ALL, end=" ")
            else:
                print(valor, end=" ")
        print("]")
    
    print("\nMatriz de similitudes:")
    for fila in matriz_similitud:
        print(fila)
    
    print("\nVecinos seleccionados para cada usuario:")
    for i, v in enumerate(vecinos):
        print(f"Usuario {i}: Vecinos {v}")

    print("\nPredicciones de valoraciones de usuarios:")
    for usuario, item, prediccion in predicciones:
        print(f"Usuario {usuario} - Ítem {item}: {prediccion}")


# EJEMPLO DE EJECUCION: python3 recomendador.py --archivo matriz.txt --metrica euclidea --vecinos 3 --tipo_prediccion media

def main():
    # Configurar el analizador de argumentos
    parser = argparse.ArgumentParser(description='Sistema de recomendación basado en diferentes métricas y tipos de predicción.')
    parser.add_argument('-a', '--archivo', type=str, required=True, help='Ruta al archivo de la matriz de utilidad')
    parser.add_argument('-m', '--metrica', type=str, required=True, choices=['pearson', 'coseno', 'euclidea'], help='Métrica elegida: pearson, coseno o euclidea')
    parser.add_argument('-v', '--vecinos', type=int, required=True, help='Número de vecinos considerado')
    parser.add_argument('-t', '--tipo_prediccion', type=str, required=True, choices=['simple', 'media'], help='Tipo de predicción: simple o media')

    # Parsear los argumentos
    args = parser.parse_args()

    # Asignar los argumentos a variables
    archivo = args.archivo
    metrica = args.metrica
    k = args.vecinos
    tipo_prediccion = args.tipo_prediccion

    # Cargar la matriz de utilidad
    matriz, min_val, max_val = cargar_matriz_utilidad(archivo)
    
    # Calcular la matriz de similitud
    matriz_similitud = calcular_similitud_matriz(matriz, metrica)
    # Seleccionar los vecinos
    vecinos = seleccionar_vecinos(matriz_similitud, k)
    # Lista para guardar únicamente las predicciones
    predicciones = []
    
    # Predecir valores faltantes
    for usuario in range(len(matriz)):
        for item in range(len(matriz[usuario])):
            if matriz[usuario][item] == '-':
                if tipo_prediccion == 'simple':
                    matriz[usuario][item] = prediccion_simple(usuario, vecinos[usuario], matriz, matriz_similitud, item, min_val)
                elif tipo_prediccion == 'media':
                    matriz[usuario][item] = prediccion_con_media(usuario, vecinos[usuario], matriz, matriz_similitud, item, min_val)
                predicciones.append((usuario, item, matriz[usuario][item]))
    # Imprimir los resultados
    imprimir_resultados(matriz, matriz_similitud, vecinos, predicciones)

if __name__ == "__main__":
    main()