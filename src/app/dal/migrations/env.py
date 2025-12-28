import asyncio
import importlib
import logging
import pkgutil
from logging import getLogger, INFO, Logger
from logging.config import fileConfig
from pathlib import Path
from pkgutil import ModuleInfo
from types import ModuleType
from typing import Any

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
    """
    Автоматически импортирует все SQLAlchemy-модели, чтобы их видел Alembic.
    """

    dal_path: Path = BASE_DIR / 'src/app/dal'

    for models_dir in dal_path.rglob('models'):  # рекурсивный поиск файлов и директорий по шаблону
        models_dir: Path

        if not models_dir.is_dir() or '__pycache__' in str(models_dir):
            continue

        _models_dir_relative_path: Path = models_dir.relative_to(BASE_DIR)  # src/app/dal/accounts/models
        models_package_path: str = '.'.join(_models_dir_relative_path.parts)  # src.app.dal.accounts.models

        for module_info in pkgutil.iter_modules([str(models_dir)]):
            module_info: ModuleInfo

            if module_info.name == '__init__' or module_info.ispkg:
                continue

            full_module_path: str = f'{models_package_path}.{module_info.name}'

            try:
                module: ModuleType = importlib.import_module(full_module_path)
                logger.info(f'- Импортирован модуль: {full_module_path}')

                for module_attr_name in dir(module):
                    module_attr: Any = getattr(module, module_attr_name)

                    if hasattr(module_attr, '__table__'):  # если это модель SQLAlchemy
                        logger.info(f'-- Импортирована модель: {module_attr_name}')

            except Exception as exc:
                logger.error(f'-- Ошибка при импорте модуля {full_module_path}: {exc}')
                raise exc


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
