"""Contiene los métodos decoradores para agregar funcionalidad
de seguridad a los métodos de entrada del servicio
"""

from typing import (Any, Callable)
from functools import wraps
import requests
from fastapi import (Response)
from .constantes import (DUMMY_TOKEN, HTTP_401)
# VALIDAR_TOKEN_URL)


def requiere_token(func: Callable) -> Callable:
    """Wrapper que verifica la validez del token enviado"""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        try:
            # response = requests.post(
            #     url= VALIDAR_TOKEN_URL,
            #     data= { "uid": kwargs["uid"],
            #         "token": kwargs["token"],
            #         "idUsuario": None }
            # )

            # response.raise_for_status()

            if kwargs.get("token") != DUMMY_TOKEN:
                return Response(status_code=HTTP_401)

            return func(*args, **kwargs)
        except requests.HTTPError as error:
            return Response(status_code=error.response.status_code)

    return wrapper
