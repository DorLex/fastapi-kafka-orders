from types import TracebackType
from typing import Any, Self


class MockKafkaProducer:
    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[Exception] | None,
        exc_value: Exception | None,
        exc_traceback: TracebackType | None,
    ) -> None:
        pass

    async def send_and_wait(self, *args: Any, **kwargs: Any) -> bool:
        return True


async def mock_get_producer() -> MockKafkaProducer:
    return MockKafkaProducer()
