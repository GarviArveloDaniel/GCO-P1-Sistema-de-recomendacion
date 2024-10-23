from cosine import coseno_similitud
from euclidea import similitud_euclidea
from pearson import pearson


def cargar_matriz_utilidad(archivo):
    """
    Carga la matriz de utilidad desde un archivo.
    
    Args:
        archivo (str): Ruta al archivo que contiene la matriz.
    
    Returns:
        list: Matriz de utilidad con calificaciones de usuarios.
    """
    with open(archivo, 'r') as f:
        matriz = [line.strip().split() for line in f.readlines()]
        # Convertir los elementos a float o mantener el "-" para faltantes
        matriz = [[float(x) if x != '-' else '-' for x in fila] for fila in matriz]
    return matriz



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
        # Obtenemos los vecinos ordenados por similitud de mayor a menor
        vecinos_ordenados = sorted(range(len(sim)), key=lambda x: sim[x], reverse=True)
        # Excluimos al propio usuario (primer elemento) y seleccionamos los k vecinos más cercanos
        vecinos.append(vecinos_ordenados[1:k+1])
    return vecinos


def prediccion_simple(usuario, vecinos, matriz, similitudes, item):
    """
    Predice la calificación faltante de un usuario para un ítem, usando predicción simple.
    
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
    for vecino in vecinos:
        if matriz[vecino][item] != '-':
            numerador += similitudes[usuario][vecino] * matriz[vecino][item]
            denominador += abs(similitudes[usuario][vecino])
    
    return numerador / denominador if denominador != 0 else 0


def prediccion_con_media(usuario, vecinos, matriz, similitudes, item):
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
    media_usuario = sum([v for v in matriz[usuario] if v != '-']) / len([v for v in matriz[usuario] if v != '-'])
    numerador = 0
    denominador = 0
    
    for vecino in vecinos:
        media_vecino = sum([v for v in matriz[vecino] if v != '-']) / len([v for v in matriz[vecino] if v != '-'])
        if matriz[vecino][item] != '-':
            numerador += similitudes[usuario][vecino] * (matriz[vecino][item] - media_vecino)
            denominador += abs(similitudes[usuario][vecino])
    
    return media_usuario + numerador / denominador if denominador != 0 else media_usuario


def imprimir_resultados(matriz, matriz_similitud, vecinos):
    """
    Imprime la matriz de utilidad con las predicciones, las similitudes y los vecinos seleccionados.
    """
    print("Matriz de utilidad con predicciones:")
    for fila in matriz:
        print(fila)
    
    print("\nMatriz de similitudes:")
    for fila in matriz_similitud:
        print(fila)
    
    print("\nVecinos seleccionados para cada usuario:")
    for i, v in enumerate(vecinos):
        print(f"Usuario {i}: Vecinos {v}")


def main():
    archivo = 'matriz.txt'  # Ruta al archivo de la matriz de utilidad
    metrica = 'pearson'  # Cambiar por 'coseno' o 'euclidea'
    k = 3  # Número de vecinos
    tipo_prediccion = 'simple'  # 'simple' o 'media'
    
    matriz = cargar_matriz_utilidad(archivo)
    matriz_similitud = calcular_similitud_matriz(matriz, metrica)
    vecinos = seleccionar_vecinos(matriz_similitud, k)
    
    # Predecir valores faltantes
    for usuario in range(len(matriz)):
        for item in range(len(matriz[usuario])):
            if matriz[usuario][item] == '-':
                if tipo_prediccion == 'simple':
                    matriz[usuario][item] = prediccion_simple(usuario, vecinos[usuario], matriz, matriz_similitud, item)
                elif tipo_prediccion == 'media':
                    matriz[usuario][item] = prediccion_con_media(usuario, vecinos[usuario], matriz, matriz_similitud, item)
    
    imprimir_resultados(matriz, matriz_similitud, vecinos)

if __name__ == "__main__":
    main()
