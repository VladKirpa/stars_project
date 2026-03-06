from fastapi import APIRouter, Depends
from app.database import get_db
from app.schemas.finances import WithdrawAmountRequest, PaymentConfirmRequest, WithdrawHistoryResponse  
from app.schemas.admin import StatusResponse
from app.orm.withdraw_orm import create_withdrawal_request, get_user_withdraw_history
from app.orm.pending_payment_orm import confirm_payment
from app.api.dependencies import get_current_user
from app.models import User
from typing import List


router = APIRouter(prefix="/finances", tags=["User Finances"])

@router.get("/withdraw/history", response_model=List[WithdrawHistoryResponse])
async def api_get_withdraw_history(
    current_user: User = Depends(get_current_user),
    session = Depends(get_db)
):
    #return withdraw history for current user
    history = await get_user_withdraw_history(user_id=current_user.id, session=session)
    return history

@router.post("/withdraw", response_model=StatusResponse)
async def api_create_withdraw(
    data: WithdrawAmountRequest,
    current_user: User = Depends(get_current_user),
    session = Depends(get_db)
):
    result = await create_withdrawal_request(
        user_id=current_user.id, 
        amount=data.amount, 
        session=session
    )
    return StatusResponse(message=result["message"])

@router.post("/payment/confirm")
async def api_confirm_payment(data: PaymentConfirmRequest, session = Depends(get_db)):
    return await confirm_payment(data.external_id, session)



