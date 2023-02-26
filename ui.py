# Importamos los módulos necesarios
import helpers
import database as db
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING

# Clase para centrar ventanas
class CenterWidgetMixin:
    def center(self):
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int(ws/2 - w/2)
        y = int(hs/2 - h/2)
        self.geometry(f"{w}x{h}+{x}+{y}")

# Clase para la ventana de crear clientes
class CreateClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Crear cliente")
        self.build()
        self.center()
        self.transient(parent)
        self.grab_set()

    def build(self):
        # Creamos el marco principal
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        # Creamos las etiquetas de los campos que se deben llenar
        Label(frame, text="DNI (2 ints y 1 upper char)").grid(row=0, column=0)
        Label(frame, text="Nombre (de 2 a 30 chars)").grid(row=0, column=1)
        Label(frame, text="Apellido (de 2 a 30 chars)").grid(row=0, column=2)

        # Creamos los campos de entrada para el DNI, Nombre y Apellido
        dni = Entry(frame)
        dni.grid(row=1, column=0)
        dni.bind("<KeyRelease>", lambda event: self.validate(event, 0))
        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda event: self.validate(event, 1))
        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda event: self.validate(event, 2))

        # Creamos el marco para los botones
        frame = Frame(self)
        frame.pack(pady=10)

        # Creamos el botón para crear un nuevo cliente y el botón para cancelar la operación
        crear = Button(frame, text="Crear", command=self.create_client)
        crear.configure(state=DISABLED)
        crear.grid(row=0, column=0)
        Button(frame, text="Cancelar", command=self.close).grid(row=0, column=1)

        # Guardamos las referencias a los widgets creados
        self.validaciones = [0, 0, 0]
        self.crear = crear
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def create_client(self):
        # Agregamos nuevo cliente a la tabla y a la base de datos
        self.master.treeview.insert(
            parent='', index='end', iid=self.dni.get(),
            values=(self.dni.get(), self.nombre.get(), self.apellido.get()))
        db.Clientes.crear(self.dni.get(), self.nombre.get(), self.apellido.get())
        self.close()

    def close(self):
        # Cerramos la ventana y actualizamos la vista principal
        self.destroy()
        self.update()

    def validate(self, event, index):
        # Validamos el valor ingresado en el campo correspondiente y cambiamos el color de fondo del campo en base a si es válido o no
        valor = event.widget.get()
        valido = helpers.dni_valido(valor, db.Clientes.lista) if index == 0 \
            else (valor.isalpha() and len(valor) >= 2 and len(valor) <= 30)
        event.widget.configure({"bg": "Green" if valido else "Red"})
        # Cambiamos el estado del botón en base a las validaciones
        self.validaciones[index] = valido
        self.crear.config(state=NORMAL if self.validaciones == [1, 1, 1] else DISABLED)

