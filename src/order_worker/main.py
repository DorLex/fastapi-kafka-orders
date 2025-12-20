import asyncio

from src.common.kafka_layer import consumer_listening

if __name__ == '__main__':
    asyncio.run(consumer_listening())
