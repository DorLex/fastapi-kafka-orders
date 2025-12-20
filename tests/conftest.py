from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.accounts.schemas.user import UserOutSchema
from src.common.db import Base, get_db
from src.__dependencies import get_session
from src.main import app as main_app
from .config import MODE, async_engine_test, SessionTest


@pytest.fixture(scope='session', autouse=True)
async def prepare_db():
    assert MODE == 'TEST'

    async with async_engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with async_engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionTest() as session:
        yield session


main_app.dependency_overrides[get_db] = override_get_session


@pytest.fixture(scope='session')
def app():
    return main_app


@pytest.fixture(scope='session')
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as async_client:
        yield async_client


@pytest.fixture(scope='session')
async def base_test_user_data():
    return {
        'username': 'base_test_user',
        'email': 'base-test-user@test.com',
        'password': '123456789',
    }


@pytest.fixture(scope='session')
async def base_test_user(app: FastAPI, prepare_db, client: AsyncClient, base_test_user_data):
    url = app.url_path_for('user_registration')
    response = await client.post(url, json=base_test_user_data)

    assert response.status_code == status.HTTP_201_CREATED, response.text

    return UserOutSchema(**response.json())


@pytest.fixture(scope='session')
async def access_token(app: FastAPI, base_test_user, client: AsyncClient, base_test_user_data):
    url = app.url_path_for('login_by_access_token')
    response = await client.post(url, data=base_test_user_data)

    assert response.status_code == status.HTTP_200_OK, response.text

    return response.json().get('access_token')


@pytest.fixture(scope='session')
async def auth_headers(access_token):
    return {'Authorization': f'Bearer {access_token}'}