# Clase para la ventana de editar clientes
class EditClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Actualizar cliente")
        self.build()
        self.center()
        self.transient(parent)
        self.grab_set()

    def build(self):
        # Creamos el marco principal
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        # Creamos las etiquetas de los campos que se deben llenar
        Label(frame, text="DNI (no editable)").grid(row=0, column=0)
        Label(frame, text="Nombre (de 2 a 30 chars)").grid(row=0, column=1)
        Label(frame, text="Apellido (de 2 a 30 chars)").grid(row=0, column=2)

        # Creamos los campos de entrada para el DNI, Nombre y Apellido
        dni = Entry(frame)
        dni.grid(row=1, column=0)
        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda event: self.validate(event, 0))
        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda event: self.validate(event, 1))

        # Obtenemos los datos del cliente seleccionado en la vista principal y los mostramos en los campos correspondientes
        cliente = self.master.treeview.focus()
        campos = self.master.treeview.item(cliente, 'values')
        dni.insert(0, campos[0])
        dni.config(state=DISABLED)
        nombre.insert(0, campos[1])
        apellido.insert(0, campos[2])

        # Creamos el marco para los botones
        frame = Frame(self)
        frame.pack(pady=10)

        # Creamos el botón para actualizar los datos del cliente y el botón para cancelar la operación
        actualizar = Button(frame, text="Actualizar", command=self.edit_client)
        actualizar.grid(row=0, column=0)
        Button(frame, text="Cancelar", command=self.close).grid(row=0, column=1)

        # Guardamos las referencias a los widgets creados
        self.validaciones = [1, 1]
        self.actualizar = actualizar
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def edit_client(self):
        # Actualizamos los datos del cliente en la tabla y en la base de datos
        cliente = self.master.treeview.focus()
        self.master.treeview.item(cliente, values=(
            self.dni.get(), self.nombre.get(), self.apellido.get()))
        db.Clientes.modificar(self.dni.get(), self.nombre.get(), self.apellido.get())
        self.close()

    def close(self):
        # Cerramos la ventana y actualizamos la vista principal
        self.destroy()
        self.update()

    def validate(self, event, index):
        # Validamos el valor ingresado en el campo correspondiente y cambiamos el color de fondo del campo en base a si es válido o no
        valor = event.widget.get()
        valido = (valor.isalpha() and len(valor) >= 2 and len(valor) <= 30)
        event.widget.configure({"bg": "Green" if valido else "Red"})
        # Cambiar el estado del botón en base a las validaciones
        self.validaciones[index] = valido
        self.actualizar.config(state=NORMAL if self.validaciones == [1, 1] else DISABLED)

# Clase para la ventana principal
class MainWindow(Tk, CenterWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title("Gestor de clientes")
        self.build()
        self.center()

    def build(self):
        # Creamos el marco principal
        frame = Frame(self)
        frame.pack()

        # Creamos los cabezales de la tabla
        treeview = ttk.Treeview(frame)
        treeview['columns'] = ('DNI', 'Nombre', 'Apellido')

        # Configuramos el ancho de las columnas
        treeview.column("#0", width=0, stretch=NO)
        treeview.column("DNI", anchor=CENTER)
        treeview.column("Nombre", anchor=CENTER)
        treeview.column("Apellido", anchor=CENTER)

        # Configuramos el encabezado de las columnas
        treeview.heading("DNI", text="DNI", anchor=CENTER)
        treeview.heading("Nombre", text="Nombre", anchor=CENTER)
        treeview.heading("Apellido", text="Apellido", anchor=CENTER)

        # Creamos la barra de desplazamiento vertical
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        treeview['yscrollcommand'] = scrollbar.set

        # Rellenamos la tabla con los datos de la base de datos
        for cliente in db.Clientes.lista:
            treeview.insert(
                parent='', index='end', iid=cliente.dni,
                values=(cliente.dni, cliente.nombre, cliente.apellido))

        # Empaquetamos la tabla y la barra de desplazamiento
        treeview.pack()

        frame = Frame(self)
        frame.pack(pady=20)

        # Creamos los botones para crear, modificar y borrar clientes
        Button(frame, text="Crear", command=self.create).grid(row=0, column=0)
        Button(frame, text="Modificar", command=self.edit).grid(row=0, column=1)
        Button(frame, text="Borrar", command=self.delete).grid(row=0, column=2)

        # Guardamos la referencia a la tabla
        self.treeview = treeview

    def delete(self):
        # Asignamos la función de borrado
        cliente = self.treeview.focus()
        if cliente:
            campos = self.treeview.item(cliente, "values")
            confirmar = askokcancel(
                title="Confirmar borrado",
                message=f"¿Borrar {campos[1]} {campos[2]}?",
                icon=WARNING)
            if confirmar:
                self.treeview.delete(cliente)
                db.Clientes.borrar(campos[0])

    def create(self):
        # Asignamos la función de creación
        CreateClientWindow(self)

    def edit(self):
        # Asignamos la función de edición
        if self.treeview.focus():
            EditClientWindow(self)


if __name__ == "__main__":
    # Lo mandamos a ejecutar al run.py
    app = MainWindow()
    app.mainloop()
