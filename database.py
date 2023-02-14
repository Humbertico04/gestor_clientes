from config import DATABASE_PATH
import csv

class Cliente:
    # Constructor con 3 parámetros
    def __init__(self, dni, nombre, apellido):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
    # Función para imprimir
    def __str__(self):
            return f"({self.dni}) {self.nombre} {self.apellido}"

class Clientes:
    # Creamos la lista y cargamos los clientes en memoria
    lista = []
    with open(DATABASE_PATH, newline='\n') as fichero:
        reader = csv.reader(fichero, delimiter=';')
        for dni, nombre, apellido in reader:
            cliente = Cliente(dni, nombre, apellido)
            lista.append(cliente)

    # Busca un cliente por su DNI
    @staticmethod
    def buscar(dni):
        for cliente in Clientes.lista:
            if cliente.dni == dni:
                return cliente

    # Crea un nuevo cliente
    @staticmethod
    def crear(dni, nombre, apellido):
        cliente = Cliente(dni, nombre, apellido)
        Clientes.lista.append(cliente)
        Clientes.guardar()
        return cliente

    # Modifica la información de un cliente
    @staticmethod
    def modificar(dni, nombre, apellido):
        for i, cliente in enumerate(Clientes.lista):
            if cliente.dni == dni:
                Clientes.lista[i].nombre = nombre
                Clientes.lista[i].apellido = apellido
                Clientes.guardar()
                return Clientes.lista[i]
    
    # Borra un cliente
    @staticmethod
    def borrar(dni):
        for i, cliente in enumerate(Clientes.lista):
            if cliente.dni == dni:
                cliente = Clientes.lista.pop(i)
                Clientes.guardar()
                return cliente
            
    # Guarda los clientes en el fichero de la BD
    @staticmethod
    def guardar():
        with open(DATABASE_PATH, "w", newline="\n") as fichero:
            writer = csv.writer(fichero, delimiter=";")
            for c in Clientes.lista:
                writer.writerow((c.dni, c.nombre, c.apellido))
