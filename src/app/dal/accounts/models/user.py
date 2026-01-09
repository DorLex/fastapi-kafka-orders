from typing import TYPE_CHECKING

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.db.base_model import Base

if TYPE_CHECKING:
    from src.app.dal.orders.models.order import Order


class User(Base):
    __tablename__: str = 'user'

    username: Mapped[str] = mapped_column(Text, unique=True)
    email: Mapped[str] = mapped_column(Text, unique=True)
    hashed_password: Mapped[str] = mapped_column(Text)

    orders: Mapped[list['Order']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
    )

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, username={self.username!r})'
