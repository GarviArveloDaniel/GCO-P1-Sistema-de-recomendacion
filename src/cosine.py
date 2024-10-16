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