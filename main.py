#importaciones
from fastapi import FastAPI
from typing import Optional
import asyncio

# Crear la aplicación FastAPI
app = FastAPI(
    title="API de Calificaciones TAI",
    description="Una API simple para gestionar calificaciones en TAI",
    version="1.0."
)

usuarios=[
    {"id":1,"nombre":"Jungkook","edad":28},
    {"id":2,"nombre":"Bangchan","edad":28},  
    {"id":3,"nombre":"Hyunjin","edad":25}
          ]



#endpoints
@app.get("/",tags=["Inicio"])
async def HolaMundo():
    return {"mensaje": "Hola Mundo FastAPI a TAI"}

@app.get("/v1/bienvenidos",tags=["Inicio"])
async def bienvenidos():
    return {"mensaje": "Bienvenido a TAI"}

@app.get("/v1/calificaciones",tags=["Asincronia"])
async def calificaciones():
    await asyncio.sleep(2)  # Simula na operación asincrónica
    return {"mensaje": "Tu calificación en TAI es 10"}

@app.get("/v1/Usuarios",tags=["Parametro obligatorio"])
async def consultaUsuarios(id: int):
    await asyncio.sleep(2)  # Simula na operación asincrónica
    return {"Usuario consultado": id}

@app.get("/v1/Usuarios_op",tags=["Parametro opcional"])
async def consultaOp(id: Optional [int] = None):
    await asyncio.sleep(3)  # Simula na operación asincrónica
    if id is not None:
     for usuario in usuarios:
        if usuario["id"] == id:
            return {"Usuario consultado": id,
                    "Datos":usuario
                    }
        return {"mensaje":"Usuaroio no encontrado o no proporcionado"}
    else:
        return {"Aviso": "No se proporcionó ningún ID de usuario"}

# Ejecutar la aplicación con: uvicorn main:app --reload
# Acceder a la ruta: http://
#localhost:8000/v1/calificaciones