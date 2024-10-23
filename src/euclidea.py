# MÉTRICA EUCLIDEA. 
# -*- coding: utf-8 -*-

# libreria math para operaciones matemáticas, en este caso para poder calcular la raíz cuadrada
import math

def similitud_euclidea(usuario1, usuario2):
    """
    Calcula la similitud euclídea entre dos usuarios con listas de calificaciones, ignorando valores -1 y '-'.

    Parámetros:
    usuario1 (list): Lista con las calificaciones del usuario 1.
    usuario2 (list): Lista con las calificaciones del usuario 2.

    Retorna:
    float: Similitud entre los dos usuarios (inversamente proporcional a la distancia).
    """
    # Asegurarse de que las listas tengan la misma longitud rellenando con '-'
    max_len = max(len(usuario1), len(usuario2))
    usuario1.extend(['-'] * (max_len - len(usuario1)))
    usuario2.extend(['-'] * (max_len - len(usuario2)))
    
    # Calcular la suma de los cuadrados de las diferencias para ítems calificados
    suma_cuadrados = 0
    items_comunes = 0
    for i in range(len(usuario1)):
        if usuario1[i] not in [-1, '-'] and usuario2[i] not in [-1, '-']:  # Ignorar ítems no calificados
            suma_cuadrados += (usuario1[i] - usuario2[i]) ** 2
            items_comunes += 1
    
    # Si no hay ítems calificados en común, retornar similitud cero
    if items_comunes == 0:
        return 0
    
    # Calcular la distancia euclídea
    distancia = math.sqrt(suma_cuadrados)
    
    # Retornar la similitud (inversamente proporcional a la distancia)
    return 1 / (1 + distancia)

'''
# Ejemplo de uso de la función euclidean_distance con guiones
user_a = [5.0, 3.0, '-', 4.0]
user_b = [1.0, -1, 4.0, 2.0]

similitud = similitud_euclidea(user_a, user_b)
print(f"Similitud Euclídea: {similitud}")
''' 
