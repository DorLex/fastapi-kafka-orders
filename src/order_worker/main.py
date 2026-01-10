import asyncio

from src.order_worker.api.consumer import consumer_listening

if __name__ == '__main__':
    asyncio.run(consumer_listening())
