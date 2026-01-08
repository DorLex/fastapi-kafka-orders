import json
from logging import getLogger, Logger
from typing import TypeVar

logger: Logger = getLogger(__name__)

T: TypeVar = TypeVar('T')


def serializer(message: T) -> bytes:
    return json.dumps(message).encode('utf-8')


def deserializer(message: bytes) -> T | None:
    try:
        return json.loads(message.decode('utf-8'))
    except Exception as exc:
        logger.error(f'Ошибка при десериализации сообщения: {type(exc)} | {exc}')

    return None
