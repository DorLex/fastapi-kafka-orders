from collections.abc import AsyncGenerator, Generator
from typing import TYPE_CHECKING, Any

import pytest
from alembic import command
from alembic.config import Config
from fastapi.security import HTTPBasicCredentials
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from starlette.testclient import TestClient

from src.app.bll.accounts.dto.user import UserCreateDTO, UserResponseDTO
from src.app.bll.accounts.services.jwt import JWTService
from src.app.bll.accounts.services.user import UserService
from src.app.dal.accounts.repositories.user import UserRepository
from src.app.main import app
from src.common.constants.paths import BASE_DIR
from src.common.db.dependencies import get_db
from src.common.envs import env_config

if TYPE_CHECKING:
    from src.app.bll.accounts.dto.token import TokenResponseDTO

alembic_config: Config = Config(BASE_DIR / 'alembic.ini')

env_config.postgres_db = 'test_orders_db'


@pytest.fixture(scope='session', autouse=True)
def setup() -> Generator[None, Any]:
    if env_config.postgres_db == 'test_orders_db':
        command.upgrade(alembic_config, 'head')  # накатываем миграции на тестовую БД

        yield  # тут контекст переключается на прогон всех тестов

        command.downgrade(alembic_config, 'base')  # откатываем миграции на тестовой БД

    else:
        raise RuntimeError('Неверные настройки тестов!')


async_test_engine: AsyncEngine = create_async_engine(
    env_config.postgresql_url,
    poolclass=NullPool,  # иначе падает ошибка RuntimeError: ... attached to a different loop
)

TestAsyncSessionMaker: async_sessionmaker[AsyncSession] = async_sessionmaker(
    async_test_engine,
    expire_on_commit=False,
)


async def override_get_db() -> AsyncGenerator[AsyncSession]:
    async with TestAsyncSessionMaker() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db  # подменяем зависимость основной сессии БД на тестовую


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope='session')
async def base_test_user_credentials() -> UserCreateDTO:
    return UserCreateDTO(
        username='test_user',
        email='test_user@email.com',
        password='test_user_password',
    )


@pytest.fixture(scope='session', autouse=True)
async def base_test_user(
    setup: None,  # noqa: ARG001 # чтобы сначала прогрузилась фикстура setup
    base_test_user_credentials: UserCreateDTO,
) -> UserResponseDTO:
    async with TestAsyncSessionMaker() as db:
        user_service: UserService = UserService(UserRepository(db))
        user: UserResponseDTO = await user_service.create_user(base_test_user_credentials)
        await db.commit()

    return user


@pytest.fixture(scope='session')
async def auth_headers(base_test_user_credentials: UserCreateDTO) -> dict[str, str]:
    async with TestAsyncSessionMaker() as db:
        jwt_service: JWTService = JWTService(UserRepository(db))
        token_dto: TokenResponseDTO = await jwt_service.generate_jwt(
            HTTPBasicCredentials(
                username=base_test_user_credentials.username,
                password=base_test_user_credentials.password,
            ),
        )

    return {'Authorization': f'Bearer {token_dto.access_token}'}
