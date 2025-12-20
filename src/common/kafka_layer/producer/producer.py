from aiokafka import AIOKafkaProducer

from src.common.kafka_layer.config import KAFKA_BOOTSTRAP_SERVERS
from src.common.kafka_layer.utils import serializer


async def get_producer():
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=serializer,
    )

    return producer
