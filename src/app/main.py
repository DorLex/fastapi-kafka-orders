from fastapi import FastAPI

from src.app.api.v1 import api_v1_router
from src.app.infrastructure.admin_panel.init import init_admin_models
from src.common.logs.config import setup_logging

setup_logging()

app: FastAPI = FastAPI(title='Orders-App')

init_admin_models(app)

app.include_router(api_v1_router)

# TODO: настроить админку
# TODO: обновить README
# TODO: добавить /admin в README
