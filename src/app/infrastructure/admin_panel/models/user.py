from typing import ClassVar

from sqladmin import ModelView
from sqlalchemy.orm import InstrumentedAttribute

from src.app.infrastructure.accounts.models.user import User


class UserAdmin(ModelView, model=User):
    column_list: ClassVar[list[str | InstrumentedAttribute]] = [User.id, User.username, User.email]
    form_excluded_columns: ClassVar[list[str | InstrumentedAttribute]] = [User.created_at, User.updated_at]
