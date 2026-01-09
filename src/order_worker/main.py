import asyncio
from logging import Logger, getLogger

from src.order_worker.api.consumer import consumer_listening

logger: Logger = getLogger(__name__)

if __name__ == '__main__':
    logger.info('AIOKafkaConsumer Running...')
    asyncio.run(consumer_listening())
