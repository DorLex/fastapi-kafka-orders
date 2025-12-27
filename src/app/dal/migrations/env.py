import asyncio
import importlib
import logging
import pkgutil
from pkgutil import ModuleInfo
from logging import getLogger, INFO, Logger
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from alembic.config import Config
from sqlalchemy import MetaData, pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from src.common.constants.paths import BASE_DIR
from src.common.db import Base
from src.common.envs import env_config

logging.basicConfig(level=INFO)
logger: Logger = getLogger(__name__)


def auto_import_models():
    dal_path: Path = BASE_DIR / 'src/app/dal'

    for models_dir in dal_path.rglob('models'):  # рекурсивный поиск файлов и директорий по шаблону
        if not models_dir.is_dir() or '__pycache__' in str(models_dir):
            continue

        models_dir_relative_path: Path = models_dir.relative_to(BASE_DIR)  # src/app/dal/accounts/models
        models_package_path: str = '.'.join(models_dir_relative_path.parts)  # src.app.dal.accounts.models

        logger.info(f'- Сканируем пакет: {models_package_path}')

        # # Импортируем сам пакет models
        # try:
        #     importlib.import_module(models_package_path)
        #     logger.info(f'-- Пакет загружен')
        # except Exception as exc:
        #     logger.error(f'-- Ошибка загрузки пакета: {exc}')
        #     continue

        # Сканируем все модули внутри пакета models
        for finder, module_name, is_pkg in pkgutil.iter_modules([str(models_dir)]):
            if module_name == '__init__' or is_pkg:
                continue

            full_module_path = f"{models_package_path}.{module_name}"

            try:
                # Импортируем модуль с моделью
                module = importlib.import_module(full_module_path)
                logger.info(f"    📄 Загружен модуль: {module_name}")

                # Дополнительно: можно найти все классы моделей в модуле
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if hasattr(attr, '__table__'):  # Проверяем, что это модель SQLAlchemy
                        logger.info(f"      🎯 Найдена модель: {attr_name}")

            except ImportError as e:
                # Игнорируем ошибки импорта, если модуль требует зависимостей
                logger.info(f"    ⚠️ Не удалось загрузить {module_name}: {e}")
            except Exception as e:
                logger.info(f"    ❌ Ошибка в модуле {module_name}: {e}")


auto_import_models()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config: Config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option('sqlalchemy.url', env_config.postgresql_url)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata: MetaData = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
