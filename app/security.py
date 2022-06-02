"""Contiene los métodos decoradores para agregar funcionalidad
de seguridad a los métodos de entrada del servicio
"""

import base64


def decodificar_base64(texto_codificado: str):
    """Decodifica un texto base 64"""
    bytes_base64 = texto_codificado.encode('ascii')
    bytes_decodificado = base64.b64decode(bytes_base64)

    return bytes_decodificado.decode('ascii')
