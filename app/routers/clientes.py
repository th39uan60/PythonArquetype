# pylint: disable=unused-argument

"""Contiene los métodos CRUD de la API relacionados con
la administración de clientes
"""

from typing import Optional
import logging
from fastapi import (APIRouter, Header, HTTPException)
from ..schemas.requests import ClienteRequest
from ..schemas.responses import ClienteResponse
from ..models.cliente_dao import ClienteDAO
from .token import requiere_token
from ..constantes import (HTTP_404, HTTP_500)

router = APIRouter()


@router.get("/pos/clientes/{cte_id}", response_model=ClienteResponse)
@requiere_token
def obtener_cliente(
        cte_id: int, uid: str = Header(None),
        token: Optional[str] = Header(None)):
    """Obtiene un cliente por medio de su id
    param cte_id: id del cliente a buscar
    return: Cliente
    """
    try:
        cliente = ClienteDAO.obtener(cte_id)
    except Exception as ex:
        logging.error(f"clientes.obtener_cliente() - {ex}")
        raise HTTPException(status_code=HTTP_500, detail=str(ex)) from ex
    else:
        if cliente is None:
            raise HTTPException(
                status_code=HTTP_404,
                detail="No existe cliente con el ID proporcionado")

    return cliente


@router.post("/pos/clientes/", response_model=int)
@requiere_token
def alta_cliente(
        cte: ClienteRequest, uid: str = Header(None),
        token: Optional[str] = Header(None)):
    """Da de alta un cliente en la base de datos
    param prod: ClienteRequest
    return: int
    """
    try:
        cte_id = ClienteDAO.dar_alta(cte)
    except Exception as ex:
        logging.error(f"clientes.alta_cliente() - {ex}")
        raise HTTPException(status_code=HTTP_500, detail=str(ex)) from ex

    return cte_id
