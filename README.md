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

Con el entorno virtual activado, instala las bibliotecas necesarias para el sistema de recomendación utilizando pip. En el caso de este proyecto, las bibliotecas a instalar son numpy y colorama:

```bash
pip install numpy
pip install colorama
```

Estas instrucciones permitirán configurar el entorno de Python en Linux e instalar las bibliotecas necesarias para el sistema de recomendación.

--- 

# Explicación del código implementado
El sistema de recomendación consta de varios módulos, cada uno responsable de una métrica de similitud o una funcionalidad particular. A continuación, se detallan los archivos implementados y su funcionalidad:

### cosine.py
```bash
import math

def coseno_similitud(u, v):
  """
    Calcula la similitud coseno entre dos listas de valoraciones.
    
    Args:
        u (list): Lista de calificaciones del primer usuario.
        v (list): Lista de calificaciones del segundo usuario.
    
    Returns:
        float: Correlación de coseno entre las dos listas de calificaciones.
  """
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
```

La función `coseno_similitud(u, v)` calcula la similitud entre dos usuarios o ítems basándose en sus valoraciones de una serie de items, usando la métrica de similitud coseno. Esta técnica es común en sistemas de recomendación, ya que permite medir cuánto se parecen dos vectores analizando el ángulo entre ellos en un espacio n-dimensional.


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
    Calcula la correlación de Pearson entre dos listas de valoraciones.
    
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

Este código implementa un sistema de recomendación utilizando **filtrado colaborativo** mediante tres métricas de similitud: **coseno**, **euclídea** y **correlación de Pearson**. Se describe a continuación las principales funciones. 

**FUNCIONES PRINCIPALES Y FLUJO GENERAL**

**`Importamos los métodos`**
```python
from cosine import coseno_similitud
from euclidea import similitud_euclidea
from pearson import pearson
import argparse
from colorama import Fore, Style, init
```
Importamos los métodos que desarrollamos para calcular las similitudes (`cosine`, `euclidea`, `pearson`), `argparse` para gestionar los parámetros por línea de comandos y `colorama` para poder darle color a la salida por consola.

**`cargar_matriz_utilidad(archivo)`**
```python
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
```
   - Carga y procesa la matriz de utilidad desde un archivo, donde cada fila corresponde a un usuario y cada columna a un ítem.
   - Convierte cada valor a `float`, manteniendo los valores faltantes como `"-"`.

**`calcular_similitud_matriz(matriz, metrica)`**
```python
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
```
   - Calcula la **similitud** de cada usuario con el resto utilizando la métrica especificada:
     - **coseno**: Utiliza la similitud de coseno para evaluar cuán similares son las preferencias de dos usuarios.
     - **euclidea**: Calcula la distancia euclídea inversa, siendo más alta para usuarios con valoraciones cercanas.
     - **pearson**: Mide la correlación lineal entre las valoraciones de dos usuarios.

**`seleccionar_vecinos(similitudes, k)`**
```python
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
```
   - Selecciona los `k` usuarios más similares para cada usuario en la matriz de similitud calculada.
   - Ordena y selecciona los vecinos en función de los valores de similitud de mayor a menor.

**`prediccion_simple(usuario, vecinos, matriz, similitudes, item, min_val)`**
```python
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

```
   - Realiza una **predicción simple** de la calificación faltante para un usuario e ítem específicos.
   - La predicción es un promedio ponderado de las valoraciones de los vecinos, donde los pesos son las similitudes entre los usuarios.
   - Si la predicción es inferior al valor mínimo que puede tener una calificacion, se devuelve este valor mínimo.
   - Redondea la prediccion a 2 decimales.

**`prediccion_con_media(usuario, vecinos, matriz, similitudes, item)`**
```python
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
```
   - Realiza la **predicción basada en la diferencia con la media** de los usuarios.
   - Considera la desviación de cada vecino respecto a su media, ajustando la predicción para que sea relativa a la media del usuario en cuestión.
   - Si la predicción es inferior al valor mínimo que puede tener una calificacion, se devuelve este valor mínimo.
   - Redondea la prediccion a 2 decimales.

**`imprimir_resultados(matriz, matriz_similitud, vecinos, predicciones)`**
```python
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
```
   - Imprime:
     - La matriz de utilidad, incluyendo las predicciones generadas en color rojo.
     - La matriz de similitudes entre usuarios.
     - Los vecinos seleccionados para cada usuario.
     - Las predicciones generadas con la métrica especificada.

**`Función main()`**
```python
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
```

    - En primer lugar se gestionan los argumentos que se pasan por línea de comandos.
    - Se carga la matriz de utilidad y se calcula la matriz similitud y vecinos.
    - Para aquellos items que un usuario no ha valorado, se calcula la predicción, se añade en la matriz utilidad y se guarda en una lista para imprimirla posteriormente. Nótese que el añadir la predicción a la matriz utilidad no afecta a predicciones posteriores puesto que ya se ha calculado la matriz similitud y la lista con los vecinos para todos los usuarios.
    - Se imprimen los resultados.

