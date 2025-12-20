from aiokafka import AIOKafkaConsumer

from src.common.constants.kafka import KafkaGroupEnum, KafkaTopicEnum
from src.common.kafka_layer.utils import deserializer
from src.common.settings import config


async def get_consumer(topic: KafkaTopicEnum, group: KafkaGroupEnum):
    if not isinstance(topic, KafkaTopicEnum) or not isinstance(group, KafkaGroupEnum):
        raise ValueError(f'Переданы невалидные значения: {topic=}, {group=}')

    consumer: AIOKafkaConsumer = AIOKafkaConsumer(
        topic,
        group_id=group,
        bootstrap_servers=config.kafka_bootstrap_servers,
        value_deserializer=deserializer,
        key_deserializer=deserializer,
    )

    return consumer
