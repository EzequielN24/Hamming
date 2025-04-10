import ejemplo

import time

inicio = time.time()
ejemplo.colocar_bit_control("u")
fin = time.time()

print(f"Tiempo de ejecución: {fin - inicio:.8f} segundos")

inicio = time.time()
ejemplo.jaja("u")
fin = time.time()

print(f"Tiempo de ejecución: {fin - inicio:.8f} segundos")