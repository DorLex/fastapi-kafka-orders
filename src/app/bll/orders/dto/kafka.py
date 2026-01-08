from pydantic import BaseModel


class KafkaMessageDTO(BaseModel):
    order_id: int
