from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.app.bll.accounts.dependencies.user import get_current_user
from src.app.bll.accounts.dto.user import UserResponseDTO
from src.common.kafka_layer.dto import KafkaMessageDTO
from src.app.bll.orders.dto.order import OrderCreateDTO, OrderNotificationDTO, OrderResponseDTO
from src.app.bll.orders.dto.order_with_owner import OrderWithOwnerDTO
from src.app.bll.orders.services.kafka import OrderKafkaService
from src.app.bll.orders.services.order import OrderService
from src.app.dal.orders.repositories.order import OrderRepository
from src.common.constants.kafka import KafkaTopicEnum
from src.common.db.dependencies import get_db
from src.common.kafka_layer.producer import get_producer

router: APIRouter = APIRouter(
    prefix='/orders',
    tags=['Orders'],
    dependencies=[Depends(get_current_user)],
)


@router.get('')
async def get_orders(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> list[OrderResponseDTO]:
    """Получить все заказы."""

    order_service: OrderService = OrderService(OrderRepository(db))
    return await order_service.get_orders(skip, limit)


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    order_data: OrderCreateDTO,
    current_user: UserResponseDTO = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> OrderNotificationDTO:
    """Создать заказ."""

    order_service: OrderService = OrderService(OrderRepository(db))
    order: OrderResponseDTO = await order_service.create_order(current_user.id, order_data)
    await db.commit()

    producer: AIOKafkaProducer = await get_producer()
    order_kafka_service: OrderKafkaService = OrderKafkaService(producer)

    kafka_msg: KafkaMessageDTO = KafkaMessageDTO(order_id=order.id)
    await order_kafka_service.send_message(KafkaTopicEnum.orders, kafka_msg)

    return OrderNotificationDTO(order_id=order.id, message=f'Заказ №{order.id} принят в обработку.')


@router.get('/my')
async def get_my_orders(
    skip: int = 0,
    limit: int = 100,
    current_user: UserResponseDTO = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[OrderResponseDTO]:
    """Получить заказы текущего пользователя."""

    order_service: OrderService = OrderService(OrderRepository(db))
    # TODO: сделать общий фильтр?
    return await order_service.get_order_by_user(current_user.id, skip, limit)


@router.get('/with-owner')
async def get_orders_with_owner(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> list[OrderWithOwnerDTO]:
    """Получить заказы с владельцем."""

    order_service: OrderService = OrderService(OrderRepository(db))
    return await order_service.get_orders_with_owner(skip, limit)
