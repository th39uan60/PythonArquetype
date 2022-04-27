"""Es el punto de entrada del servicio (y contiene el acceso a la raíz),
y donde se incluyen los routers relacionados
"""

from fastapi import FastAPI
from .routers import (clientes, productos, ventas)
from .models import bd

# creamos la estructura de base de datos
bd.ModeloBase.metadata.create_all(bd.motor_bd)

app = FastAPI()

# incluimos los routers por separado
app.include_router(clientes.router)
app.include_router(productos.router)
app.include_router(ventas.router)


@app.get("/")
def root():
    """Devuelve la dirección de la documentación de la API"""
    # return { "Message" : f"Check '{app.docs_url}' for details on API" }
    return f"<HTML>Check <a href='{app.docs_url}'>" \
        "Swagger Docs</a> for details on API</HTML>"
