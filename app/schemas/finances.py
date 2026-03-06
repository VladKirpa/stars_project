from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from app.models.withdrawal_request import WithdrawalStatus

class PaymentConfirmRequest(BaseModel):
    external_id: str

class UserLeaveRequest(BaseModel):
    user_id: int
    order_id: int

class WithdrawAmountRequest(BaseModel):
    amount: int = Field(..., ge=25, description="Min sum to withdraw is 25 stars")

class WithdrawHistoryResponse(BaseModel):
    id: int
    amount: int
    status: WithdrawalStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)