## USO DEL PROGRAMA
Este sistema puede ejecutarse en la terminal mediante:
```bash
python3 recomendador.py --archivo matriz.txt --metrica euclidea --vecinos 3 --tipo_prediccion media
```
Argumentos de entrada:

-a, --archivo: Ruta al archivo de texto que contiene la matriz de utilidad.

-m, --metrica: La métrica de similitud que se usará, puede ser pearson, coseno o euclidea.

-v, --vecinos: Número de vecinos a considerar en el cálculo de predicciones.

-t, --tipo_prediccion: Tipo de predicción a realizar, ya sea simple o media.

# Ejemplos de uso de la aplicación
Para probar estos ejemplo, haremos uso de la matriz siguiente:
```bash
0.000
5.000
2.809 4.309 3.096 4.281 3.292 1.814 2.385 0.632 3.315 2.851 0.979 3.614 2.985 4.434 - 0.344 1.252 0.352 4.952 4.621 0.175 0.125 1.579 - 2.162 
2.281 1.313 3.766 3.074 2.332 4.182 3.447 3.282 2.460 4.735 2.162 4.164 4.519 3.633 4.509 0.903 1.390 1.984 0.946 3.543 2.756 1.559 2.191 2.756 3.487 
1.760 2.950 3.991 2.567 - 2.314 1.016 0.298 1.171 4.962 3.094 1.094 0.845 0.370 4.234 0.574 2.692 1.444 - 2.050 3.081 0.957 - 2.912 2.444 
1.865 - 2.964 1.533 0.277 4.743 2.883 3.848 - 2.949 - 4.705 2.487 4.236 1.461 2.874 4.661 3.312 0.194 1.684 2.047 4.108 - 2.233 2.692 
3.848 - - 2.324 2.349 0.828 2.033 2.012 1.982 4.685 3.083 3.094 2.766 2.462 2.381 4.025 0.570 0.931 2.430 0.396 3.639 4.827 - 2.428 1.358 
2.376 4.643 1.234 4.000 2.087 4.461 2.112 0.107 - 4.454 2.418 2.548 2.948 - 4.345 3.659 1.448 1.196 2.142 2.170 2.196 2.147 1.236 2.957 2.254 
1.609 3.284 4.143 4.910 0.353 4.098 3.987 2.310 4.039 4.628 3.333 1.999 3.675 4.834 4.557 4.072 1.439 0.741 1.278 3.433 0.149 1.336 0.515 3.930 0.835 
1.523 4.484 0.616 4.857 2.213 4.700 1.681 1.942 0.155 1.890 4.804 1.458 0.242 3.256 0.417 1.716 3.631 3.249 1.419 4.043 1.370 2.850 2.468 0.288 0.114 
0.964 3.248 1.031 2.464 4.486 - - 2.693 0.085 1.562 3.830 1.183 4.497 2.321 1.461 0.523 - 0.061 0.146 - 2.928 3.274 2.916 3.944 4.920 
1.416 - 4.181 1.314 4.041 4.529 4.884 2.779 3.839 4.924 0.072 1.167 1.574 0.927 1.716 3.700 3.867 0.970 4.303 3.483 1.890 3.800 4.223 - - 
```

