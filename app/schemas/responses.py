# PYLINT FALSE POSITIVES (disable them)
# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument

"""Contiene todos los modelos usados como salidas dentro de la aplicación
de punto de venta para persistencia de datos.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import (Any, Optional)
from pydantic import BaseModel


@dataclass
class VentaResponse(BaseModel):
    """Representa los datos de una venta para las respuestas"""
    vta_id: int
    fecha: datetime
    prods: list[int]
    cte_id: Optional[int] = 0
    subtotal: float
    impuesto: float
    total: float

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)


@dataclass
class ClienteResponse(BaseModel):
    """Representa los datos de una persona (cliente) para las respuestas"""
    cte_id: int
    nombre: str
    apellidos: str
    fecha_nac: datetime

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)


@dataclass
class ProductoResponse(BaseModel):
    """Representa los datos de un producto para las respuestas"""
    sku: int
    desc: str
    precio: float
    fecha_upd: Optional[datetime] = None

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)
