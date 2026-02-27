#importaciones
from fastapi import FastAPI,status,HTTPException
from typing import Optional, List
import asyncio
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

# Crear la aplicación FastAPI
app = FastAPI(
    title="API de Biblioteca",
    description="Una API para el control de Biblioteca digital",
    version="1.0."
)

# Simulación de base de datos
libros = []
prestamos = []
usuarios = []

#modelo de validación pydantic
class Libro(BaseModel):
    id: int
    nombre: str = Field(..., min_length=2, max_length=100)
    autor: str 
    año: int = Field(..., gt=1450, le=datetime.now().year)
    paginas: int = Field(..., gt=1)
    estado: str = Field(default="disponible", pattern="^(disponible|prestado)$")

class UsuarioBase(BaseModel):
    id: int
    nombre: str = Field(..., min_length=2, max_length=100)
    correo: EmailStr

class Prestamo(BaseModel):
    libro_id: int
    usuario: int

#endpoints
@app.get("/v1/bienvenidos",tags=["Inicio"])
async def bienvenidos():
    return {"mensaje": "Bienvenido a Biblioteca"}

# registrar un libro
@app.post("/v1/libros",status_code=status.HTTP_201_CREATED, tags=["Libors"])
async def registrar_libro(libro: Libro):
    await asyncio.sleep(2)  # Simula na operación asincrónica
    for lib in libros:
        if lib["id"] == libro.id:
            raise HTTPException(
                status_code=400,
                detail="El ID del libro ya existe")
    libros.append(libro.dict())
    return {"status": "200",
            "message": "Libro registrado exitosamente",
            "datos": libro}

#listar libros
@app.get("/v1/libros",tags=["Libros"])
async def listar_libros():
    return {"status": "200",
            "total": len(libros),
            "datos": libros}

#buscar libro por nombre
@app.get("/v1/libros/buscar",tags=["Libros"])
async def buscar_libro(nombre: str):
    await asyncio.sleep(2)  # Simula na operación asincrónica
    resultados = [l for l in libros if l["nombre"].lower() == nombre.lower()]
    if not resultados:
        raise HTTPException(status_code=400, detail="Libro no encontrado")
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