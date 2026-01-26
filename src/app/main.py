from fastapi import FastAPI

from src.app.api.v1 import api_v1_router
from src.common.logs.config import setup_logging

setup_logging()

app: FastAPI = FastAPI(title='Orders-App')

app.include_router(api_v1_router)

# TODO: обновить тесты
# TODO: проверить ручки после переименования папок
# TODO: добавить накатку миграций в докере
# TODO: добавить админку
# TODO: обновить README
