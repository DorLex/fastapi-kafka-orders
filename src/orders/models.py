from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.common.db import Base
from src.orders.enums import OrderStatusEnum


class OrderModel(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))

    status: Mapped[OrderStatusEnum] = mapped_column(
        ENUM(OrderStatusEnum, name='order_status_enum'),
        nullable=False,
        default=OrderStatusEnum.created,
    )

    description: Mapped[str] = mapped_column(String)

    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    owner: Mapped['UserModel'] = relationship(
        back_populates='orders',
        lazy='joined',
    )

    def __repr__(self) -> str:
        return f'Order(id={self.id!r}, title={self.title!r})'
