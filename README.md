# GCO P1 Sistema de recomendación
Primera práctica de la asignatura GCO: Sistema de recomendación

# Integrantes del grupo

- Alba Pérez Rodríguez
- Daniel Garvi Arvelo
- Guillermo Díaz Bricio
- Alexander Morales Díaz

# Introducción.
Los sistemas de recomendación son herramientas clave en la era digital, permitiendo a las plataformas ofrecer sugerencias personalizadas a los usuarios en función de sus preferencias. El filtrado colaborativo es una técnica popular en este campo que se basa en la idea de que usuarios con gustos similares tienden a compartir opiniones sobre ítems, utilizando estas similitudes para predecir las preferencias en productos o servicios que aún no han sido valorados por un usuario.

En esta práctica, se implementará un sistema de recomendación basado en filtrado colaborativo. El sistema utilizará una matriz de utilidad que contiene las calificaciones de los usuarios sobre diversos ítems, y se aplicarán diferentes métricas de similitud, como la correlación de Pearson, la distancia coseno o la euclidiana, para predecir las calificaciones faltantes. El objetivo es identificar usuarios vecinos con gustos similares y generar recomendaciones precisas, siguiendo los principios del filtrado colaborativo basado en usuarios.
--- 

# Dependencias
Este sistema de recomendación está desarrollado en Python, por lo que se requieren algunos pasos de instalación y configuración. A continuación, se detallan las instrucciones de instalación de Python y las dependencias necesarias en una terminal de Linux.

## Instalación de Python

En la mayoría de las distribuciones de Linux, Python viene preinstalado. Para verificar si ya tienes Python en tu sistema, abre una terminal y ejecuta:

```bash
python3 --version
```
Si ya tienes Python instalado, este comando te mostrará la versión actual. Si Python no está instalado o necesitas una actualización, sigue estos pasos:

1. Actualizar el índice de paquetes.

Esto asegurará que todos los paquetes del sistema estén en su última versión antes de instalar Python.

```bash
sudo apt update
```

2. Instalar python.

Ejecuta el siguiente comando para instalar Python 3:

```bash
sudo apt install python3
```

3. Instalar pip.

pip es el gestor de paquetes para Python, necesario para instalar las bibliotecas requeridas.

```bash
sudo apt install python3-pip
```

Para verificar que tanto python3 como pip están correctamente instalados, ejecuta los siguientes comandos:
```bash
python3 --version
pip3 --version
```

## Configuración del entorno de pyhton.
Para este proyecto, es recomendable configurar un entorno virtual, lo cual permite gestionar las dependencias del proyecto sin interferir con otras aplicaciones.

1. Instalar el módulo venv.

Si el módulo venv no está instalado, instálalo con el siguiente comando:

```bash
sudo apt install python3-venv
```

2. Crear un entorno virtual.

Dentro del directorio del proyecto, ejecuta el siguiente comando para crear un entorno virtual llamado entorno_recomendador:

```bash
python3 -m venv entorno_recomendador
```

3. Activar el entorno virtual.

Una vez creado, activa el entorno virtual con:

```bash
source entorno_recomendador/bin/activate
```

Cuando el entorno esté activo, deberías ver (entorno_recomendador) antes del prompt de la terminal, indicando que estás en el entorno virtual.

Con el entorno virtual activado, instala las bibliotecas necesarias para el sistema de recomendación utilizando pip. En el caso de este proyecto, la biblioteca a instalar es numpy:

```bash
pip install numpy
```

Estas instrucciones permitirán configurar el entorno de Python en Linux e instalar las bibliotecas necesarias para el sistema de recomendación.
--- 

# Explicación del código implementado
El sistema de recomendación consta de varios módulos, cada uno responsable de una métrica de similitud o una funcionalidad particular. A continuación, se detallan los archivos implementados y su funcionalidad:

