import logging
from logging import getLogger, INFO, Logger

from aiokafka import AIOKafkaConsumer, ConsumerRecord

from src.common.constants.kafka import KafkaGroupEnum, KafkaTopicEnum
from src.common.kafka_layer.consumer import get_consumer
from src.common.kafka_layer.dto import KafkaMessageDTO

logging.basicConfig(level=INFO)  # TODO: убрать
logger: Logger = getLogger(__name__)


async def consumer_listening() -> None:
    consumer: AIOKafkaConsumer = await get_consumer(KafkaTopicEnum.orders, KafkaGroupEnum.order_group)

    async with consumer as cns:
        logger.info(f'AIOKafkaConsumer listening topic="{KafkaTopicEnum.orders}"')

        async for raw_message in cns:
            try:
                raw_message: ConsumerRecord
                raw_message_value: dict | None = raw_message.value

                logger.info(f'Принят запрос из топика: {raw_message_value}')

                if not raw_message_value:
                    continue

                kafka_msg: KafkaMessageDTO = KafkaMessageDTO(**raw_message_value)

                print(f'=== Тут будет обработка заказа {kafka_msg} === ')

            except Exception as exc:  # чтобы сервис не падал полностью при рандомной ошибке
                logger.exception(exc)
