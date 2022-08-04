# pylint: disable=unused-argument

"""Contiene los métodos CRUD de la API relacionados con
la administración de ventas
"""

import logging
from typing import Optional
from fastapi import (APIRouter, Header, HTTPException)
from ..schemas.requests import VentaRequest
from ..schemas.responses import VentaResponse
from ..models.venta_dao import VentaDAO
from .token import requiere_token
from ..constantes import (HTTP_404, HTTP_500)
from ..ticket import generar_ticket

router = APIRouter()


@router.get("/pos/ventas/{vta_id}", response_model=VentaResponse)
@requiere_token
def obtener_venta(
        vta_id: int, uid: str = Header(None),
        token: Optional[str] = Header(None)):
    """Obtiene una venta por medio de su id
    param vta_id: id de la venta a buscar
    return: VentaResponse
    """
    try:
        venta = VentaDAO.obtener(vta_id)
    except Exception as ex:
        logging.error(f"ventas.obtener_venta() - {ex}")
        raise HTTPException(status_code=HTTP_500, detail=str(ex)) from ex
    else:
        if venta is None:
            raise HTTPException(
                status_code=HTTP_404,
                detail="No existe venta con el ID proporcionado")

    return venta


@router.post("/pos/ventas/", response_model=int)
@requiere_token
def generar_venta(
        vta: VentaRequest, uid: str = Header(None),
        token: Optional[str] = Header(None)):
    """Registra un nuevo producto en inventario
    param venta: VentaRequest
    return: int
    """
    try:
        vta_id = VentaDAO.generar(vta)
        generar_ticket(vta)
    except Exception as ex:
        logging.error(f"ventas.generar_venta() - {ex}")
        raise HTTPException(status_code=HTTP_500, detail=str(ex)) from ex

    return vta_id
