"""Contiene la configuración de persistencia de datos.
Usando sqlalchemy el consumidor es ignorante del DBMS
"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

USR_BD = getenv("usr_bd")
PSW_BD = getenv("psw_bd")
SERVIDOR_BD = "localhost:5432"
NOMBRE_BD = "prototype"
DATABASE_URL = f"postgresql://{USR_BD}:{PSW_BD}@{SERVIDOR_BD}/{NOMBRE_BD}"
# DATABASE_URL = f"sqlite://pointofsale.bd"

motor_bd = create_engine(DATABASE_URL)
ModeloBase = declarative_base()
