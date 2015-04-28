'''
Encriptador RSA simple

Matematica Discreta - TP Anual
Nahuel Lattessi
2014
'''

# coding: utf-8
import sys
import math
import random
import getopt


#--- FUNCIONES ---#

# Funcion para ver si un numero dado 'num' es primo.
# 1) Si 'num' es 2, es primo
# 2) Si 'num' es par, no es primo
# 3) Compruebo si existe un divisor de 'num' entre 3 y 'num' al cuadrado
# solo los impares. De existir, 'num' no es primo.
def es_primo(num):
    if num > 1:
        if num == 2: # 1)
            return True
        if num % 2 == 0: # 2)
            return False
        for x in range(3, int(math.sqrt(num) + 1), 2): # 3)
            if num % x == 0:
                return False
        return True
    return False

# Funcion para generar un primo de 'n' cantidad de digitos.
# 1) Establezco digito minimo
# 2) Establezco digito maximo.
# 3) Elijo un numero al azar entre ambos extremos
# 4) Si es primo, lo devuelvo. Si no lo es, elijo otro numero y repregunto.
def generar_primo(digitos):
    low = int('1' + '0' * (digitos - 1))
    high = int('9' * digitos)
    done = False
    while not done:
        num = random.randint(low, high)
        if es_primo(num):
            return num

# Funcion recursiva que busca el minimo comun divisor entre 2 numeros.
def mcd(a, b):
    if b == 0:
        return a
    return mcd(b, a % b)

# El alfabeto a utilizar para la codificacion del mensaje
alfabeto = u''' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\t\n\x0b\x0c\r0123456789áéíóúñ'''

# Funcion que codifica una letra en numero segun su posicion en el alfabeto
def codificar_letra(letra):
    return alfabeto.index(letra)

# Funcion que decodifica un numero en letra segun el alfabeto.
def decodificar_letra(n):
    return alfabeto[n]

# Funcion que codifica un texto ingresado, codificando letra por letra.
def codificar_texto(texto):
    return [codificar_letra(c) for c in texto]

# Funcion que decodifica una lista de numeros en el texto correspondiente.
def decodificar_texto(lista):
    return ''.join([decodificar_letra(n) for n in lista])

# Funcion que encripta en RSA una letra
# a partir de una clave publica dada
def encriptar_letra(M, clave_publica):
    n, e = clave_publica
    return ((M ** e) % n)

# Funcion que desencripta una letra encriptada en RSA
# a partir de una clave privada dada
def desencriptar_letra(C, clave_privada):
    n, d = clave_privada
    return ((C ** d) % n)

# Funcion que encripta un texto en RSA
def encriptar_texto(mensaje, clave_publica):
    return [encriptar_letra(M, clave_publica) for M in mensaje]

# Funcion que desencripta un texto encriptado en RSA
def desencriptar_texto(mensaje_encriptado, clave_privada):
    n, d = clave_privada
    return [desencriptar_letra(C, clave_privada) for C in mensaje_encriptado]

# Funcion que imprime el mensaje de ayuda
def print_ayuda():
    print "rsa.py --crear --digitos <n>"
    print "rsa.py --encriptar --mensaje <mensaje> --publica <(n, e)>"
    print "rsa.py --desencriptar --mensaje <mensaje> --privada <(n, d)>"


#--- Main ---#
def main(argv):

    # Seteo las opciones y argumentos por consola
    try:
        opts, args = getopt.getopt(argv, "h", ["help", "crear", "digitos=", "encriptar", "mensaje=", "publica=", "desencriptar", "privada="])
    except getopt.GetoptError:
        print_ayuda()
        sys.exit(2)

    # Variables que alojan los argumentos
    accion = None
    digitos = None
    mensaje = None
    clave = None

    # Guardo los argumentos ingresados en las variables correspondientes
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_ayuda()
            sys.exit()
        elif opt == "--crear":
            accion = "crear"
        elif opt == "--encriptar":
            accion = "encriptar"
        elif opt == "--desencriptar":
            accion = "desencriptar"
        elif opt == "--digitos":
            digitos = int(arg)
        elif opt == "--mensaje":
            mensaje = arg
        elif opt == "--publica":
            clave = arg
        elif opt == "--privada":
            clave = arg

    # Si no se ingreso una accion, imprimo ayuda
    if accion is None:
        print_ayuda()
        sys.exit()


    # Accion: Crear par de llaves publica y privada
    if accion == "crear":
        
        # Si faltan datos, imprimo la ayuda
        if digitos is None:
            print_ayuda()
            sys.exit()

        # Digitos minimo 2 para soportar
        # la cantidad de caracteres del alfabeto
        if digitos < 2:
            digitos = 2
        
        # Genero 2 numeros primos distintos entre si
        p = generar_primo(digitos)
        q = generar_primo(digitos)
        while q == p:
            q = generar_primo(digitos)
        
        # Establezco 'n'
        n = p * q
        
        # Calculo la funcion de Euler de 'n'
        euler = (p-1) * (q-1)

        # Elijo 'e' al azar cumpliendo:
        # 1 <= e <= euler Y coprimo con variable 'euler'
        e = random.randint(1, euler)
        while (mcd(e, euler) != 1):
            e = random.randint(1, euler)
        
        # Elijo 'd' al azar cumpliendo:
        # 1<=d<=n Y que satisfasga e * d = 1 (mod 'euler')
        d = random.randint(1, n)
        while (((e * d) % euler) != 1):
               d = random.randint(1, n)

        # Armo el par de llaves para devolverlas
        # como un string separado por coma
        clave_publica = ','.join(map(str, [n, e]))
        clave_privada = ','.join(map(str, [n ,d]))
        print "Clave publica: {}".format(clave_publica)
        print "Clave privada: {}".format(clave_privada)


    # Accion: Encripto un texto dado a partir de una clave publica
    elif accion == "encriptar":

        # Si faltan datos, imprimo la ayuda
        if mensaje is None or clave is None:
            print_ayuda()
            sys.exit()

        # Transformo la clave en string a la lista de int que la representa
        clave_publica = map(int, clave.replace(" ", "").split(','))

        # Codifico el texto segun el alfabeto
        # como una lista de int y lo encripto
        M = codificar_texto(mensaje)
        C = encriptar_texto(M, clave_publica)
        
        # Muestro el texto encriptado como un string separado por coma
        salida = ','.join(map(str, C)) 
        print "{}".format(salida)


    # Accion: Desencripto un texto dado a partir de una clave privada
    elif accion == "desencriptar":

        # Si faltan datos, imprimo la ayuda
        if mensaje is None or clave is None:
            print_ayuda()
            sys.exit()

        # Transformo la clave en string a una lista de int que la representa
        clave_privada = map(int, clave.replace(" ", "").split(','))
        
        # Transformo el texto en string a una lista de int y lo desencripto
        C = map(int, mensaje.split(','))
        M = desencriptar_texto(C, clave_privada)

        # Decodifico el texto segun el alfabeto y lo muestro por pantalla
        salida = decodificar_texto(M)
        print "{}".format(salida)


if __name__ == "__main__":
    main(sys.argv[1:])