## Ejemplo 1 --> Usando la métrica de similitud de Pearson y tipo de predicción media.
```bash
python3 recomendador.py --archivo matriz.txt --metrica pearson --vecinos 3 --tipo_prediccion media
```
El resultado de este ejemplo será el siguiente que vemos:
```bash
Matriz de utilidad con predicciones:
[ 2.809 4.309 3.096 4.281 3.292 1.814 2.385 0.632 3.315 2.851 0.979 3.614 2.985 4.434 4.2 0.344 1.252 0.352 4.952 4.621 0.175 0.125 1.579 3.09 2.162 ]
[ 2.281 1.313 3.766 3.074 2.332 4.182 3.447 3.282 2.46 4.735 2.162 4.164 4.519 3.633 4.509 0.903 1.39 1.984 0.946 3.543 2.756 1.559 2.191 2.756 3.487 ]
[ 1.76 2.95 3.991 2.567 1.26 2.314 1.016 0.298 1.171 4.962 3.094 1.094 0.845 0.37 4.234 0.574 2.692 1.444 1.01 2.05 3.081 0.957 0.73 2.912 2.444 ]
[ 1.865 3.48 2.964 1.533 0.277 4.743 2.883 3.848 1.96 2.949 3.9 4.705 2.487 4.236 1.461 2.874 4.661 3.312 0.194 1.684 2.047 4.108 2.22 2.233 2.692 ]
[ 3.848 4.2 2.09 2.324 2.349 0.828 2.033 2.012 1.982 4.685 3.083 3.094 2.766 2.462 2.381 4.025 0.57 0.931 2.43 0.396 3.639 4.827 1.13 2.428 1.358 ]
[ 2.376 4.643 1.234 4.0 2.087 4.461 2.112 0.107 3.07 4.454 2.418 2.548 2.948 3.48 4.345 3.659 1.448 1.196 2.142 2.17 2.196 2.147 1.236 2.957 2.254 ]
[ 1.609 3.284 4.143 4.91 0.353 4.098 3.987 2.31 4.039 4.628 3.333 1.999 3.675 4.834 4.557 4.072 1.439 0.741 1.278 3.433 0.149 1.336 0.515 3.93 0.835 ]
[ 1.523 4.484 0.616 4.857 2.213 4.7 1.681 1.942 0.155 1.89 4.804 1.458 0.242 3.256 0.417 1.716 3.631 3.249 1.419 4.043 1.37 2.85 2.468 0.288 0.114 ]
[ 0.964 3.248 1.031 2.464 4.486 3.77 2.34 2.693 0.085 1.562 3.83 1.183 4.497 2.321 1.461 0.523 2.15 0.061 0.146 3.26 2.928 3.274 2.916 3.944 4.92 ]
[ 1.416 3.93 4.181 1.314 4.041 4.529 4.884 2.779 3.839 4.924 0.072 1.167 1.574 0.927 1.716 3.7 3.867 0.97 4.303 3.483 1.89 3.8 4.223 3.71 3.33 ]

Matriz de similitudes:
[0, 0.2367276525808474, 0.12181680268855179, -0.42091911073678084, -0.1963743090231027, 0.33927861578642043, 0.3752905175399032, 0.02153421951288432, -0.10075629172585003, 0.03248236051139243]
[0.2367276525808474, 0, 0.2418777668986924, 0.17000426346725436, -0.08191365519533665, 0.22656023954837196, 0.44622274730976463, -0.243210009862165, 0.16082645814382215, -0.09980662008288013]
[0.12181680268855179, 0.2418777668986924, 0, -0.36855760688243894, 0.07269275607171184, 0.4153036519635081, 0.15787512911611704, 0.002341937722947724, 0.06016825686048832, 0.14760708234930783]
[-0.42091911073678084, 0.17000426346725436, -0.36855760688243894, 0, -0.07229829624214154, -0.11733073960359801, 0.12285942125693958, 0.2678406900988734, -0.0650679900197235, -0.037586397244808833]
[-0.1963743090231027, -0.08191365519533665, 0.07269275607171184, -0.07229829624214154, 0, 0.27088749427553327, 0.03255772051461206, -0.24897091371943947, -0.03734900838150185, -0.06519057788300603]
[0.33927861578642043, 0.22656023954837196, 0.4153036519635081, -0.11733073960359801, 0.27088749427553327, 0, 0.6043870248581101, 0.17296977927266557, 0.00800059455323475, -0.008016553164480236]
[0.3752905175399032, 0.44622274730976463, 0.15787512911611704, 0.12285942125693958, 0.03255772051461206, 0.6043870248581101, 0, 0.07579858009245745, -0.1720594269864079, -0.0074532104051489925]
[0.02153421951288432, -0.243210009862165, 0.002341937722947724, 0.2678406900988734, -0.24897091371943947, 0.17296977927266557, 0.07579858009245745, 0, 0.0880076382883248, -0.15874933997688664]
[-0.10075629172585003, 0.16082645814382215, 0.06016825686048832, -0.0650679900197235, -0.03734900838150185, 0.00800059455323475, -0.1720594269864079, 0.0880076382883248, 0, -0.11363678994892266]
[0.03248236051139243, -0.09980662008288013, 0.14760708234930783, -0.037586397244808833, -0.06519057788300603, -0.008016553164480236, -0.0074532104051489925, -0.15874933997688664, -0.11363678994892266, 0]

Vecinos seleccionados para cada usuario:
Usuario 0: Vecinos [6, 5, 1]
Usuario 1: Vecinos [6, 2, 0]
Usuario 2: Vecinos [5, 1, 6]
Usuario 3: Vecinos [7, 1, 6]
Usuario 4: Vecinos [5, 2, 6]
Usuario 5: Vecinos [6, 2, 0]
Usuario 6: Vecinos [5, 1, 0]
Usuario 7: Vecinos [3, 5, 8]
Usuario 8: Vecinos [1, 7, 2]
Usuario 9: Vecinos [2, 0, 6]

Predicciones de valoraciones de usuarios:
Usuario 0 - Ítem 14: 4.2
Usuario 0 - Ítem 23: 3.09
Usuario 2 - Ítem 4: 1.26
Usuario 2 - Ítem 18: 1.01
Usuario 2 - Ítem 22: 0.73
Usuario 3 - Ítem 1: 3.48
Usuario 3 - Ítem 8: 1.96
Usuario 3 - Ítem 10: 3.9
Usuario 3 - Ítem 22: 2.22
Usuario 4 - Ítem 1: 4.2
Usuario 4 - Ítem 2: 2.09
Usuario 4 - Ítem 22: 1.13
Usuario 5 - Ítem 8: 3.07
Usuario 5 - Ítem 13: 3.48
Usuario 8 - Ítem 5: 3.77
Usuario 8 - Ítem 6: 2.34
Usuario 8 - Ítem 16: 2.15
Usuario 8 - Ítem 19: 3.26
Usuario 9 - Ítem 1: 3.93
Usuario 9 - Ítem 23: 3.71
Usuario 9 - Ítem 24: 3.33
```

