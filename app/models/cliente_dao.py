"""Contiene los métodos CRUD disponibles
para la persistencia de un cliente
"""

from sqlalchemy import (Column, Integer, String, DateTime, select)
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from ..schemas.requests import ClienteRequest
from ..schemas.responses import ClienteResponse
from .bd import (ModeloBase, motor_bd)


class ClienteDAO(ModeloBase):
    """Contiene métodos para persistencia de un cliente"""
    __tablename__ = "cliente"

    cte_id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    fecha_nac = Column(DateTime)

    def __init__(self, cte_id, nombre, apellidos, fecha_nac):
        # no  autogenerado, depende del código de barras
        self.cte_id = cte_id
        self.nombre = nombre
        self.apellidos = apellidos
        self.fecha_nac = fecha_nac

    @staticmethod
    def obtener(cte_id: int) -> ClienteResponse:
        """Obtiene un cliente desde BD con el id proporcionado
        param cte_id: el id de cliente a buscar
        return: Cliente
        """

        with Session(motor_bd) as sesion_bd:
            # preparamos la consulta indicando el destino y filtros
            consulta = select(ClienteDAO).where(ClienteDAO.cte_id == cte_id)

            try:
                # ejecutamos la consulta en BD
                cte_dao = sesion_bd.scalars(consulta).one()
                # transformamos el DAO en response
                cte = ClienteResponse(
                    cte_id=cte_dao.cte_id, nombre=cte_dao.nombre,
                    apellidos=cte_dao.apellidos, fecha_nac=cte_dao.fecha_nac)
            except NoResultFound:
                cte = None

        return cte

    @staticmethod
    def dar_alta(cliente: ClienteRequest) -> int:
        """Registra un cliente nuevo en BD y devuelve el id generado
        param cliente: el cliente a dar de alta
        return: int
        """
        with Session(motor_bd) as sesion_bd:
            # transformamos el request en DAO
            cliente_dao = ClienteDAO(
                cliente.cte_id, cliente.nombre, cliente.apellidos,
                cliente.fecha_nac)
            # al agregar el objeto se terminará insertando un registro
            sesion_bd.add(cliente_dao)
            sesion_bd.commit()
            nuevo_id = cliente_dao.cte_id

        return nuevo_id
