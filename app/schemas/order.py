from decimal import Decimal
import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.models import Task, TaskCompletion
from typing import Literal
from app.config import DEFAULT_REWARD_FOR_SUB, DEFAULT_WORKER_PAY


class OrderBase(BaseModel):
    
    #id , creator id, subs_amount, reward_for_sub ,created_at, status

    subs_quantity: int = Field(ge=100)
    channel_id: str
    
class OrderCreate(OrderBase):
    
    creator_id: int
    action_type: Literal['SUBSCRIBE_CHANNEL'] # Allowed action / change here to add new options
    description: str


class OrderRead(OrderCreate):
    id: int
    status: str
    # total_completions: int
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)



class OrderShortRead(BaseModel):
    action_type: Literal['SUBSCRIBE_CHANNEL']
    description: str | None = None
    channel_id: str
    
    model_config = ConfigDict(from_attributes=True)