import asyncio

from src.common.logs.config import setup_logging
from src.order_worker.api.consumer import consumer_listening

if __name__ == '__main__':
    setup_logging()
    asyncio.run(consumer_listening())