### cosine.py
```bash
import math

def coseno_similitud(u, v):
  # Inicializar variables para los sumatorios
  sum_uu = 0
  sum_vv = 0
  sum_uv = 0

  # Contar el número de ítems compartidos
  count = 0

  for i in range(len(u)):
    if u[i] != '-' and v[i] != '-':  # Ignorar elementos no valorados
      count += 1
      u_val = float(u[i])
      v_val = float(v[i])

      # Calcular los componentes del sumatorio
      sum_uv += u_val * v_val
      sum_uu += u_val ** 2
      sum_vv += v_val ** 2

  # Si no hay ítems compartidos, retornar 0 (sin similitud)
  if count == 0:
    return 0

  # Calcular la similitud coseno
  denom = math.sqrt(sum_uu) * math.sqrt(sum_vv)
  if denom == 0:
    return 0  # Evitar división por 0
    
  return sum_uv / denom

'''
# Ejemplo de uso
usuario_1 = [3.0, 1.0, '-', 5.0, 4.0]
usuario_2 = [4.0, '-', 3.0, 5.0, '-']

similitud = coseno_similitud(usuario_1, usuario_2)
print("Similitud coseno:", similitud)
'''
```

La función `coseno_similitud(u, v)` calcula la similitud entre dos usuarios o ítems basándose en sus valoraciones, usando la métrica de similitud coseno. Esta técnica es común en sistemas de recomendación, ya que permite medir cuánto se parecen dos vectores analizando el ángulo entre ellos en un espacio n-dimensional.


1. **Explicación de la Función**

**Inicialización de Variables:**  
   La función comienza creando variables para almacenar los resultados intermedios necesarios para el cálculo de la similitud coseno. 

**Recorrido de Valoraciones Compartidas:**  
   La función itera sobre las valoraciones de los vectores `u` y `v`, que representan dos usuarios o ítems. Solo considera los ítems donde ambos usuarios han dado una valoración (ignora aquellos marcados como `'-'`, indicando ítems sin valorar).

**Acumulación de Valores:**  
   Durante la iteración:
   - Calcula el producto de cada par de valoraciones y lo acumula para el cálculo de similitud.
   - Suma los cuadrados de cada valoración de ambos usuarios o ítems.
   
**Calculo de Similitud Coseno:**  
   Al finalizar, calcula la similitud coseno dividiendo la suma de productos de valoraciones compartidas por el producto de las raíces cuadradas de los sumatorios de cuadrados. Si el denominador es cero (lo que ocurre si alguno de los vectores no tiene valoraciones en común), la función retorna `0` para indicar que no hay similitud.

---

### euclidea.py
```bash

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

```

La función `similitud_euclidea(usuario1, usuario2)` mide la similitud entre dos usuarios utilizando la distancia euclídea entre sus valoraciones. Esta métrica es especialmente útil en sistemas de recomendación, ya que ayuda a identificar qué tan diferentes o parecidos son dos usuarios o ítems en función de la "distancia" entre sus valoraciones. La distancia euclídea es inversamente proporcional a la similitud: cuanto menor es la distancia, mayor es la similitud.

1. **Explicación de la Función**

**Extensión de las Listas:**  
   La función extiende ambas listas de usuarios a la misma longitud para asegurar que tengan la misma cantidad de ítems, rellenando las posiciones faltantes con el símbolo `'-'`, lo que indica valoraciones no disponibles.

**Cálculo de la Suma de Cuadrados:**  
   La función itera sobre las valoraciones en común entre los usuarios:
   - Para cada ítem, si ambos usuarios tienen valoraciones válidas (ignorando `'-'` y `-1`), calcula el cuadrado de la diferencia y lo suma al total.
   - Lleva un recuento de los ítems con valoraciones válidas, ya que si no existen ítems compartidos no se puede calcular una similitud significativa.

**Cálculo de la Distancia y la Similitud:**  
   Después de acumular la suma de los cuadrados, calcula la raíz cuadrada para obtener la distancia euclídea. Luego, convierte la distancia en una medida de similitud mediante la fórmula inversa `1 / (1 + distancia)`. Si no hay ítems comunes, retorna 0 para indicar ausencia de similitud.


