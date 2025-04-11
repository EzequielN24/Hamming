import ejemplo as ejemplo

import time

inicio = time.time()

arreglar_archivo = 1 #1 si se quiere arreglar. 0 en caso contrario

ejemplo.codificar_archivo('texto_plano.txt','texto_hammificado.txt')

ejemplo.decodificar_archivo('texto_hammificado.txt','texto_decodificado.txt',arreglar_archivo)

ejemplo.ingresar_error('texto_hammificado.txt', 'texto_error.txt')

ejemplo.decodificar_archivo('texto_error.txt', 'texto_decodificado_error.txt',arreglar_archivo)

fin = time.time()

print(f"Tiempo de ejecución: {fin - inicio:.16f} segundos")