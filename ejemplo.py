import random

def hamminizacion(p):
    primer=codificacion_hamming(int((ord(p)))>>4)
    segundo=codificacion_hamming(int((ord(p))% 16))
    return {"primer" : chr(primer) , "segundo" : chr(segundo)}


def codificacion_hamming(p):
    control1=(((p & 8) >> 3) + ((p & 4) >> 2)+ ((p & 1))) % 2
    control2=(((p & 8) >> 3) + ((p & 2) >> 1)+ ((p & 1))) % 2
    control3=(((p & 4) >> 2)+ ((p & 2) >> 1) + ((p & 1))) % 2
    paridad=(control1 + control2 + control3 + (((p & 8) >> 3) + ((p & 4) >> 2)+ ((p & 1)) + ((p & 2) >> 1)))%2
    num=0
    num = (control1 << 7) + (control2 << 6) + ((p & 8) << 2) + (control3 << 4) + ((p & 4) << 1) + ((p & 2) << 1) + ((p & 1) << 1) + paridad
    return num


def deshamminizacion(p,q):
    p = ord(p)
    q = ord(q)
    decodificacion = control_hamming(p)
    if control_bit_paridad(p) == 0:
        if not decodificacion:
            result= {'primer': decodificacion_hamming(p)}
        else:
            print("Hay dos errores")
            return -1
    else:
        if not decodificacion:
            print("Error en el bit de paridad")
            return -1
        else:
            print(f"Hay un error en la posición {decodificacion["s2"]} {decodificacion["s1"]} {decodificacion["s0"]}")
            return -1
    decodificacion = control_hamming(q)
    if control_bit_paridad(q) == 0:
        if not decodificacion:
            result['segundo'] = decodificacion_hamming(q)
            resultado = (result['primer'] << 4) + result['segundo']
            return resultado
        else:
            print("Hay dos errores")
            return -1
    else:
        if not decodificacion:
            print("Error en el bit de paridad")
            return -1
        else:
            print (f"Hay un error en la posición {decodificacion["s2"]} {decodificacion["s1"]} {decodificacion["s0"]}")
            return -1


def control_hamming(p):
    s0 = ((p & 128) >> 7) ^ ((p & 32) >> 5) ^ ((p & 8) >> 3) ^ ((p & 2) >> 1)
    s1 = ((p & 64) >> 6) ^ ((p & 32) >> 5) ^ ((p & 4) >> 2) ^ ((p & 2) >> 1)
    s2 = ((p & 16) >> 4) ^ ((p & 8) >> 3) ^ ((p & 4) >> 2) ^ ((p & 2) >> 1)

    if (s0 or s1 or s2):
        return {"s0": s0, "s1": s1, "s2": s2}
    else:
        return {}


def control_bit_paridad(p):
    return ((p & 128) >> 7) ^ ((p & 64) >> 6) ^ ((p & 32) >> 5) ^ ((p & 16) >> 4) ^ ((p & 8) >> 3) ^ ((p & 4) >> 2) ^ ((p & 2) >> 1) ^ (p & 1)


def decodificacion_hamming(p):
    return ((p & 32) >> 2) + ((p & 8) >> 1) + ((p & 4) >> 1) + ((p & 2) >> 1)




def codificar_archivo(file_name_read, file_name_write):
    try:
        with open(file_name_read, "rb") as f:
            contenido = f.read().decode('utf-8')
            with open(file_name_write, 'w') as wr:
                for i in range(0,len(contenido)):
                    hamming = hamminizacion(contenido[i])
                    wr.write(f"{hamming['primer']}{hamming['segundo']}")
    except FileNotFoundError as e:
        print("Ocurrió un error al abrir los archivos: ", e)
    except Exception as e:
        print("Error: ", e)


def decodificar_archivo(file_name_read, file_name_write):
    try:
        with open(file_name_read, "rb") as f:
            contenido = f.read().decode('utf-8')
            with open(file_name_write, 'w') as wr:
                for i in range(0,len(contenido),2):
                    d_hamming = deshamminizacion(contenido[i],contenido[i+1])
                    if(d_hamming == -1):
                        wr.write(f"Hay un error en la letra {i} en la posición tatata")
                    else:
                        wr.write(f"{chr(d_hamming)}")
    except FileNotFoundError as e:
        print("Ocurrió un error al abrir los archivos: ", e)
    except Exception as e:
        print("Error: ", e)




def ingresar_error(file_name_read,file_name_write):
    try:
        with open(file_name_read, 'rb') as f:
            contenido = f.read().decode()
            for x,caracter in enumerate(contenido):
                if random.randint(0,1) == 1:
                    error = random.randint(0,7)
                    mask = 1 << error
                    caracter= mask ^ ord(caracter)
                    contenido = contenido[:x] +  chr(caracter) + contenido[x+1:]
            with open(file_name_write, 'w') as wr:
                wr.write(contenido)
    except Exception as e:
        print(e)