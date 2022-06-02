# pylint: disable=invalid-name

"""Sirve para administrar los tickets de venta"""

from os import getenv
from time import time
from pykafka import KafkaClient
from .schemas.requests import VentaRequest
from .security import decodificar_base64


def generar_ticket(venta: VentaRequest):
    """Envía los datos necesarios para generar un ticket de venta"""

    mensaje_json = f"\"c\":\"{venta.cte_id}\", \"p\":\"{venta.prods}\", \
\"s\":\"{venta.subtotal}\", \"f\":\"{venta.impuesto}\", \
\"t\":\"{venta.total}\", \"d\":\"{time()}\""
    enviar_ticket("{" + mensaje_json + "}")


def enviar_ticket(mensaje: str):
    """Configura la conexión a kafka y envía el mensaje
    con la información del ticket
    """
    KAFKA_URL = decodificar_base64(getenv("KAFKAURL"))
    TICKETS_TOPIC = decodificar_base64(getenv("KAFKATICKETS"))

    client = KafkaClient(hosts=KAFKA_URL)
    prod = client.topics[TICKETS_TOPIC].get_producer()

    prod.produce(message=bytes(mensaje, 'utf-8'))
