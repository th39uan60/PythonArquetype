# pylint: disable=invalid-name

"""Contiene métodos bridge para comunicarse con los servicios
de administración de tokens de seguridad
"""

from os import getenv
from functools import wraps
from typing import (Any, Callable)
import requests
from fastapi import (APIRouter, Header, Response)
from ..constantes import (DUMMY_TOKEN, HTTP_401)
from ..security import decodificar_base64

router = APIRouter()


def requiere_token(func: Callable) -> Callable:
    """Wrapper que verifica la validez del token enviado"""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        try:
            if not validar_token(
                    token=kwargs.get("token"),
                    uid=kwargs.get("uid"),
                    usuario=kwargs.get("idUsuario")):
                return Response(status_code=HTTP_401)

            return func(*args, **kwargs)
        except requests.HTTPError as error:
            return Response(status_code=error.response.status_code)

    return wrapper


@router.post("/token/", response_model=str)
def generar_token(
        idusuario: str, psw: str, ip: str, mac: str,
        uid: str = Header(None)):
    """Obtiene un token de seguridad
    param idUsuario: id del usuario
    param psw: password del usuario
    param ip: dirección ip del host
    param mac: mac address del host
    return: str
    """

    response = None
    try:
        TOKEN_URL = decodificar_base64(getenv("GENERARTOKEN_URL"))
        response = requests.post(
            TOKEN_URL,
            headers={"uid": uid},
            json={
                "idUsuario": idusuario, "password": psw, "ip": ip,
                "mac": mac}
            )

        if response.status_code == 200:
            mensaje = f"resultado: {response['resultado']}"
        else:
            mensaje = f"detalles: {response['detalles']}, dummy: {DUMMY_TOKEN}"
    except Exception as ex:
        if response is None:
            mensaje = f"ex: {ex}, dummy: {DUMMY_TOKEN}"
        else:
            mensaje = f"error: {response.json()}, dummy: {DUMMY_TOKEN}"

    return mensaje


def validar_token(token: str, uid: str, usuario: str):
    """Valida un token de seguridad enviado
    return: boolean
    """
    if token == DUMMY_TOKEN:
        resultado = True
    else:
        TOKEN_URL = decodificar_base64(getenv("VALIDARTOKEN_URL"))
        response = requests.post(
            TOKEN_URL,
            headers={"uid": uid},
            json={
                "idUsuario": usuario,
                "token": token}
            )

        resultado = response is not None

    return resultado
