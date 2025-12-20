from aiokafka import AIOKafkaProducer

from src.common.envs import env_config
from src.common.kafka_layer.utils import serializer


async def get_producer() -> AIOKafkaProducer:
    producer: AIOKafkaProducer = AIOKafkaProducer(
        bootstrap_servers=env_config.kafka_bootstrap_servers,
        value_serializer=serializer,
        key_serializer=serializer,
    )

    return producer
