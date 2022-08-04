# pylint: disable=unused-argument

"""Contiene los métodos CRUD de la API relacionados con
la administración de productos
"""

import logging
from typing import Optional
from fastapi import (APIRouter, Header, HTTPException)
from ..schemas.requests import ProductoRequest
from ..schemas.responses import ProductoResponse
from ..models.producto_dao import ProductoDAO
from .token import requiere_token
from ..constantes import (HTTP_404, HTTP_500)

router = APIRouter()


@router.get("/pos/productos/{sku}", response_model=ProductoResponse)
@requiere_token
def obtener_producto(
        sku: int, uid: str = Header(None),
        token: Optional[str] = Header(None)):
    """Obtiene un producto por medio de su sku
    param sku_prod: int
    return: Producto
    """
    try:
        producto = ProductoDAO.obtener(sku)
    except Exception as ex:
        logging.error(f"productos.obtener_producto() - {ex}")
        raise HTTPException(status_code=HTTP_500, detail=str(ex)) from ex
    else:
        if producto is None:
            raise HTTPException(
                status_code=HTTP_404,
                detail="No existe producto con el SKU proporcionado")

    return producto


@router.post("/pos/productos/", response_model=int)
@requiere_token
def registrar_producto(
        prod: ProductoRequest, uid: str = Header(None),
        token: Optional[str] = Header(None)):
    """Registra un nuevo producto en inventario
    param prod: ProductoRequest
    return: int
    """
    try:
        sku = ProductoDAO.registrar(prod)
    except Exception as ex:
        logging.error(f"productos.registrar_producto() - {ex}")
        raise HTTPException(status_code=HTTP_500, detail=str(ex)) from ex

    return sku