## Ejemplo 2 --> Usando la métrica de similitud coseno y tipo de predicción media.
```bash
python3 recomendador.py --archivo matriz.txt --metrica coseno --vecinos 3 --tipo_prediccion media
```
Para este caso, el resultado será el siguiente:
```bash
Matriz de utilidad con predicciones:
[ 2.809 4.309 3.096 4.281 3.292 1.814 2.385 0.632 3.315 2.851 0.979 3.614 2.985 4.434 4.19 0.344 1.252 0.352 4.952 4.621 0.175 0.125 1.579 3.0 2.162 ]
[ 2.281 1.313 3.766 3.074 2.332 4.182 3.447 3.282 2.46 4.735 2.162 4.164 4.519 3.633 4.509 0.903 1.39 1.984 0.946 3.543 2.756 1.559 2.191 2.756 3.487 ]
[ 1.76 2.95 3.991 2.567 1.01 2.314 1.016 0.298 1.171 4.962 3.094 1.094 0.845 0.37 4.234 0.574 2.692 1.444 0.81 2.05 3.081 0.957 0.62 2.912 2.444 ]
[ 1.865 3.11 2.964 1.533 0.277 4.743 2.883 3.848 2.37 2.949 3.53 4.705 2.487 4.236 1.461 2.874 4.661 3.312 0.194 1.684 2.047 4.108 1.9 2.233 2.692 ]
[ 3.848 2.85 2.76 2.324 2.349 0.828 2.033 2.012 1.982 4.685 3.083 3.094 2.766 2.462 2.381 4.025 0.57 0.931 2.43 0.396 3.639 4.827 1.09 2.428 1.358 ]
[ 2.376 4.643 1.234 4.0 2.087 4.461 2.112 0.107 2.61 4.454 2.418 2.548 2.948 3.0 4.345 3.659 1.448 1.196 2.142 2.17 2.196 2.147 1.236 2.957 2.254 ]
[ 1.609 3.284 4.143 4.91 0.353 4.098 3.987 2.31 4.039 4.628 3.333 1.999 3.675 4.834 4.557 4.072 1.439 0.741 1.278 3.433 0.149 1.336 0.515 3.93 0.835 ]
[ 1.523 4.484 0.616 4.857 2.213 4.7 1.681 1.942 0.155 1.89 4.804 1.458 0.242 3.256 0.417 1.716 3.631 3.249 1.419 4.043 1.37 2.85 2.468 0.288 0.114 ]
[ 0.964 3.248 1.031 2.464 4.486 2.86 2.25 2.693 0.085 1.562 3.83 1.183 4.497 2.321 1.461 0.523 0.84 0.061 0.146 1.7 2.928 3.274 2.916 3.944 4.92 ]
[ 1.416 3.18 4.181 1.314 4.041 4.529 4.884 2.779 3.839 4.924 0.072 1.167 1.574 0.927 1.716 3.7 3.867 0.97 4.303 3.483 1.89 3.8 4.223 2.82 2.98 ]

Matriz de similitudes:
[0, 0.8354148401290216, 0.7474341978966083, 0.667008293376464, 0.6963173750981585, 0.8349074654746086, 0.8330095957055638, 0.7271228832342438, 0.6670929533459892, 0.7573988630713611]
[0.8354148401290216, 0, 0.8492207002222775, 0.870751459296185, 0.8260625400835315, 0.8771404780971275, 0.8913235291464705, 0.7160878437464523, 0.809356177074145, 0.8110282952581811]
[0.7474341978966083, 0.8492207002222775, 0, 0.730909443818667, 0.774156733694782, 0.8793584514761291, 0.8118698400934873, 0.6973591708663172, 0.7283300741929014, 0.7667821444975077]
[0.667008293376464, 0.870751459296185, 0.730909443818667, 0, 0.787656802976235, 0.8004648067756932, 0.8093520271189034, 0.8122667883609671, 0.7298401374812873, 0.8008826074002988]
[0.6963173750981585, 0.8260625400835315, 0.774156733694782, 0.787656802976235, 0, 0.8700353311820423, 0.7920060928454171, 0.6758603272578847, 0.7665501032687941, 0.7773430229297237]
[0.8349074654746086, 0.8771404780971275, 0.8793584514761291, 0.8004648067756932, 0.8700353311820423, 0, 0.9122590260346779, 0.7949680273136751, 0.7740515489843617, 0.8062913393391464]
[0.8330095957055638, 0.8913235291464705, 0.8118698400934873, 0.8093520271189034, 0.7920060928454171, 0.9122590260346779, 0, 0.7391801563013224, 0.6680352698250531, 0.7713830529203723]
[0.7271228832342438, 0.7160878437464523, 0.6973591708663172, 0.8122667883609671, 0.6758603272578847, 0.7949680273136751, 0.7391801563013224, 0, 0.7006666422574691, 0.717336363552049]
[0.6670929533459892, 0.809356177074145, 0.7283300741929014, 0.7298401374812873, 0.7665501032687941, 0.7740515489843617, 0.6680352698250531, 0.7006666422574691, 0, 0.6684880503107963]
[0.7573988630713611, 0.8110282952581811, 0.7667821444975077, 0.8008826074002988, 0.7773430229297237, 0.8062913393391464, 0.7713830529203723, 0.717336363552049, 0.6684880503107963, 0]

Vecinos seleccionados para cada usuario:
Usuario 0: Vecinos [1, 5, 6]
Usuario 1: Vecinos [6, 5, 3]
Usuario 2: Vecinos [5, 1, 6]
Usuario 3: Vecinos [1, 7, 6]
Usuario 4: Vecinos [5, 1, 6]
Usuario 5: Vecinos [6, 2, 1]
Usuario 6: Vecinos [5, 1, 0]
Usuario 7: Vecinos [3, 5, 6]
Usuario 8: Vecinos [1, 5, 4]
Usuario 9: Vecinos [1, 5, 3]

Predicciones de valoraciones de usuarios:
Usuario 0 - Ítem 14: 4.19
Usuario 0 - Ítem 23: 3.0
Usuario 2 - Ítem 4: 1.01
Usuario 2 - Ítem 18: 0.81
Usuario 2 - Ítem 22: 0.62
Usuario 3 - Ítem 1: 3.11
Usuario 3 - Ítem 8: 2.37
Usuario 3 - Ítem 10: 3.53
Usuario 3 - Ítem 22: 1.9
Usuario 4 - Ítem 1: 2.85
Usuario 4 - Ítem 2: 2.76
Usuario 4 - Ítem 22: 1.09
Usuario 5 - Ítem 8: 2.61
Usuario 5 - Ítem 13: 3.0
Usuario 8 - Ítem 5: 2.86
Usuario 8 - Ítem 6: 2.25
Usuario 8 - Ítem 16: 0.84
Usuario 8 - Ítem 19: 1.7
Usuario 9 - Ítem 1: 3.18
Usuario 9 - Ítem 23: 2.82
Usuario 9 - Ítem 24: 2.98
```

