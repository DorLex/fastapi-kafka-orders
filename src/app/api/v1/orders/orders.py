from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Depends, Path, Query
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.app.bll.accounts.dependencies.user import get_current_user
from src.app.bll.accounts.dto.user import UserResponseDTO
from src.app.bll.common.dto.filters import PaginationParams
from src.app.bll.orders.dto.filters import OrderFilter
from src.app.bll.orders.dto.order import OrderCreateDTO, OrderNotificationDTO, OrderPartialUpdateDTO, OrderResponseDTO
from src.app.bll.orders.dto.order_with_owner import OrderWithOwnerDTO
from src.app.bll.orders.services.kafka import OrderKafkaService
from src.app.bll.orders.services.order import OrderService
from src.app.dal.orders.repositories.order import OrderRepository
from src.common.constants.kafka import KafkaTopicEnum
from src.common.db.dependencies import get_db
from src.common.kafka_layer.dto import KafkaMessageDTO
from src.common.kafka_layer.producer import get_producer

router: APIRouter = APIRouter(
    prefix='/orders',
    tags=['Orders'],
    dependencies=[Depends(get_current_user)],
)


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


@router.patch('/{order_id}')
async def update_order_partial(
    order_data: OrderPartialUpdateDTO,
    order_id: PositiveInt = Path(gt=0),
    db: AsyncSession = Depends(get_db),
) -> OrderResponseDTO:
    order_service: OrderService = OrderService(OrderRepository(db))
    updated_order: OrderResponseDTO = await order_service.update_order_partial(order_id, order_data)
    await db.commit()

    return updated_order


@router.get('')
async def get_orders(
    filters: OrderFilter = Query(),
    db: AsyncSession = Depends(get_db),
) -> list[OrderResponseDTO]:
    """Получить все заказы."""

    order_service: OrderService = OrderService(OrderRepository(db))
    return await order_service.get_orders_by_filter(filters)


@router.get('/my')
async def get_my_orders(
    filters: PaginationParams = Query(),
    current_user: UserResponseDTO = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[OrderResponseDTO]:
    """Получить заказы текущего пользователя."""

    order_service: OrderService = OrderService(OrderRepository(db))
    order_filter: OrderFilter = OrderFilter(user_id=current_user.id, **filters.model_dump())

    return await order_service.get_orders_by_filter(order_filter)


@router.get('/with-owner')
async def get_orders_with_owner(
    filters: PaginationParams = Query(),
    db: AsyncSession = Depends(get_db),
) -> list[OrderWithOwnerDTO]:
    """Получить заказы с владельцем."""

    order_service: OrderService = OrderService(OrderRepository(db))
    return await order_service.get_orders_with_owner(filters)
