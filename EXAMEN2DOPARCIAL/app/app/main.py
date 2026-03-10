#importaciones
import secrets

from fastapi import Depends, FastAPI,status,HTTPException
from typing import Optional, List
import asyncio
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field
from datetime import datetime

# Crear la aplicación FastAPI
app = FastAPI(
    title="API de Citas Médicas",
    description="Una API para el control de Citas Médicas",
    version="1.0."
)

#modelo de validación pydantic
class Citas(BaseModel):
    id: int
    nombre: str = Field(..., min_length=5, max_length=50)
    apellido: str 
    fecha_cita: int = Field(..., gt=datetime.now().year, le=datetime.now().year)
    motivo: str = Field(..., min_length=20,max_length=100)

#seguridad con HTTP Basic
security = HTTPBasic()
def verificar_Peticion(credentials: HTTPBasicCredentials = Depends(security)):
    usuarioAuth = secrets.compare_digest(credentials.username, "root")
    contraAuth = secrets.compare_digest(credentials.password, "1234")
    if not (usuarioAuth and contraAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
    return credentials.username


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
    resultados = [c for c in Citas if c["id"] == id]
    if not resultados:
        raise HTTPException(status_code=400, detail="Cita no encontrada")
    return {"status": "200",
            "total": len(resultados),
            "datos": resultados}

#confirmar citas
@app.put("/v1/citas/confirmar/{id}",tags=["Citas"])
async def confirmar_cita(id: int):
    for cita in Citas:
        if cita["id"] == id:
            if cita["estado"] == "pendiente":
                cita["estado"] = "confirmada"
                return {"status": "200",
                        "message": "Cita confirmada exitosamente",
                        "datos": cita}
            else:
                raise HTTPException(status_code=400, detail="La cita no está pendiente")
    raise HTTPException(status_code=409, detail="Cita no encontrada")

#eliminar citas
@app.delete("/v1/citas/{id}",tags=["CRUD Citas"])
async def eliminar_cita(id: int, usuarioAuth: str = Depends(verificar_Peticion)):
    for index, cita in enumerate(Citas):
        if cita["id"] == id:
            cita_eliminada = Citas.pop(index)
            return {"status": "200",
                    "message": "Cita eliminada exitosamente",
                    "datos" : cita_eliminada}
    raise HTTPException(
        status_code=409,
        detail="Cita no encontrada")       