## Ejemplo 3 --> Usando la métrica de similitud euclidea y tipo de predicción media.
```bash
python3 recomendador.py --archivo matriz.txt --metrica euclidea --vecinos 3 --tipo_prediccion media
```
Para este caso, el resultado será:
```bash
Matriz de utilidad con predicciones:
[ 2.809 4.309 3.096 4.281 3.292 1.814 2.385 0.632 3.315 2.851 0.979 3.614 2.985 4.434 4.29 0.344 1.252 0.352 4.952 4.621 0.175 0.125 1.579 2.88 2.162 ]
[ 2.281 1.313 3.766 3.074 2.332 4.182 3.447 3.282 2.46 4.735 2.162 4.164 4.519 3.633 4.509 0.903 1.39 1.984 0.946 3.543 2.756 1.559 2.191 2.756 3.487 ]
[ 1.76 2.95 3.991 2.567 1.74 2.314 1.016 0.298 1.171 4.962 3.094 1.094 0.845 0.37 4.234 0.574 2.692 1.444 1.34 2.05 3.081 0.957 1.04 2.912 2.444 ]
[ 1.865 3.61 2.964 1.533 0.277 4.743 2.883 3.848 1.6 2.949 3.28 4.705 2.487 4.236 1.461 2.874 4.661 3.312 0.194 1.684 2.047 4.108 2.18 2.233 2.692 ]
[ 3.848 3.08 2.89 2.324 2.349 0.828 2.033 2.012 1.982 4.685 3.083 3.094 2.766 2.462 2.381 4.025 0.57 0.931 2.43 0.396 3.639 4.827 1.49 2.428 1.358 ]
[ 2.376 4.643 1.234 4.0 2.087 4.461 2.112 0.107 2.56 4.454 2.418 2.548 2.948 2.72 4.345 3.659 1.448 1.196 2.142 2.17 2.196 2.147 1.236 2.957 2.254 ]
[ 1.609 3.284 4.143 4.91 0.353 4.098 3.987 2.31 4.039 4.628 3.333 1.999 3.675 4.834 4.557 4.072 1.439 0.741 1.278 3.433 0.149 1.336 0.515 3.93 0.835 ]
[ 1.523 4.484 0.616 4.857 2.213 4.7 1.681 1.942 0.155 1.89 4.804 1.458 0.242 3.256 0.417 1.716 3.631 3.249 1.419 4.043 1.37 2.85 2.468 0.288 0.114 ]
[ 0.964 3.248 1.031 2.464 4.486 3.47 2.07 2.693 0.085 1.562 3.83 1.183 4.497 2.321 1.461 0.523 1.71 0.061 0.146 2.42 2.928 3.274 2.916 3.944 4.92 ]
[ 1.416 4.17 4.181 1.314 4.041 4.529 4.884 2.779 3.839 4.924 0.072 1.167 1.574 0.927 1.716 3.7 3.867 0.97 4.303 3.483 1.89 3.8 4.223 3.2 2.97 ]

Matriz de similitudes:
[0, 0.10969661068286898, 0.10742271156357089, 0.08499125019020504, 0.09265859484987722, 0.12140317918669213, 0.10742214562858425, 0.09027128059140783, 0.0905984242856575, 0.09090221237703781]
[0.10969661068286898, 0, 0.11134779397570664, 0.11987290666433104, 0.10758240675726705, 0.12359067248841527, 0.12026540067002073, 0.08342605250079974, 0.10804580113251287, 0.09804864961052485]
[0.10742271156357089, 0.11134779397570664, 0, 0.09494962714562988, 0.11193298050717655, 0.1374357842155823, 0.09656135928234208, 0.09399332850324404, 0.10825505030030215, 0.10406667082967791]
[0.08499125019020504, 0.11987290666433104, 0.09494962714562988, 0, 0.10464318422193736, 0.10903983029879585, 0.10134042717488913, 0.10945096376979375, 0.10545135392315752, 0.10266523179723798]
[0.09265859484987722, 0.10758240675726705, 0.11193298050717655, 0.10464318422193736, 0, 0.13491475080542567, 0.09774354666430023, 0.08922751581255509, 0.10613270483921962, 0.100086451679856]
[0.12140317918669213, 0.12359067248841527, 0.1374357842155823, 0.10903983029879585, 0.13491475080542567, 0, 0.14281857771449294, 0.10485119347871413, 0.10707904525408557, 0.10293737445469175]
[0.10742214562858425, 0.12026540067002073, 0.09656135928234208, 0.10134042717488913, 0.09774354666430023, 0.14281857771449294, 0, 0.0842849445663596, 0.08237016165132205, 0.08888351231341618]
[0.09027128059140783, 0.08342605250079974, 0.09399332850324404, 0.10945096376979375, 0.08922751581255509, 0.10485119347871413, 0.0842849445663596, 0, 0.0967525378193288, 0.08502202662587086]
[0.0905984242856575, 0.10804580113251287, 0.10825505030030215, 0.10545135392315752, 0.10613270483921962, 0.10707904525408557, 0.08237016165132205, 0.0967525378193288, 0, 0.09395825338270056]
[0.09090221237703781, 0.09804864961052485, 0.10406667082967791, 0.10266523179723798, 0.100086451679856, 0.10293737445469175, 0.08888351231341618, 0.08502202662587086, 0.09395825338270056, 0]

Vecinos seleccionados para cada usuario:
Usuario 0: Vecinos [5, 1, 2]
Usuario 1: Vecinos [5, 6, 3]
Usuario 2: Vecinos [5, 4, 1]
Usuario 3: Vecinos [1, 7, 5]
Usuario 4: Vecinos [5, 2, 1]
Usuario 5: Vecinos [6, 2, 4]
Usuario 6: Vecinos [5, 1, 0]
Usuario 7: Vecinos [3, 5, 8]
Usuario 8: Vecinos [2, 1, 5]
Usuario 9: Vecinos [2, 5, 3]

Predicciones de valoraciones de usuarios:
Usuario 0 - Ítem 14: 4.29
Usuario 0 - Ítem 23: 2.88
Usuario 2 - Ítem 4: 1.74
Usuario 2 - Ítem 18: 1.34
Usuario 2 - Ítem 22: 1.04
Usuario 3 - Ítem 1: 3.61
Usuario 3 - Ítem 8: 1.6
Usuario 3 - Ítem 10: 3.28
Usuario 3 - Ítem 22: 2.18
Usuario 4 - Ítem 1: 3.08
Usuario 4 - Ítem 2: 2.89
Usuario 4 - Ítem 22: 1.49
Usuario 5 - Ítem 8: 2.56
Usuario 5 - Ítem 13: 2.72
Usuario 8 - Ítem 5: 3.47
Usuario 8 - Ítem 6: 2.07
Usuario 8 - Ítem 16: 1.71
Usuario 8 - Ítem 19: 2.42
Usuario 9 - Ítem 1: 4.17
Usuario 9 - Ítem 23: 3.2
Usuario 9 - Ítem 24: 2.97
```

