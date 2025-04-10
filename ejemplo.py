def colocar_bit_control(p):
    primer=(int((ord(p))))
    primer >>=4
    aux1 = 0
    aux1 = aux1 | ((primer & 8) << 2) | ((primer & 4) << 1) | ((primer & 2) << 1) |((primer & 1) << 1)
    aux1= aux1 | (( ((aux1 & 128) >> 7) ^ ((aux1 & 32) >> 5) ^ ((aux1 & 8) >> 3) ^ ((aux1 & 2) >> 1) ) << 7)
    aux1= aux1 | (( ((aux1 & 64) >> 6) ^ ((aux1 & 32) >> 5) ^ ((aux1 & 4) >> 2) ^ ((aux1 & 2) >> 1) ) << 6)
    aux1= aux1 | (( ((aux1 & 16) >> 4) ^ ((aux1 & 8) >> 3) ^ ((aux1 & 4) >> 2) ^ ((aux1 & 2) >> 1) ) << 4)
    aux1= aux1 | (( ((aux1 & 128) >> 7) ^ ((aux1 & 64) >> 6) ^ ((aux1 & 32) >> 5) ^ ((aux1 & 16) >> 4) ^ ((aux1 & 8) >> 3) ^ ((aux1 & 4) >> 2) ^ ((aux1 & 2) >> 1) ))
    segundo=int((ord(p))% 16)
    aux2 = 0
    aux2 = aux2 | ((segundo & 8) << 2) | ((segundo & 4) << 1) | ((segundo & 2) << 1) |((segundo & 1) << 1)
    print(bin(aux1))
    aux2= aux2 | (( ((aux2 & 128) >> 7) ^ ((aux2 & 32) >> 5) ^ ((aux2 & 8) >> 3) ^ ((aux2 & 2) >> 1) ) << 7)
    aux2= aux2 | (( ((aux2 & 64) >> 6) ^ ((aux2 & 32) >> 5) ^ ((aux2 & 4) >> 2) ^ ((aux2 & 2) >> 1) ) << 6)
    aux2= aux2 | (( ((aux2 & 16) >> 4) ^ ((aux2 & 8) >> 3) ^ ((aux2 & 4) >> 2) ^ ((aux2 & 2) >> 1) ) << 4)
    aux2= aux2 | (( ((aux2 & 128) >> 7) ^ ((aux2 & 64) >> 6) ^ ((aux2 & 32) >> 5) ^ ((aux2 & 16) >> 4) ^ ((aux2 & 8) >> 3) ^ ((aux2 & 4) >> 2) ^ ((aux2 & 2) >> 1) ))
    print(bin(aux2))


          

def hamminizacion(p):
    primer=codificacion_hamming(int((ord(p)))>>4)
    segundo=codificacion_hamming(int((ord(p))% 16))
    return {"primer" : primer , "segundo" : segundo}



def codificacion_hamming(p):
    control1=(((p & 8) >> 3) + ((p & 4) >> 2)+ ((p & 1))) % 2
    control2=(((p & 8) >> 3) + ((p & 2) >> 1)+ ((p & 1))) % 2
    control3=(((p & 4) >> 2)+ ((p & 2) >> 1) + ((p & 1))) % 2
    paridad=(control1+ control2 + control3 + (((p & 8) >> 3) + ((p & 4) >> 2)+ ((p & 1)) + ((p & 2) >> 1)))%2
    num=0
    num = (control1 << 7) + (control2 << 6) + ((p & 8) << 2) + (control3 << 4) + ((p & 4) << 1) + ((p & 2) << 1) + ((p & 1) << 1) + paridad
    return num


"""
print((int((ord("y")))) >> 4)

print(bin((int((ord("y")))) >> 4))

print(bin((int((ord("y")))) % 16))

print(bin(ord("y")))
print(bin((int((ord("y")))) % 16))
print(bin((int((ord("y")))) % 16 <<4))
print((int((ord("y")))) % 16 <<4)
colocar_bit_control((int((ord("y")))) >> 4)
"""