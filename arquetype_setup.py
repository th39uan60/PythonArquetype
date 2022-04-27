# open file directly (execution directory matters)
from app.models import bd

# this creates all related tables if they not exist
bd.ModeloBase.metadata.create_all(bd.motor_bd)