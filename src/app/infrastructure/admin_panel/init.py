from fastapi import FastAPI
from sqladmin import Admin

from src.app.infrastructure.admin_panel.models.order import OrderAdmin
from src.app.infrastructure.admin_panel.models.user import UserAdmin
from src.common.db.connection import async_engine


def init_admin_models(app: FastAPI) -> None:
    admin: Admin = Admin(app, async_engine)

    admin.add_view(UserAdmin)
    admin.add_view(OrderAdmin)
