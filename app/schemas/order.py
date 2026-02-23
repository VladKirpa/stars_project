from decimal import Decimal
import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.models import Task, TaskCompletion
from typing import Literal


class OrderBase(BaseModel):
    
    #id , creator id, subs_amount, reward_for_sub ,created_at, status

    subs_quantity: int = Field(ge=100)
    channel_id: str
    
class OrderCreate(OrderBase):
    
    creator_id: int
    action_type: Literal['SUBSCRIBE_CHANNEL'] # Allowrd action / change here to add new future
    


class OrderRead(OrderCreate):
    id: int
    status: str
    # total_completions: int
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
