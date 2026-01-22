import importlib
import pkgutil
from logging import Logger, getLogger
from pathlib import Path
from pkgutil import ModuleInfo
from types import ModuleType
from typing import Any

from src.common.constants.paths import BASE_DIR

logger: Logger = getLogger(__name__)


class ModelAutoImporter:
    """Автоматически импортирует все SQLAlchemy-модели, чтобы их видел Alembic."""

    @classmethod
    def import_models(cls) -> None:
        infrastructure_path: Path = BASE_DIR / 'src/app/infrastructure'

        for models_path in infrastructure_path.rglob('models'):  # рекурсивный поиск файлов и директорий по шаблону
            models_path: Path  # абсолютный путь до пакета models

            if not models_path.is_dir() or '__pycache__' in str(models_path):
                continue

            cls._iter_models_package(models_path)

    @classmethod
    def _iter_models_package(cls, models_path: Path) -> None:
        _models_dir_relative_path: Path = models_path.relative_to(BASE_DIR)  # src/app/infrastructure/accounts/models
        models_package_path: str = '.'.join(_models_dir_relative_path.parts)  # src.app.infrastructure.accounts.models

        for module_info in pkgutil.iter_modules([str(models_path)]):
            module_info: ModuleInfo

            if module_info.name == '__init__' or module_info.ispkg:
                continue

            # src.app.infrastructure.accounts.models.user
            full_module_path: str = f'{models_package_path}.{module_info.name}'

            cls._import_module(full_module_path)

    @classmethod
    def _import_module(cls, full_module_path: str) -> None:
        try:
            module: ModuleType = importlib.import_module(full_module_path)
            logger.info(f'- Импортирован модуль: {full_module_path}')

            cls._log_detected_models(module)

        except Exception as exc:
            logger.error(f'-- Ошибка при импорте модуля {full_module_path}: {exc}')
            raise exc

    @classmethod
    def _log_detected_models(cls, module: ModuleType) -> None:
        for module_attr_name in dir(module):
            module_attr: Any = getattr(module, module_attr_name)

            if hasattr(module_attr, '__table__'):  # если это модель SQLAlchemy
                logger.info(f'-- Импортирована модель: {module_attr_name}')