## Ejemplo 4 --> Usando la métrica de similitud de Pearson con predicción simple
```bash
python3 recomendador.py --archivo matriz.txt --metrica pearson --vecinos 3 --tipo_prediccion simple
```
Para este ejemplo, cambiaremos la matriz para probar matrices más pequeñas:
```bash
0.000
5.000
0.678 4.460 - - 2.512 - 0.266 4.778 - 0.457 
3.769 1.624 - - 3.983 4.776 1.687 2.473 1.052 1.049 
3.541 4.815 - 4.884 - 2.396 - 4.169 0.582 - 
3.778 1.152 - 2.424 1.202 - - - 3.940 2.451 
0.183 3.793 1.195 2.069 - 0.951 0.358 - - 2.351
```
El resultado de dicha ejecucion es:
```bash
Matriz de utilidad con predicciones:
[ 0.678 4.46 1.2 3.57 2.512 1.81 0.266 4.778 0.61 0.457 ]
[ 3.769 1.624 1.2 0.71 3.983 4.776 1.687 2.473 1.052 1.049 ]
[ 3.541 4.815 1.2 4.884 2.64 2.396 0.37 4.169 0.582 1.31 ]
[ 3.778 1.152 0.0 2.424 1.202 0.0 0.0 0.0 3.94 2.451 ]
[ 0.183 3.793 1.195 2.069 0.77 0.951 0.358 2.56 0.14 2.351 ]

Matriz de similitudes:
[0, 0.046574482925552566, 0.8200547781952213, -0.7255785623019365, 0.7179802072914012]
[0.046574482925552566, 0, 0.07553219920098114, -0.1434100712495233, -0.5359894531306042]
[0.8200547781952213, 0.07553219920098114, 0, -0.7169668685959448, 0.6914168877271628]
[-0.7255785623019365, -0.1434100712495233, -0.7169668685959448, 0, -0.9313357891125387]
[0.7179802072914012, -0.5359894531306042, 0.6914168877271628, -0.9313357891125387, 0]

Vecinos seleccionados para cada usuario:
Usuario 0: Vecinos [2, 4, 1]
Usuario 1: Vecinos [2, 0, 3]
Usuario 2: Vecinos [0, 4, 1]
Usuario 3: Vecinos [1, 2, 0]
Usuario 4: Vecinos [0, 2, 1]

Predicciones de valoraciones de usuarios:
Usuario 0 - Ítem 2: 1.2
Usuario 0 - Ítem 3: 3.57
Usuario 0 - Ítem 5: 1.81
Usuario 0 - Ítem 8: 0.61
Usuario 1 - Ítem 2: 1.2
Usuario 1 - Ítem 3: 0.71
Usuario 2 - Ítem 2: 1.2
Usuario 2 - Ítem 4: 2.64
Usuario 2 - Ítem 6: 0.37
Usuario 2 - Ítem 9: 1.31
Usuario 3 - Ítem 2: 0.0
Usuario 3 - Ítem 5: 0.0
Usuario 3 - Ítem 6: 0.0
Usuario 3 - Ítem 7: 0.0
Usuario 4 - Ítem 4: 0.77
Usuario 4 - Ítem 7: 2.56
Usuario 4 - Ítem 8: 0.14
```

