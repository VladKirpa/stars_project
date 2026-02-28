from pydantic import BaseModel
from decimal import Decimal
from typing import Optional, Any, Union

class StatusResponse(BaseModel): # universal response
    status: str = "success"
    message: str
    data: Optional[Any] = None

class CustomOrderCreate(BaseModel): # schema for admin_custom_task
    admin_id: int
    channel_id: str
    subs_quantity: int
    custom_worker_pay: Decimal
    description: str

class WithdrawAction(BaseModel): # approve/reject withdraw schema
    user_id: int
    withdraw_id: int

class ManualTopUpRequest(BaseModel): # manual top up balance schema
    identifier: Union[str, int] # can be @username or user_id
    amount: Decimal
    is_stars_balance: bool

class OrderCancelRequest(BaseModel): # cancel order schema
    order_id: int

class UserBanRequest(BaseModel): # ban/unban schema
    user_id: int