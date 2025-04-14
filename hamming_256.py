import random

def hamminizacion_256(p):
    codificacion = codificacion_hamming(ord(p))
    return codificacion


def codificacion_hamming(p):
    i = 248
    control1 = 0
    while i>0:
        if (i == 248 | i == 245 | i == 238 | i == 223 | i == 193):
            control1 += (p & (2 ** i)) >> i
            i-=1
            continue
        else: 
            control1 += (p & (2 ** i)) >> i
            i-=2
            continue
    i = 248
    while i>0:
        if (i == 248 | i == 246 | i == 239 | i == 224 | i == 194):
            control2 += ((p & (2 ** i)) >> i) + ((p & (2 ** (i-1))) >> (i-1))
            i-=3
            continue
        else: 
            control2 += ((p & (2 ** i)) >> i) + ((p & (2 ** (i-1))) >> (i-1))
            i-=4
            continue
        
    control1 = control1 % 2
    control2 = control2 % 2
    

    control2=(((p & 8) >> 3) + ((p & 2) >> 1) + ((p & 1))) % 2
    control3=(((p & 4) >> 2) + ((p & 2) >> 1) + ((p & 1))) % 2
    paridad=(control1 + control2 + control3 + (((p & 8) >> 3) + ((p & 4) >> 2)+ ((p & 1)) + ((p & 2) >> 1)))%2
    num=0
    num = (control1 << 7) + (control2 << 6) + ((p & 8) << 2) + (control3 << 4) + ((p & 4) << 1) + ((p & 2) << 1) + ((p & 1) << 1) + paridad
    return num


def deshamminizacion(p,q,fix_module):
    p = ord(p)
    q = ord(q)
    decodificacion = control_hamming(p)
    if control_bit_paridad(p) == 0:
        if not decodificacion:
            result= {'primer': decodificacion_hamming(p)}
        else:
            return -1 #Hay dos errores
    else:
        if not decodificacion:
            #Hay error en el bit de paridad
            if fix_module == 1:
                p = corregir_error(p,8) 
                result = {'primer': decodificacion_hamming(p)}
            else:
                result= {'primer': decodificacion_hamming(p)}
        else:
            #Hay error en una posición que no es el bit de paridad
            if fix_module == 1:
                error = (decodificacion["s2"] << 2) + (decodificacion["s1"] << 1) + (decodificacion["s0"] )
                p = corregir_error(p,error) 
                result = {'primer': decodificacion_hamming(p)}
            else:
                result= {'primer': decodificacion_hamming(p)}


    decodificacion = control_hamming(q)
    if control_bit_paridad(q) == 0:
        if not decodificacion:
            result['segundo']= decodificacion_hamming(q)
        else:
            return -1 #Hay dos errores
    else:
        if not decodificacion:
            #Hay error en el bit de paridad
            if fix_module == 1:
                q = corregir_error(q,8) 
                result ['segundo'] =  decodificacion_hamming(q)
            else:
                result ['segundo'] =  decodificacion_hamming(q)
        else:
            #Hay error en una posición que no es el bit de paridad
            if fix_module == 1:
                error = (decodificacion["s2"] << 2) + (decodificacion["s1"] << 1) + (decodificacion["s0"] )
                q = corregir_error(q,error) 
                result ['segundo'] =  decodificacion_hamming(q)
            else:
                result ['segundo'] =  decodificacion_hamming(q)
    return (result['primer'] << 4) + (result['segundo'])


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


def corregir_error(p, error):
    return (p ^ (256 >> error))



def codificar_archivo(file_name_read, file_name_write):
    try:
        with open(file_name_read, "rb") as f:
            while True:
                contenido = f.read(31)
                if (len(contenido) == 0):
                    break
                if len(contenido) < 31:
                    contenido = contenido << ((31 - len(contenido)) * 8) #Si lee menos de 31 caracteres realiza corrimientos para hacer el hamming de lo que queda
                with open(file_name_write, 'w') as wr:
                    hamming = hamminizacion_256(contenido)
                    wr.write(f"{hamming}")
    except FileNotFoundError as e:
        print("Ocurrió un error al abrir los archivos: ", e)
    except Exception as e:
        print("Error: ", e)

def decodificar_archivo(file_name_read, file_name_write, arreglar_archivo):
    try:
        with open(file_name_read, "rb") as f:
            contenido = f.read().decode()
            with open(file_name_write, 'w') as wr:
                for i in range(0,len(contenido),2):
                    wr.write(f"{chr(deshamminizacion(contenido[i],contenido[i+1],arreglar_archivo))}")
    except FileNotFoundError as e:
        print("Ocurrió un error al abrir los archivos: ", e)
    except Exception as e:
        print("Error al decodificar archivo: ", e)




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
                wr.write(f"{(contenido)}")
    except Exception as e:
        print(f"Error al ingresar error: {e}")