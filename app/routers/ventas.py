# pylint: disable=unused-argument

"""Contiene los métodos CRUD de la API relacionados con
la administración de ventas
"""

from typing import Optional
from fastapi import (APIRouter, Header, HTTPException)
from ..schemas.requests import VentaRequest
from ..schemas.responses import VentaResponse
from ..models.venta_dao import VentaDAO
from ..security import requiere_token
from ..constantes import (HTTP_404, HTTP_500)

router = APIRouter()


@router.get("/ventas/{vta_id}", response_model=VentaResponse)
@requiere_token
def obtener_venta(vta_id: int, token: Optional[str] = Header(None)):
    """Obtiene una venta por medio de su id
    param vta_id: id de la venta a buscar
    return: Venta
    """
    try:
        venta = VentaDAO.obtener(vta_id)
    except Exception as ex:
        raise HTTPException(status_code=HTTP_500, detail=str(ex)) from ex
    else:
        if venta is None:
            raise HTTPException(
                status_code=HTTP_404,
                detail="No existe venta con el ID proporcionado")

    return venta


@router.post("/ventas/", response_model=int)
@requiere_token
def generar_venta(vta: VentaRequest, token: Optional[str] = Header(None)):
    """Registra un nuevo producto en inventario
    param venta: VentaRequest
    return: int
    """
    try:
        vta_id = VentaDAO.generar(vta)
    except Exception as ex:
        raise HTTPException(status_code=HTTP_500, detail=str(ex)) from ex

    return vta_id
