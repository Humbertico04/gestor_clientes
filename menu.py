import os
import helpers
import database as db

def iniciar():
    while True:
        helpers.limpiar_pantalla()

        print("========================")
        print(" BIENVENIDO AL Manager ")
        print("========================")
        print("[1] Listar clientes ")
        print("[2] Buscar cliente ")
        print("[3] Añadir cliente ")
        print("[4] Modificar cliente ")
        print("[5] Borrar cliente ")
        print("[6] Cerrar el Manager ")
        print("========================")

        opcion = input("> ")
        helpers.limpiar_pantalla()
        if opcion == '1': # Si el usuario ingresa 1, se listan los clientes
            print("Listando los clientes...\n")
            for cliente in db.Clientes.lista: # Se recorre la lista de clientes
                print(cliente) # Se imprime cada cliente

        if opcion == '2': # Si la opción es 2, buscar un cliente
            print("Buscando un cliente...\n")
            dni = helpers.leer_texto(3, 3, "DNI (2 ints y 1 char)").upper() # Lee el DNI del cliente
            cliente = db.Clientes.buscar(dni) # Busca el cliente con el DNI introducido
            print(cliente) if cliente else print("Cliente no encontrado.") # Si el cliente existe, se imprime, si no, se imprime que no existe

        if opcion == '3':  # Opción 3: Añadir un cliente
            print("Añadiendo un cliente...\n")
            # Comprobación de DNI válido
            while 1:  # Bucle infinito
                dni = helpers.leer_texto(3, 3, "DNI (2 ints y 1 char)").upper()  # Pedir el DNI
                if helpers.dni_valido(dni, db.Clientes.lista):  # Si el DNI es válido
                    break  # Salir del bucle
            nombre = helpers.leer_texto(2, 30, "Nombre (de 2 a 30 chars)").capitalize()  # Pedir el nombre
            apellido = helpers.leer_texto(2, 30, "Apellido (de 2 a 30 chars)").capitalize()  # Pedir el apellido
            db.Clientes.crear(dni, nombre, apellido)  # Crear el cliente
 
        if opcion == '4':
            # Se muestra un mensaje de "Modificando un cliente" y se pide por teclado el DNI del cliente a modificar.
            print("Modificando un cliente...\n")
            dni = helpers.leer_texto(3, 3, "DNI (2 ints y 1 char)").upper()
            # Se busca el cliente por el DNI que se ha introducido por teclado.
            cliente = db.Clientes.buscar(dni)
            if cliente:
                # Si se ha encontrado el cliente, se le pide por teclado el nombre y el apellido, que se guardan en la variable nombre y apellido.
                nombre = helpers.leer_texto(2, 30, f"Nombre (de 2 a 30 chars) [{cliente.nombre}]").capitalize()
                apellido = helpers.leer_texto(2, 30, f"Apellido (de 2 a 30 chars) [{cliente.apellido}]").capitalize()
                # Se llama al método modificar del módulo Clientes y se le pasan los parámetros dni, nombre y apellido.
                db.Clientes.modificar(cliente.dni, nombre, apellido)
                print("Cliente modificado correctamente.")
            else:
                # Si no se ha encontrado el cliente, se muestra un mensaje de "Cliente no encontrado."
                print("Cliente no encontrado.")

        if opcion == '5': # Selecciona la opción 5 para borrar un cliente
            print("Borrando un cliente...\n")
            dni = helpers.leer_texto(3, 3, "DNI (2 ints y 1 char)").upper() # Lee el DNI del cliente a borrar
            print("Cliente borrado correctamente.") if db.Clientes.borrar(dni) else print("Cliente no encontrado.")

        if opcion == '6':
            print("Saliendo...\n")
            break
        
        input("\nPresiona ENTER para continuar...")