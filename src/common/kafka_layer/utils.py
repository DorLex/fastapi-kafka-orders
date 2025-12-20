import json
from typing import TypeVar

T: TypeVar = TypeVar('T')


def serializer(message: T) -> bytes:
    return json.dumps(message).encode('utf-8')


def deserializer(message: bytes) -> T:
    return json.loads(message.decode('utf-8'))
