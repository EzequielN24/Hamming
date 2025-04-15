import random
import math

def codificar_archivo(file_name_read, file_name_write):
    try:
        with open(file_name_read, "rb") as f, open(file_name_write, "w",encoding="utf-8") as wr:
            while True:
                bloque = f.read(31)
                if len(bloque) == 0:
                    break
                valor = int.from_bytes(bloque, byteorder='big')
                valor <<= (8 * (31 - len(bloque)))
                num = crear_numero_256(valor)
                for i in range(1,32):
                    letra=(num >> (256 - (8 * i))) & 255
                    print(chr(letra))
                    print(ord(chr(letra)))
                    wr.write(f"{chr(letra)}")
    except FileNotFoundError as e:
        print("Ocurrió un error al abrir los archivos: ", e)
    except Exception as e:
        print("Error: ", e)



def crear_numero_256(p):
    j = 1
    res = 0
    for i in range(1, 257):
        if (i==1 or i==2 or i==4 or i==8 or i==16 or i==32 or i==64 or i==128 or i==256):
            continue
        else:
            bit = (p >> (248 - j)) & 1
            res |= (bit << (256 - i))
            j += 1
    p = codificacion_hamming_256(res)
    print(bin(p))
    return p


def calcular_bit_control(p, pos):
    control = 0
    for i in range(pos, 257, pos * 2):
        for j in range(i, min(i + pos, 257)):
            control ^= (p >> (256 - j)) & 1
    return control


def codificacion_hamming_256(p):
    for bit_pos in [1, 2, 4, 8, 16, 32, 64, 128]:
        control = calcular_bit_control(p, bit_pos)
        p |= (control << (256 - bit_pos))
    return p

    
    """
    control1=0
    for i in range(1,256,2):
        control1=control1 ^ (p>>(256-i) & 1)
    print(control1<<255)
    p = p | (control1 << 255)
    control2=0
    for i in range(2,256,4):
        control2=control2 ^ (p>>(256-i) & 1) ^ (p>>(255-i) & 1)
    p = p | (control2 << 254)
    control3=0
    for i in range(4,256,8):
        control3=control3 ^ (p>>(256-i) & 1) ^ (p>>(255-i) & 1) ^ (p>>(254-i) & 1) ^ (p>>(253-i) & 1)
    p = p | (control3 << 252)
    control4=0
    for i in range(8,256,16):
        control4=control4 ^ (p>>(256-i) & 1) ^ (p>>(255-i) & 1) ^ (p>>(254-i) & 1) ^ (p>>(253-i) & 1) ^ (p>>(252-i) & 1) ^ (p>>(251-i) & 1) ^ (p>>(250-i) & 1) ^ (p>>(249-i) & 1)
    p = p | (control4 << 248)
    control5=0
    for i in range(16,256,32):
        control5=control5 ^ (p>>(256-i) & 1) ^ (p>>(255-i) & 1) ^ (p>>(254-i) & 1) ^ (p>>(253-i) & 1) ^ (p>>(252-i) & 1) ^ (p>>(251-i) & 1) ^ (p>>(250-i) & 1) ^ (p>>(249-i) & 1) ^ (p>>(248-i) & 1) ^ (p>>(247-i) & 1) ^ (p>>(246-i) & 1) ^ (p>>(245-i) & 1) ^ (p>>(244-i) & 1) ^ (p>>(243-i) & 1) ^ (p>>(242-i) & 1) ^ (p>>(241-i) & 1)
    p = p | (control5 << 240)
    print(bin(p))
    return p;
    """






def hamminizacion_256(p):
    codificacion = codificacion_hamming_256(p)
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