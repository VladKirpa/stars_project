from fastapi import APIRouter, Depends

from app.database import get_db
from app.schemas.finances import WithdrawRequest, PaymentConfirmRequest
from app.schemas.admin import StatusResponse
from app.orm.withdraw_orm import create_withdrawal_request
from app.orm.pending_payment_orm import confirm_payment

router = APIRouter(prefix="/finances", tags=["User Finances"])

@router.post("/withdraw", response_model=StatusResponse)
async def api_create_withdraw(data: WithdrawRequest, session = Depends(get_db)):

    result = await create_withdrawal_request(data.user_id, data.amount, session)
    return StatusResponse(message=result["message"])

@router.post("/payment/confirm")
async def api_confirm_payment(data: PaymentConfirmRequest, session = Depends(get_db)):

    return await confirm_payment(data.external_id, session) # return dict with updated balance 