from enum import StrEnum


class OrderStatusEnum(StrEnum):
    new = 'new'
    in_processing = 'in_processing'
    completed = 'completed'
    canceled = 'canceled'
    failed = 'failed'
