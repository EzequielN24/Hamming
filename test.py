import hamming_4096 as ejemplo

import time

inicio = time.time()

arreglar_archivo = 0 #1 si se quiere arreglar. 0 en caso contrario


ejemplo.codificar_archivo_4096('texto_plano.txt','texto_hammificado.txt')

ejemplo.decodificar_archivo_4096('texto_hammificado.txt','texto_decodificado.txt',1)

ejemplo.ingresar_error_4096('texto_hammificado.txt','texto_error.txt')

ejemplo.decodificar_archivo_4096('texto_error.txt','texto_decodificado_error.txt',0)

fin = time.time()

print(f"Tiempo de ejecución: {fin - inicio:.16f} segundos")

