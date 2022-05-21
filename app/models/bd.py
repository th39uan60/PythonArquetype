"""Contiene la configuración de persistencia de datos.
Usando sqlalchemy el consumidor es ignorante del DBMS
"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from ..security import decodificar_base64

SRV_BD = decodificar_base64(getenv("SERVIDORBD"))
USR_BD = decodificar_base64(getenv("USUARIOBD"))
PSW_BD = decodificar_base64(getenv("PASSWORDBD"))
NOMBRE_BD = "pythonarchetype"
# aquí definimos la conexión al MDBS (ya sea postgres o sqlite)
DATABASE_URL = f"postgresql://{USR_BD}:{PSW_BD}@{SRV_BD}/{NOMBRE_BD}"
# DATABASE_URL = f"sqlite:///./possqlite.db"

motor_bd = create_engine(DATABASE_URL)
ModeloBase = declarative_base()
