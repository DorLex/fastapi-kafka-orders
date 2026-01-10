from typing import TYPE_CHECKING

from src.common.constants.kafka import KafkaGroupEnum, KafkaTopicEnum
from src.common.kafka_layer.consumer import get_consumer
from src.order_worker.bll.services.order_processing import OrderProcessingService

if TYPE_CHECKING:
    from aiokafka import AIOKafkaConsumer


async def consumer_listening() -> None:
    consumer: AIOKafkaConsumer = await get_consumer(KafkaTopicEnum.orders, KafkaGroupEnum.order_group)
    order_processing_service: OrderProcessingService = OrderProcessingService(consumer)
    await order_processing_service.process_new_orders()
