from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.app.bll.accounts.dependencies.user import get_current_user
from src.app.bll.accounts.dto.user import UserResponseDTO
from src.app.bll.accounts.services.jwt import JWTService
from src.app.bll.orders.dto.order import OrderCreateSchema, OrderResponseDTO
from src.app.bll.orders.dto.order_with_owner import OrderWithOwnerDTO
from src.app.bll.orders.services.order import OrderService
from src.app.dal.orders.models.order import Order
from src.app.dal.orders.repositories.order import OrderRepository
from src.common.db.dependencies import get_db
from src.common.kafka_layer.producer.producer import get_producer

router: APIRouter = APIRouter(
    prefix='/orders',
    tags=['Orders'],
    dependencies=[Depends(JWTService.decode_token)],
)


@router.get(
    '',
    response_model=list[OrderResponseDTO],
)
async def get_orders(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> list[Order]:
    """Получить все заказы."""

    order_service: OrderService = OrderService(OrderRepository(db))
    return await order_service.get_orders(skip, limit)


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
)
async def create_order(
    order: OrderCreateSchema,
    current_user: UserResponseDTO = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Создать заказ."""

    order_service: OrderService = OrderService(OrderRepository(db))
    order: Order = await order_service.create_order(current_user.id, order)
    await db.commit()

    # TODO: сделать DTO для кафка-сообщений
    message = {'order_id': order.id, 'customer_email': current_user.email}

    # TODO: вынести это в отдельный сервис или в OrderService?
    producer: AIOKafkaProducer = await get_producer()
    async with producer as pd:
        await pd.send_and_wait('orders', message)

    # TODO: вернуть DTO
    return {'order_id': order.id, 'message': f'Заказ №{order.id} принят на обработку. (Статус: new)'}


@router.get(
    '/my',
    response_model=list[OrderResponseDTO],
)
async def get_my_orders(
    skip: int = 0,
    limit: int = 100,
    current_user: UserResponseDTO = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[Order]:
    """Получить заказы текущего пользователя."""

    order_service: OrderService = OrderService(OrderRepository(db))
    return await order_service.get_order_by_user(current_user.id, skip, limit)


@router.get(
    '/with-owner',
    response_model=list[OrderWithOwnerDTO],
)
async def get_orders_with_owner(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)) -> list[Order]:
    """Получить заказы с владельцем."""

    order_service: OrderService = OrderService(OrderRepository(db))
    return await order_service.get_orders_with_owner(skip, limit)
