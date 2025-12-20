from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.app.accounts.models import User
from src.app.accounts.services.auth import get_current_user, verify_token
from src.__dependencies import get_session
from src.common.kafka_layer.producer.producer import get_producer
from src.app.orders.models import Order
from src.app.orders.schemas.order import OrderOutSchema, OrderCreateSchema
from src.app.orders.schemas.order_with_owner import OrderWithOwnerSchema
from src.app.orders.service import OrderService

router = APIRouter(
    prefix='/orders',
    tags=['orders'],
    dependencies=[Depends(verify_token)],
)


@router.get('/', response_model=list[OrderOutSchema])
async def read_orders(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)):
    """Показать все заказы"""

    orders: list[Order] = await OrderService(session).get_all(skip, limit)
    return orders


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=dict[str, int | str])
async def add_order(
    order: OrderCreateSchema,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Добавить заказ"""

    db_order: Order = await OrderService(session).create(current_user, order)
    await session.commit()

    message = {'order_id': db_order.id, 'customer_email': current_user.email}

    producer = await get_producer()
    async with producer as pd:
        await pd.send_and_wait('orders', message)

    return {'order_id': db_order.id, 'message': f'Заказ №{db_order.id} принят на обработку. (Статус: created)'}


@router.get('/my/', response_model=list[OrderOutSchema])
async def read_my_orders(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Показать заказы текущего пользователя"""

    user_orders: list[Order] = await OrderService(session).get_by_user(current_user, skip, limit)
    return user_orders


@router.get('/with-owner/', response_model=list[OrderWithOwnerSchema])
async def read_orders_with_owner(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)):
    """Показать заказы с владельцем"""

    orders_with_owner: list[Order] = await OrderService(session).get_all_with_owner(skip, limit)
    return orders_with_owner
