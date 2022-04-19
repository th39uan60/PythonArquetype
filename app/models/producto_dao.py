"""Contiene los métodos CRUD disponibles
para la persistencia de un producto
"""

from sqlalchemy import (Column, Integer, String, Float, DateTime, select)
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from ..schemas.requests import ProductoRequest
from ..schemas.responses import ProductoResponse
from .bd import (ModeloBase, motor_bd)


class ProductoDAO(ModeloBase):
    """Contiene métodos para persistencia de un producto"""
    __tablename__ = "producto"

    sku = Column(Integer, primary_key=True)
    desc = Column(String, nullable=False)
    precio = Column(Float)
    fecha_upd = Column(DateTime)

    def __init__(self, sku, desc, precio):
        # no  autogenerado, depende del código de barras
        self.sku = sku
        self.desc = desc
        self.precio = precio

    @staticmethod
    def obtener(prod_sku: int) -> ProductoResponse:
        """Obtiene un producto desde BD con el SKU proporcionado
        param prod_sku: el id del producto a ser buscado
        return: Producto
        """
        with Session(motor_bd) as sesion_bd:
            # preparamos la consulta indicando el destino y filtros
            consulta = select(ProductoDAO).where(ProductoDAO.sku == prod_sku)
            try:
                # ejecutamos la consulta en BD
                prod_dao = sesion_bd.scalars(consulta).one()
            except NoResultFound:
                prod = None
            else:
                # transformamos el DAO en response (sin fecha de actualizacion)
                prod = ProductoResponse(
                    sku=prod_dao.sku, desc=prod_dao.desc,
                    precio=prod_dao.precio, fecha_upd=None)

        return prod

    @staticmethod
    def registrar(producto: ProductoRequest) -> int:
        """Registra un producto en BD y devuelve el sku generado
        param producto: el producto a ser registrado
        return: int
        """
        with Session(motor_bd) as sesion_bd:
            # transformamos el request en DAO
            prod_dao = ProductoDAO(
                producto.sku, producto.desc, producto.precio)
            # al agregar el objeto se terminará insertando un registro
            sesion_bd.add(prod_dao)
            sesion_bd.commit()
            nuevo_sku = prod_dao.sku

        return nuevo_sku
