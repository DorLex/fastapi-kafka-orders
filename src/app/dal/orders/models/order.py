from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.constants.order import OrderStatusEnum
from src.common.db.objs import Base


class Order(Base):
    __tablename__: str = 'order'

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))

    title: Mapped[str] = mapped_column(Text)
    status: Mapped[OrderStatusEnum] = mapped_column(Text, nullable=False, default=OrderStatusEnum.new)
    description: Mapped[str] = mapped_column(Text)

    user: Mapped['User'] = relationship(
        back_populates='orders',
        lazy='joined',
    )

    def __repr__(self) -> str:
        return f'Order(id={self.id!r}, title={self.title!r})'
