from aiokafka import AIOKafkaConsumer

from src.common.constants.kafka import KafkaGroupEnum, KafkaTopicEnum
from src.common.envs import env_config
from src.common.kafka_layer.utils import deserializer


async def get_consumer(topic: KafkaTopicEnum, group: KafkaGroupEnum) -> AIOKafkaConsumer:
    if not isinstance(topic, KafkaTopicEnum) or not isinstance(group, KafkaGroupEnum):
        raise ValueError(f'Переданы невалидные значения: {topic=}, {group=}')

    consumer: AIOKafkaConsumer = AIOKafkaConsumer(
        topic,
        group_id=group,
        bootstrap_servers=env_config.kafka_bootstrap_servers,
        value_deserializer=deserializer,
        key_deserializer=deserializer,
    )

    return consumer
