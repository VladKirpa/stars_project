from decimal import Decimal
import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal, Optional

class OrderBase(BaseModel):
    subs_quantity: int
    channel_id: str

class OrderCreate(OrderBase):
    creator_id: int
    action_type: Literal['SUBSCRIBE_CHANNEL']
    description: str

class OrderRead(OrderCreate):
    id: int
    status: str
    current_subs: int = 0
    created_at: Optional[datetime.datetime] = None
    reward_for_sub: Decimal = Decimal('0.0')
    worker_pay: Decimal = Decimal('0.0')

    model_config = ConfigDict(from_attributes=True)



class OrderShortRead(BaseModel):
    action_type: Literal['SUBSCRIBE_CHANNEL']
    description: str | None = None
    channel_id: str
    
    model_config = ConfigDict(from_attributes=True)