### pearson.py
```bash

def pearson (i, j):
  """
    Calcula la correlación de Pearson entre dos listas de calificaciones.
    
    Args:
        i (list): Lista de calificaciones del primer usuario.
        j (list): Lista de calificaciones del segundo usuario.
    
    Returns:
        float: Correlación de Pearson entre las dos listas de calificaciones.
  """
  valid_i = [element for element in i if element != "-"]
  valid_j = [element for element in j if element != "-"]

  media_i = sum(valid_i) / len(valid_i)
  media_j = sum(valid_j) / len(valid_j)

  numerator = 0
  first_denom = 0
  second_denom = 0

  for element_i, element_j in zip(i,j):
    if (element_i != "-" and element_j != "-"):
      numerator += (element_i - media_i) * (element_j - media_j)
      first_denom += (element_i - media_i) ** 2
      second_denom += (element_j - media_j) ** 2
  
  denom = (first_denom ** 0.5) * (second_denom ** 0.5)

  return (numerator / denom) if denom != 0 else 0
```

Se define la función pearson, que calcula la correlación de Pearson entre dos usuarios. Esta métrica es útil para capturar la relación lineal entre las calificaciones de dos usuarios, ignorando cualquier desplazamiento promedio.

1. **Explicación de la Función**

**Cálculo de las Medias:**  
   La función primero filtra los elementos con calificación válida (ignorando aquellos marcados como `"-"`). Luego calcula las medias de las valoraciones válidas para cada usuario (`media_i` para el primer usuario y `media_j` para el segundo usuario).

**Cálculo del Numerador y los Denominadores:**  
   A continuación, se procede a calcular los componentes necesarios para la fórmula de Pearson:
   - **Numerador:** Calcula la covarianza, que mide el grado en que las valoraciones de los dos usuarios se desvían en la misma dirección respecto a sus respectivas medias.
   - **Denominadores:** Calcula las sumas de los cuadrados de las diferencias entre cada valoración y la media para cada usuario, lo que normaliza la covarianza en la fórmula de Pearson.

**Cálculo de la Correlación de Pearson:**  
   Finalmente, la función calcula el valor de la correlación como `numerator / denom`, donde:
   - `denom` es la raíz cuadrada de los productos de las sumas de los cuadrados de cada usuario.
   - Si `denom` es 0 (caso en que uno o ambos usuarios tienen valoraciones constantes), la función retorna 0, indicando que no se puede calcular una correlación significativa.


### recomendador.py
```bash 

from cosine import coseno_similitud
from euclidea import similitud_euclidea
from pearson import pearson
import argparse



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
        f.readline()
        f.readline()
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
        # Excluir al propio usuario
        vecinos_ordenados = sorted([(j, sim_j) for j, sim_j in enumerate(sim) if j != i], key=lambda x: x[1], reverse=True)
        # Seleccionar los k vecinos más cercanos
        vecinos.append([vecino[0] for vecino in vecinos_ordenados[:k]])
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
        if vecino < len(matriz) and item < len(matriz[vecino]):  # Verificar que los índices sean válidos
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
        return media_usuario  # Evitar división por cero
    
    return media_usuario + (numerador / denominador)


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


# EJEMPLO DE EJECUCION: python3 recomendador.py --archivo matriz.txt --metrica euclidea --vecinos 3 --tipo_prediccion media

def main():
    # Configurar el analizador de argumentos
    parser = argparse.ArgumentParser(description='Sistema de recomendación basado en diferentes métricas y tipos de predicción.')
    parser.add_argument('--archivo', type=str, required=True, help='Ruta al archivo de la matriz de utilidad')
    parser.add_argument('--metrica', type=str, required=True, choices=['pearson', 'coseno', 'euclidea'], help='Métrica elegida: pearson, coseno o euclidea')
    parser.add_argument('--vecinos', type=int, required=True, help='Número de vecinos considerado')
    parser.add_argument('--tipo_prediccion', type=str, required=True, choices=['simple', 'media'], help='Tipo de predicción: simple o media')

    # Parsear los argumentos
    args = parser.parse_args()

    # Asignar los argumentos a variables
    archivo = args.archivo
    metrica = args.metrica
    k = args.vecinos
    tipo_prediccion = args.tipo_prediccion

    # Cargar la matriz de utilidad
    matriz = cargar_matriz_utilidad(archivo)
    # Calcular la matriz de similitud
    matriz_similitud = calcular_similitud_matriz(matriz, metrica)
    # Seleccionar los vecinos
    vecinos = seleccionar_vecinos(matriz_similitud, k)
    
    # Predecir valores faltantes
    for usuario in range(len(matriz)):
        for item in range(len(matriz[usuario])):
            if matriz[usuario][item] == '-':
                if tipo_prediccion == 'simple':
                    matriz[usuario][item] = prediccion_simple(usuario, vecinos[usuario], matriz, matriz_similitud, item)
                elif tipo_prediccion == 'media':
                    matriz[usuario][item] = prediccion_con_media(usuario, vecinos[usuario], matriz, matriz_similitud, item)
    
    # Imprimir los resultados
    imprimir_resultados(matriz, matriz_similitud, vecinos)

if __name__ == "__main__":
    main()
```

