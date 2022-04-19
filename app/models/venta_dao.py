# pylint: disable=too-many-arguments
# pylint: disable=too-few-public-methods

"""Contiene los métodos CRUD disponibles
para la persistencia de una venta
"""

from datetime import date
from sqlalchemy import (Column, Integer, Float, DateTime, select, ForeignKey)
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import (Session, relationship)
from ..schemas.requests import VentaRequest
from ..schemas.responses import VentaResponse
from .bd import (ModeloBase, motor_bd)
from .producto_dao import ProductoDAO


class VentaDAO(ModeloBase):
    """Contiene métodos para persistencia de una venta"""
    __tablename__ = "venta"

    vta_id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime)
    cte_id = Column(Integer, nullable=True, default=None)
    subtotal = Column(Float)
    impuesto = Column(Float)
    total = Column(Float)
    prods = relationship(
        "ProductoDAO",
        secondary="productosxventa")

    def __init__(self, fecha, cte_id, subtotal, impuesto, total, prods):
        self.fecha = fecha
        self.cte_id = cte_id
        self.subtotal = subtotal
        self.impuesto = impuesto
        self.total = total
        self.prods = prods

    @staticmethod
    def obtener(vta_id: int) -> VentaResponse:
        """Obtiene una venta desde BD con el id proporcionado
        param id_vta: int
        return: Venta
        """
        with Session(motor_bd) as sesion_bd:
            # preparamos la consulta indicando el destino y filtros
            consulta = select(VentaDAO).where(VentaDAO.vta_id == vta_id)
            try:
                # ejecutamos la consulta en BD
                venta_dao = sesion_bd.scalars(consulta).one()
            except NoResultFound:
                venta = None
            else:
                lista_skus = []
                # obtenemos solo los skus de productos
                for prod in venta_dao.prods:
                    lista_skus += [prod.sku]

                # transformamos el DAO en response
                venta = VentaResponse(
                    vta_id=venta_dao.vta_id, fecha=venta_dao.fecha,
                    prods=lista_skus, subtotal=venta_dao.subtotal,
                    impuesto=venta_dao.impuesto, total=venta_dao.total,
                    cte_id=venta_dao.cte_id)

        return venta

    @staticmethod
    def generar(venta: VentaRequest) -> int:
        """Registra una venta en BD y devuelve el id generado
        param venta: la venta a ser registrada
        return: int
        """
        with Session(motor_bd) as sesion_bd:
            # preparamos la consulta indicando el destino y filtros
            consulta = select(ProductoDAO).where(
                ProductoDAO.sku.in_(venta.prods))

            # ejecutamos la consulta en BD
            lista_prods = sesion_bd.scalars(consulta).all()
            if len(lista_prods) != len(venta.prods):
                raise NoResultFound("Alguno de los productos no existe")

            # transformamos el request en DAO
            venta_dao = VentaDAO(
                date.today(), venta.cte_id, venta.subtotal, venta.impuesto,
                venta.total, lista_prods)
            # al agregar el objeto se terminará insertando un registro
            sesion_bd.add(venta_dao)
            sesion_bd.commit()
            nuevo_id = venta_dao.vta_id

        return nuevo_id


class ProductoXVentaDAO(ModeloBase):
    """Representa los datos de relación muchos-a-muchos entre productos
    y ventas
    """
    __tablename__ = "productosxventa"

    vta_id = Column(Integer, ForeignKey("venta.vta_id"), primary_key=True)
    prod_sku = Column(Integer, ForeignKey("producto.sku"), primary_key=True)
    venta = relationship(VentaDAO, backref="venta")
    producto = relationship(ProductoDAO, backref="producto")

    def __init__(self, vta_id, prod_sku):
        self.vta_id = vta_id
        self.prod_sku = prod_sku
