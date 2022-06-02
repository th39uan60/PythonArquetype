# PYLINT FALSE POSITIVES (disable them)
# pylint: disable=no-name-in-module
# pylint: disable=too-few-public-methods

"""Contiene todos los modelos usados como entradas dentro de la aplicación
de punto de venta para persistencia de datos.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class VentaRequest(BaseModel):
    """Representa los datos de una venta para peticiones"""
    prods: list[int] = []
    cte_id: Optional[int] = 0
    subtotal: float
    impuesto: float
    total: float


class ClienteRequest(BaseModel):
    """Representa los datos de una persona (cliente) para peticiones"""
    cte_id: Optional[int] = 0
    nombre: str
    apellidos: str
    fecha_nac: datetime


class ProductoRequest(BaseModel):
    """Representa los datos de un producto para peticiones"""
    sku: Optional[int] = 0
    desc: str
    precio: float
