from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, constr, validator
import database as db
import helpers

headers = {"content-type": "charset=utf-8"}

# Definición de modelos
class ModeloCliente(BaseModel):
    # Se define el modelo para los clientes
    dni: constr(min_length=3, max_length=3)
    nombre: constr(min_length=2, max_length=30)
    apellido: constr(min_length=2, max_length=30)

class ModeloCrearCliente(ModeloCliente):
    # Se define el modelo para la creación de clientes, basado en el modelo de cliente
    @validator("dni")
    def validar_dni(cls, dni):
        # Se valida que el DNI sea válido y que el cliente no exista ya en la lista de clientes
        if not helpers.dni_valido(dni, db.Clientes.lista):
            raise ValueError("Cliente ya existente o DNI incorrecto")
        return dni

# Creación de la aplicación
app = FastAPI(
    title="API del Gestor de clientes",
    description="Ofrece diferentes funciones para gestionar los clientes."
)

# Definición de rutas
@app.get("/clientes/", tags=["Clientes"])
async def clientes():
    # Retorna todos los clientes en la lista de clientes
    content = [cliente.to_dict() for cliente in db.Clientes.lista]
    return JSONResponse(content=content, headers=headers)

@app.get("/clientes/buscar/{dni}/", tags=["Clientes"])
async def clientes_buscar(dni: str):
    # Busca un cliente por su DNI en la lista de clientes
    cliente = db.Clientes.buscar(dni=dni)
    if not cliente:
        # Si el cliente no existe, retorna un error 404
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return JSONResponse(content=cliente.to_dict(), headers=headers)

@app.post("/clientes/crear/", tags=["Clientes"])
async def clientes_crear(datos: ModeloCrearCliente):
    # Crea un nuevo cliente con los datos provistos en el cuerpo de la solicitud
    cliente = db.Clientes.crear(datos.dni, datos.nombre, datos.apellido)
    if cliente:
        # Si el cliente se ha creado correctamente, lo retorna en la respuesta
        return JSONResponse(content=cliente.to_dict(), headers=headers)
    # Si no se pudo crear el cliente, retorna un error 404
    raise HTTPException(status_code=404)

@ app.put("/clientes/actualizar/", tags=["Clientes"])
async def clientes_actualizar(datos: ModeloCliente):
    # Actualiza un cliente con los datos provistos en el cuerpo de la solicitud
    if db.Clientes.buscar(datos.dni):
        cliente = db.Clientes.modificar(datos.dni, datos.nombre, datos.apellido)
        if cliente:
            # Si el cliente se ha actualizado correctamente, lo retorna en la respuesta
            return JSONResponse(content=cliente.to_dict(), headers=headers)
    # Si no se pudo actualizar el cliente, retorna un error 404
    raise HTTPException(status_code=404)

@app.delete("/clientes/borrar/{dni}/", tags=["Clientes"])
async def clientes_borrar(dni: str):
    # Elimina un cliente por su DNI
    if db.Clientes.buscar(dni=dni):
        cliente = db.Clientes.borrar(dni=dni)
        # Si el cliente se ha eliminado correctamente, lo retorna en la respuesta
        return JSONResponse(content=cliente.to_dict
(), headers=headers)
    raise HTTPException(status_code=404)

print("Servidor de la API...")
