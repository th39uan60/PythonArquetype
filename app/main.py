"""Es el punto de entrada del servicio (y contiene el acceso a la raíz),
y donde se incluyen los routers relacionados
"""

from os import getenv
import logging
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .routers import (clientes, productos, ventas, token)
from .models import bd
from .security import decodificar_base64


LOG_LV = int(decodificar_base64(getenv("LOGLEVEL")))
logging.basicConfig(
    filename="pointofsale.log", encoding="utf-8", level=LOG_LV,
    format="%(asctime)s. %(levelname)s: %(message)s")

# creamos la estructura de base de datos
bd.ModeloBase.metadata.create_all(bd.motor_bd)
logging.info("database metadata creation: OK")

app = FastAPI()

# incluimos los routers por separado
app.include_router(clientes.router)
app.include_router(productos.router)
app.include_router(ventas.router)
app.include_router(token.router)


@app.get("/pos")
def root():
    """Devuelve la dirección de la documentación de la API"""
    return f"Check service_root:port{app.docs_url}" \
        "for detailed API documentation"

@app.get("/pos/docs")
def root():
    """Redirecciona hacia la documentación de la API"""
    return RedirectResponse("/docs", status_code=303)