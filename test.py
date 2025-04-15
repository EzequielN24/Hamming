import hamming_256 as ejemplo

import time

inicio = time.time()

arreglar_archivo = 0 #1 si se quiere arreglar. 0 en caso contrario


ejemplo.codificar_archivo('texto_plano.txt','texto_hammificado.txt')

fin = time.time()

print(f"Tiempo de ejecución: {fin - inicio:.16f} segundos")