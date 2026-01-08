from aiokafka import ConsumerRecord

from src.order_worker.__service import OrderProcessor


async def run_order_processing(consumer_message: ConsumerRecord):
    order_id = consumer_message.value.get('order_id')
    customer_email = consumer_message.value.get('customer_email')

    order_processing_service = OrderProcessor()
    await order_processing_service.execute_order(order_id, customer_email)