Este código implementa un sistema de recomendación utilizando **filtrado colaborativo** mediante tres métricas de similitud: **coseno**, **euclídea** y **correlación de Pearson**. Se describe a continuación las principales funciones. 

**FUNCIONES PRINCIPALES Y FLUJO GENERAL**
 
**`cargar_matriz_utilidad(archivo)`**
   - Carga y procesa la matriz de utilidad desde un archivo, donde cada fila corresponde a un usuario y cada columna a un ítem.
   - Convierte cada valor a `float`, manteniendo los valores faltantes como `"-"`.

**`calcular_similitud_matriz(matriz, metrica)`**
   - Calcula la **similitud** entre todos los usuarios de la matriz utilizando la métrica especificada:
     - **coseno**: Utiliza la similitud de coseno para evaluar cuán similares son las preferencias de dos usuarios.
     - **euclidea**: Calcula la distancia euclídea inversa, siendo más alta para usuarios con valoraciones cercanas.
     - **pearson**: Mide la correlación lineal entre las valoraciones de dos usuarios.

**`seleccionar_vecinos(similitudes, k)`**
   - Selecciona los `k` usuarios más similares para cada usuario en la matriz de similitud calculada.
   - Ordena y selecciona los vecinos en función de los valores de similitud de mayor a menor.

**`prediccion_simple(usuario, vecinos, matriz, similitudes, item)`**
   - Realiza una **predicción simple** de la calificación faltante para un usuario e ítem específicos.
   - La predicción es un promedio ponderado de las valoraciones de los vecinos, donde los pesos son las similitudes entre los usuarios.

**`prediccion_con_media(usuario, vecinos, matriz, similitudes, item)`**
   - Realiza la **predicción basada en la diferencia con la media** de los usuarios.
   - Considera la desviación de cada vecino respecto a su media, ajustando la predicción para que sea relativa a la media del usuario en cuestión.

**`imprimir_resultados(matriz, matriz_similitud, vecinos)`**
   - Imprime:
     - La matriz de utilidad, incluyendo las predicciones generadas.
     - La matriz de similitudes entre usuarios.
     - Los vecinos seleccionados para cada usuario.


## USO DEL PROGRAMA
Este sistema puede ejecutarse en la terminal mediante:
```bash
python3 recomendador.py --archivo matriz.txt --metrica euclidea --vecinos 3 --tipo_prediccion media
```
Argumentos de entrada:
--archivo: Ruta al archivo de texto que contiene la matriz de utilidad.
--metrica: La métrica de similitud que se usará, puede ser pearson, coseno o euclidea.
--vecinos: Número de vecinos a considerar en el cálculo de predicciones.
--tipo_prediccion: Tipo de predicción a realizar, ya sea simple o media.

# Ejemplos de uso de la aplicación