## Ejemplo 5 --> Usando la métrica de similitud coseno con predicción simple.
```bash
python3 recomendador.py --archivo matriz.txt --metrica coseno --vecinos 3 --tipo_prediccion simple
```
El resultado es:
```bash
Matriz de utilidad con predicciones:
[ 0.678 4.46 1.2 3.49 2.512 2.55 0.266 4.778 0.79 0.457 ]
[ 3.769 1.624 1.2 3.64 3.983 4.776 1.687 2.473 1.052 1.049 ]
[ 3.541 4.815 1.2 4.884 3.21 2.396 0.75 4.169 0.582 1.28 ]
[ 3.778 1.152 1.2 2.424 1.202 2.83 0.97 3.29 3.94 2.451 ]
[ 0.183 3.793 1.195 2.069 2.43 0.951 0.358 4.17 1.52 2.351 ]

Matriz de similitudes:
[0, 0.7054591645886906, 0.914577898770214, 0.4756819508806159, 0.8948026376983896]
[0.7054591645886906, 0, 0.8264731425785112, 0.7524261966412371, 0.47816221597020814]
[0.914577898770214, 0.8264731425785112, 0, 0.7020880552442968, 0.8745220448134532]
[0.4756819508806159, 0.7524261966412371, 0.7020880552442968, 0, 0.6137834016391546]
[0.8948026376983896, 0.47816221597020814, 0.8745220448134532, 0.6137834016391546, 0]

Vecinos seleccionados para cada usuario:
Usuario 0: Vecinos [2, 4, 1]
Usuario 1: Vecinos [2, 3, 0]
Usuario 2: Vecinos [0, 4, 1]
Usuario 3: Vecinos [1, 2, 4]
Usuario 4: Vecinos [0, 2, 3]

Predicciones de valoraciones de usuarios:
Usuario 0 - Ítem 2: 1.2
Usuario 0 - Ítem 3: 3.49
Usuario 0 - Ítem 5: 2.55
Usuario 0 - Ítem 8: 0.79
Usuario 1 - Ítem 2: 1.2
Usuario 1 - Ítem 3: 3.64
Usuario 2 - Ítem 2: 1.2
Usuario 2 - Ítem 4: 3.21
Usuario 2 - Ítem 6: 0.75
Usuario 2 - Ítem 9: 1.28
Usuario 3 - Ítem 2: 1.2
Usuario 3 - Ítem 5: 2.83
Usuario 3 - Ítem 6: 0.97
Usuario 3 - Ítem 7: 3.29
Usuario 4 - Ítem 4: 2.43
Usuario 4 - Ítem 7: 4.17
Usuario 4 - Ítem 8: 1.52
``` 

