"""Se cuenta con los valores constantes / dummy necesarios para
el funcionamiento de los servicios
"""

# definir en el deployment.yaml la info del micro-servicio para validar token
VALIDAR_TOKEN_URL = "/app_blindaje/ms-validar-token"
# HTTP_200 = 200
HTTP_401 = 401
HTTP_404 = 404
HTTP_500 = 500

# token dummy (la validación de seguridad debe hacerse mediante
# el servicio de ms-validar-token)
DUMMY_TOKEN = "851118721195"
