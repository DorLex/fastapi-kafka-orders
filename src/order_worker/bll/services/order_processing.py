import asyncio
import logging
from logging import INFO, Logger, getLogger

from aiokafka import AIOKafkaConsumer, ConsumerRecord

from src.app.bll.orders.dto.order import OrderPartialUpdateDTO, OrderResponseDTO
from src.app.bll.orders.services.order import OrderService
from src.app.dal.orders.repositories.order import OrderRepository
from src.common.constants.order import OrderStatusEnum
from src.common.db.connection import AsyncSessionMaker
from src.common.kafka_layer.dto import KafkaMessageDTO

logging.basicConfig(level=INFO)  # TODO: убрать
logger: Logger = getLogger(__name__)


class OrderProcessingService:
    def __init__(self, consumer: AIOKafkaConsumer) -> None:
        self.consumer = consumer

    async def process_new_orders(self) -> None:
        async with self.consumer as cns:
            async for raw_message in cns:
                try:
                    await self._process_order(raw_message)
                except Exception:  # чтобы сервис не падал полностью при рандомной ошибке
                    logger.exception('Ошибка при работе consumer')

    async def _process_order(self, raw_message: ConsumerRecord) -> None:
        raw_message_value: dict | None = raw_message.value

        logger.info(f'Принят запрос из топика: {raw_message_value}')
        if not raw_message_value:
            return

        kafka_msg: KafkaMessageDTO = KafkaMessageDTO(**raw_message_value)

        async with AsyncSessionMaker() as db:
            order_service: OrderService = OrderService(OrderRepository(db))
            order: OrderResponseDTO | None = await order_service.get_order_by_id(kafka_msg.order_id)
            if not order:
                logger.warning(f'Заказ {kafka_msg.order_id} не найден.')
                return

            await order_service.update_order_partial(
                kafka_msg.order_id,
                OrderPartialUpdateDTO(status=OrderStatusEnum.in_processing),
            )
            await db.commit()

            await self._count_order_products()

            await order_service.update_order_partial(
                kafka_msg.order_id,
                OrderPartialUpdateDTO(status=OrderStatusEnum.completed),
            )
            await db.commit()

    async def _count_order_products(self) -> None:
        """Имитация обработки заказа."""
        await asyncio.sleep(5)