## Ejemplo 6 --> Usando la métrica de similitud euclidea con predicción simple
```bash
python3 recomendador.py --archivo matriz.txt --metrica euclidea --vecinos 3 --tipo_prediccion simple
```
```bash
Matriz de utilidad con predicciones:
[ 0.678 4.46 1.2 3.11 2.512 1.58 0.266 4.778 1.9 0.457 ]
[ 3.769 1.624 1.2 3.48 3.983 4.776 1.687 2.473 1.052 1.049 ]
[ 3.541 4.815 1.2 4.884 3.14 2.396 0.72 4.169 0.582 1.18 ]
[ 3.778 1.152 1.2 2.424 1.202 2.5 0.8 3.54 3.94 2.451 ]
[ 0.183 3.793 1.195 2.069 2.32 0.951 0.358 4.29 2.11 2.351 ]

Matriz de similitudes:
[0, 0.16029036721763604, 0.25326048447475624, 0.16331897047753596, 0.3257146020756649]
[0.16029036721763604, 0, 0.18662075315766444, 0.18962665961976485, 0.1434459519414205]
[0.25326048447475624, 0.18662075315766444, 0, 0.15267385145090367, 0.1746490123826326]
[0.16331897047753596, 0.18962665961976485, 0.15267385145090367, 0, 0.18261372503883191]
[0.3257146020756649, 0.1434459519414205, 0.1746490123826326, 0.18261372503883191, 0]

Vecinos seleccionados para cada usuario:
Usuario 0: Vecinos [4, 2, 3]
Usuario 1: Vecinos [3, 2, 0]
Usuario 2: Vecinos [0, 1, 4]
Usuario 3: Vecinos [1, 4, 0]
Usuario 4: Vecinos [0, 3, 2]

Predicciones de valoraciones de usuarios:
Usuario 0 - Ítem 2: 1.2
Usuario 0 - Ítem 3: 3.11
Usuario 0 - Ítem 5: 1.58
Usuario 0 - Ítem 8: 1.9
Usuario 1 - Ítem 2: 1.2
Usuario 1 - Ítem 3: 3.48
Usuario 2 - Ítem 2: 1.2
Usuario 2 - Ítem 4: 3.14
Usuario 2 - Ítem 6: 0.72
Usuario 2 - Ítem 9: 1.18
Usuario 3 - Ítem 2: 1.2
Usuario 3 - Ítem 5: 2.5
Usuario 3 - Ítem 6: 0.8
Usuario 3 - Ítem 7: 3.54
Usuario 4 - Ítem 4: 2.32
Usuario 4 - Ítem 7: 4.29
Usuario 4 - Ítem 8: 2.11
```
---

# Conclusión.
Este repositorio de GitHub incluye una guía completa donde se explican las dependencias necesarias, se revisa detalladamente el código desarrollado y se proponen ejemplos de uso práctico. Todo esto se ha estructurado para facilitar tanto la instalación como el entendimiento del software, permitiendo a los usuarios implementarlo y aprovechar sus funcionalidades de manera efectiva.
