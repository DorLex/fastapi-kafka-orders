from enum import StrEnum


class KafkaTopicEnum(StrEnum):
    orders = 'orders'


class KafkaGroupEnum(StrEnum):
    order_group = 'order_group'
