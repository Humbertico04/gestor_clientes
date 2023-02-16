# Importar librerías de sistema operativo y expresiones regulares
import os
import platform
import re

# Definir función para limpiar la pantalla
def limpiar_pantalla():
    # Si el sistema operativo es Windows, usar cls
    if platform.system() == "Windows":
        os.system('cls')
    # Si el sistema operativo es Linux o Mac, usar clear
    else:
        os.system('clear')

# Definir función para leer texto
def leer_texto(longitud_min=0, longitud_max=100, mensaje=None):
    # Mostrar mensaje si se pasa como argumento
    if mensaje:
        print(mensaje)
    # Bucle para leer texto
    while True:
        texto = input("> ")
        # Comprobar longitud
        if len(texto) >= longitud_min and len(texto) <= longitud_max:
            return texto
        
# Definir función para validar un DNI
def dni_valido(dni, lista):
    # Comprobar si el DNI tiene el formato correcto
    if not re.match('[0-9]{2}[A-Z]$', dni):
        print("DNI incorrecto, debe cumplir el formato.")
        return False
    # Comprobar si el DNI ya está en la lista de clientes
    for cliente in lista:
        if cliente.dni == dni:
            print("DNI utilizado por otro cliente.")
            return False
    return True