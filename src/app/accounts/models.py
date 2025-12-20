from sqlalchemy import BIGINT, String, Integer, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.common.db import Base


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
