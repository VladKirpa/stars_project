from pydantic import BaseModel

class WithdrawRequest(BaseModel):
    user_id: int
    amount: int

class PaymentConfirmRequest(BaseModel):
    external_id: str

class UserLeaveRequest(BaseModel):
    user_id: int
    order_id: int