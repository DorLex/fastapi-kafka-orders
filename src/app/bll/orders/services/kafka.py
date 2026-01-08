from aiokafka import AIOKafkaProducer

from src.app.bll.orders.dto.kafka import KafkaMessageDTO
from src.common.constants.kafka import KafkaTopicEnum


class OrderKafkaService:
    def __init__(self, producer: AIOKafkaProducer) -> None:
        self.producer = producer

    async def send_message(self, topic: KafkaTopicEnum, kafka_msg: KafkaMessageDTO) -> None:
        if not isinstance(topic, KafkaTopicEnum):
            raise ValueError(f'Передано невалидное значения топика: {topic=}')

        async with self.producer as prd:
            await prd.send_and_wait(
                topic,
                value=kafka_msg.model_dump(mode='json'),
            )
