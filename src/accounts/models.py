from sqlalchemy import String, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.common.db import Base


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)

    hashed_password: Mapped[str] = mapped_column(String)

    orders: Mapped[list['OrderModel']] = relationship(
        back_populates='owner',
        cascade='all, delete-orphan',
    )

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, username={self.username!r})'
