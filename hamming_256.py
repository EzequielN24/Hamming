import random
import math

def crear_numero_256(p):
    # p contiene 240 bits de datos
    j = 0
    res = 0
    for i in range(1, 257):
        if (i & (i - 1)) == 0:  # Potencia de 2: posición de bit de control
            continue
        elif j < 240:
            bit = (p >> (239 - j)) & 1  # Solo tomamos 240 bits
            res |= (bit << (256 - i))
            j += 1
        else:
            # Rellenamos con ceros del 241 al 247 (se agregan automáticamente al mantener res en 0)
            continue
    return codificacion_hamming_256(res)


def codificacion_hamming_256(p):
    for bit_pos in [1, 2, 4, 8, 16, 32, 64, 128]:
        control = calcular_bit_control(p, bit_pos)
        p |= (control << (256 - bit_pos))
    p=calcular_bit_paridad(p)
    return p



def calcular_bit_control(p:int, pos:int) -> int:
    control = 0
    for i in range(pos, 256, pos * 2):
        for j in range(i, i + pos):
            control ^= (p >> (256 - j)) & 1
    return control



def calcular_bit_paridad(p):
    paridad=0
    for i in range (1,256):
        paridad ^= (p >> (256 - i)) & 1
    p^= paridad
    return p



def codificar_archivo_256(file_name_read, file_name_write):
    try:
        with open(file_name_read, "rb") as f, open(file_name_write, "w",encoding="utf-8") as wr:
            while True:
                bloque = f.read(30)
                if len(bloque) == 0:
                    break
                valor = int.from_bytes(bloque, byteorder='big')
                valor <<= (8 * (30 - len(bloque)))
                num = crear_numero_256(valor)
                print(f'La palabra codificada es {bin(num)}')
                for i in range(1,33):
                    letra=(num >> (256 - (8 * i))) & 255
                    wr.write(f"{chr(letra)}")
    except FileNotFoundError as e:
        print("Ocurrió un error al abrir los archivos: ", e)
    except Exception as e:
        print("Error: ", e)




'''--------------------------------------------------------------------------------------------------'''



def deshamminizacion_256(p,fix_module):
    decodificacion = control_hamming_256(p)
    num = (decodificacion["s6"] << 6) + (decodificacion["s5"] << 5) + (decodificacion["s4"] << 4) + (decodificacion["s3"] << 3) +(decodificacion["s2"] << 2) + (decodificacion["s1"] << 1) + (decodificacion["s0"])
    if decodificacion["paridad"] == 0:
        if num==0:
            return decodificacion_hamming_256(p)
        else:
            return -1 #Hay dos errores
    else:
        if num==0:
            #Hay error en el bit de paridad
            if fix_module == 1:
                p = corregir_error_256(p,256) 
                return decodificacion_hamming_256(p)
            else:
                return decodificacion_hamming_256(p)
        else:
            #Hay error en una posición que no es el bit de paridad
            if fix_module == 1:
                p = corregir_error_256(p,num) 
                return decodificacion_hamming_256(p)
            else:
                return decodificacion_hamming_256(p)


def corregir_error_256(p,error):
    return (p ^ (2**256 >> error)) 



def control_hamming_256(p):
    res={}
    for i,bit_pos in enumerate([1, 2, 4, 8, 16, 32, 128]):
        control = calcular_bit_control_deshamminizacion(p, bit_pos)
        res[f"s{i}"]=control
    paridad=0
    for i in range (1,257):
        paridad ^= (p >> (256 - i)) & 1
    res[f"paridad"]=paridad
    return res



def calcular_bit_control_deshamminizacion(p:int, pos:int) -> int:
    control = 0
    for i in range(pos, 256, pos * 2):
        for j in range(i, i + pos):
            control ^= ((p >> (256 - j)) & 1)
    return control


def decodificacion_hamming_256(p):
    j = 0
    res = 0
    print(bin(p))
    for i in range(1, 257):
        if (i & (i - 1)) == 0:
            continue
        if j >= 240:
            break
        bit = (p >> (256 - i)) & 1
        res |= (bit << (239 - j))
        j += 1
    return res


def decodificar_archivo_256(file_name_read, file_name_write, arreglar_archivo):
    try:
        with open(file_name_read, "r", encoding="utf-8") as f, open(file_name_write, "w",encoding="utf-8") as wr:
            while True:
                bloque = f.read(32)
                if len(bloque) == 0:
                    break
                valor=0
                for i,caracter in enumerate(bloque):
                    valor += ord(caracter) << (248-(8*i))
                num = deshamminizacion_256(valor,arreglar_archivo)
                print(f'La palabra es {bin(num)} y tiene {num.bit_length()} bits')
                for i in range(30):
                    shift = 232 - (8 * (i))
                    letra = (num >> shift) & 0xFF
                    if(letra != 0):
                        wr.write(f"{chr(letra)}")
    except FileNotFoundError as e:
        print("Ocurrió un error al abrir los archivos: ", e)
    except Exception as e:
        print("Error: ", e)



#Estamos leyendo mal el archivo


'''----------------------------------------------------------------------------------------------------------------'''

def ingresar_error_256(file_name_read,file_name_write):
    try:
        with open(file_name_read, 'r', encoding="utf-8") as f, open(file_name_write, 'w',encoding="utf-8") as wr:
            while True:
                valor=0
                contenido = f.read(32)
                if(len(contenido)==0):
                    break
                if random.randint(0,1) == 1:
                    error = random.randint(0,255)
                    mask = 1 << error
                    for i,caracter in enumerate(contenido):
                        valor += ord(caracter) << (248-(8*i))
                    valor^= mask
                    for i in range(1,33):
                        caracter=(valor >> (256-(8*i))) & 255
                        caracter=chr(caracter)
                        wr.write(f"{(caracter)}")
                else:
                    wr.write(f"{(contenido)}")
        
    except Exception as e:
        print(f"Error al ingresar error: {e}")