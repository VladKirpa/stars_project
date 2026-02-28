from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List
from app.database import get_db

from app.schemas.admin import (
    StatusResponse, CustomOrderCreate, WithdrawAction, 
    ManualTopUpRequest, OrderCancelRequest, UserBanRequest
)
from app.orm.admin.create_custom_tasks import create_custom_admin_order
from app.orm.admin.fin_stats import get_global_financial_stats
from app.orm.admin.finances import approve_withdraw_transaction, reject_withdraw_transaction, manual_balance_update
from app.orm.admin.orders import cancel_order_by_admin
from app.orm.admin.user_stats import get_users_list, get_user_profile
from app.orm.admin.user import get_user_logs_paginated, ban_user, unban_user

router = APIRouter(prefix="/admin", tags=["Admin Panel"])

#orders
@router.post("/orders/custom", response_model=StatusResponse)
async def api_create_custom_order(data: CustomOrderCreate, session = Depends(get_db)):
    result = await create_custom_admin_order(
        data.admin_id, data.channel_url, data.subs_quantity, data.custom_worker_pay, data.description, session
    )
    return StatusResponse(message=result["message"], data={"order_id": result["order_id"]})

@router.post("/orders/cancel", response_model=StatusResponse)
async def api_cancel_order(data: OrderCancelRequest, session = Depends(get_db)):
    result = await cancel_order_by_admin(data.order_id, session)
    return StatusResponse(message=result["message"], data={"refunded_amount": result["refunded_amount"]})

# finances and stats
@router.get("/stats/global")
async def api_get_global_stats(session = Depends(get_db)):
    return await get_global_financial_stats(session)

@router.post("/finances/topup", response_model=StatusResponse)
async def api_manual_topup(data: ManualTopUpRequest, session = Depends(get_db)):
    result = await manual_balance_update(data.identifier, data.amount, data.is_stars_balance, session)
    return StatusResponse(message=result["message"], data={"new_balance": result["new_balance"]})

@router.post("/finances/withdraw/approve", response_model=StatusResponse)
async def api_approve_withdraw(data: WithdrawAction, session = Depends(get_db)):
    result = await approve_withdraw_transaction(data.user_id, data.withdraw_id, session)
    return StatusResponse(message=result["message"])

@router.post("/finances/withdraw/reject", response_model=StatusResponse)
async def api_reject_withdraw(data: WithdrawAction, session = Depends(get_db)):
    result = await reject_withdraw_transaction(data.user_id, data.withdraw_id, session)
    return StatusResponse(message=result["message"])

# users
@router.get("/users/list")
async def api_get_users(limit: int = Query(50), offset: int = Query(0), session = Depends(get_db)):
    return await get_users_list(session, limit, offset)

@router.get("/users/profile/{identifier}")
async def api_get_profile(identifier: str, session = Depends(get_db)):
    return await get_user_profile(identifier, session)

@router.get("/users/logs/{identifier}")
async def api_get_logs(identifier: str, limit: int = Query(10), offset: int = Query(0), session = Depends(get_db)):
    return await get_user_logs_paginated(identifier, session, limit, offset)

@router.post("/users/ban", response_model=StatusResponse)
async def api_ban_user(data: UserBanRequest, session = Depends(get_db)):
    result = await ban_user(data.user_id, session)
    return StatusResponse(message=result["message"])

@router.post("/users/unban", response_model=StatusResponse)
async def api_unban_user(data: UserBanRequest, session = Depends(get_db)):
    result = await unban_user(data.user_id, session)
    return StatusResponse(message=result["message"])




# (1, user1, 111, 0, 0, 0, False)
