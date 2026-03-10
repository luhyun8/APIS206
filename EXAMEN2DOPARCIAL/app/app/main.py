#importaciones
from fastapi import FastAPI,status,HTTPException
from typing import Optional, List
import asyncio
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

from PRACTICA5.app.main import Prestamo

# Crear la aplicación FastAPI
app = FastAPI(
    title="API de Citas Médicas",
    description="Una API para el control de Citas Médicas",
    version="1.0."
)

# Simulación de base de datos
libros = []
prestamos = []
usuarios = []

#modelo de validación pydantic
class Citas(BaseModel):
    id: int
    nombre: str = Field(..., min_length=5, max_length=50)
    apellido: str 
    fecha_cita: int = Field(..., gt=0, le=datetime.now().year)
    motivo: str = Field(..., min_length=20,max_length=100)


#endpoints
@app.get("/v1/bienvenidos",tags=["Inicio"])
async def bienvenidos():
    return {"mensaje": "Bienvenido a Citas Médicas"}

# craer cita
@app.post("/v1/crear_citas", tags=["Citas"])
async def crear_citas(citas:Citas):
    await asyncio.sleep(2)  # Simula na operación asincrónica
    for cita in citas:
        if cita["id"] == citas.id:
            raise HTTPException(
                status_code=400,
                detail="El ID de la cita ya existe")
    citas.append(citas.dict())
    return {"status": "200",
            "message": "Cita registrada exitosamente",
            "datos": citas}

#listar citas
@app.get("/v1/listar/citas",tags=["Listado de Citas"])
async def listar_citas():
    return {"status": "200",
            "total": len(Citas),
            "datos": Citas}

#buscar cita por ID
@app.get("/v1/buscar/citas",tags=["Citas"])
async def buscar_cita(id: int):
    await asyncio.sleep(2)  # Simula na operación asincrónica
    resultados = [Citas for c in libros if c["id"] == id]
    if not resultados:
        raise HTTPException(status_code=400, detail="Cita no encontrada")
    return {"status": "200",
            "total": len(resultados),
            "datos": resultados}

#registrar prestamo de libro
@app.post("/v1/prestamos",tags=["Prestamos"])
async def registrar_prestamo(prestamo: Prestamo):
    # Verificar que el libro exista
    libro_encontrado = None
    for libro in libros:
        if libro["id"] == prestamo.libro_id:
            libro_encontrado = libro
            break
    if libro_encontrado is None:
        raise HTTPException(status_code=400, detail="El libro no existe")
    if libro_encontrado["estado"] == "prestado":
        raise HTTPException(status_code=409, detail="El libro ya está prestado")
    
    libro_encontrado["estado"] = "prestado"
    prestamos.append(prestamo.dict())
    return {"status": "200",
            "message": "Préstamo registrado exitosamente",
            "datos": prestamo}

#marcar libro como devuelto
@app.put("/v1/prestamos/devolver/{libro_id}",tags=["Prestamos"])
async def devolver_libro(libro_id: int):
    for libro in libros:
        if libro["id"] == libro_id:
            if libro["estado"] == "prestado":
                libro["estado"] = "disponible"
                return {"status": "200",
                        "message": "Libro devuelto exitosamente",
                        "datos": libro}
            else:
                raise HTTPException(status_code=400, detail="El libro no está prestado")
    raise HTTPException(status_code=409, detail="Libro no encontrado")


#eliminar registro de prestamo
@app.delete("/v1/prestamos/{id}",tags=["CRUD prestamos"])
async def eliminar_prestamo(id: int):
    for index, prestamo in enumerate(prestamos):
        if prestamo["libro_id"] == id:
            prestamo_eliminado = prestamos.pop(index)
            return {"status": "200",
                    "message": "Prestamo eliminado exitosamente",
                    "datos" : prestamo_eliminado}
    raise HTTPException(
        status_code=409,
        detail="Prestamo no encontrado")       