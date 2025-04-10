import ejemplo as ejemplo

import time

inicio = time.time()

ejemplo.codificar_archivo('texto_plano.txt','texto_hammificado.txt')

ejemplo.decodificar_archivo('texto_hammificado.txt','texto_decodificado.txt')

ejemplo.ingresar_error('texto_hammificado.txt', 'texto_error.txt')

ejemplo.decodificar_archivo('texto_error.txt', 'texto_decodificado_error.txt')

fin = time.time()

print(f"Tiempo de ejecución: {fin - inicio:.16f} segundos")