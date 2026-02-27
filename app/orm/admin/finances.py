from app.models import Order, Task, TaskCompletion, User
from app.models.transaction_log import WalletType, ActionType, TransactionLog
from app.models.withdrawal_request import WithdrawalRequest, WithdrawalStatus
from app.models.task import CompletionStatus
from sqlalchemy import select, update, delete, func, join, insert, and_, outerjoin
from sqlalchemy.orm import selectinload
from app.schemas.order import OrderCreate, OrderRead
from typing import List
import asyncio
from decimal import Decimal
from app.config import SYSTEM_BANK_ID
from fastapi import HTTPException

async def approve_withdraw_transaction(user_id:int, withdraw_id:int, session): # change status in WithdrawRequest table to approved
    try:
        withdraw_order = await session.scalar(
            select(WithdrawalRequest)
            .where(withdraw_id == WithdrawalRequest.id)
            .with_for_update()
        )

        if not withdraw_order:
            raise HTTPException(status_code=400, detail='Withdraw order not found')
        
        if withdraw_order.status != WithdrawalStatus.PENDING:
            raise HTTPException(status_code=400, detail='Order already processed')

        user = await session.scalar(select(User).where(user_id == User.id))
        
        if not user:
            raise HTTPException(status_code=400, detail='Order not found')
        

        approve_bill = TransactionLog(
            user_id=user.id,
            amount=withdraw_order.amount,
            wallet_type=WalletType.WITHDRAW,
            action_type=ActionType.WITHDRAW_APPROVED
        )
        withdraw_order.status = WithdrawalStatus.APPROVED
        session.add(approve_bill)
        await session.commit()

    except HTTPException as http_exc:
        await session.rollback()
        raise http_exc
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f'Error {str(e)}')


async def reject_withdraw_transaction(user_id: int, withdraw_id:int, session ): #Change status in WithdrawRequest table to rejected

    try:
        withdraw_order = await session.scalar(
            select(WithdrawalRequest)
            .where(withdraw_id == WithdrawalRequest.id)
            .with_for_update()
        )

        if not withdraw_order:
            raise HTTPException(status_code=400, detail='Withdraw order not found')

        if withdraw_order.status != WithdrawalStatus.PENDING:
            raise HTTPException(status_code=400, detail='Order already processed')
    
        user = await session.scalar(select(User).where(user_id == User.id).with_for_update())

        if not user:
            raise HTTPException(status_code=400, detail='Order not found')
        
        
        #moneyback 
        user.balance += Decimal(str(withdraw_order.amount))

        reject_bill = TransactionLog(
            user_id=user.id,
            amount=withdraw_order.amount,
            wallet_type=WalletType.WITHDRAW,
            action_type=ActionType.WITHDRAW_REJECTED
        )

        withdraw_order.status = WithdrawalStatus.REJECTED
        session.add(reject_bill)
        await session.commit()
        
    except HTTPException as http_exc:
        await session.rollback()
        raise http_exc

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f'Error {str(e)}')
    
# handel top up by admin, can select what wallet need to top up, ussual balance or stars_balance 
async def manual_balance_update(
    identifier: str | int, 
    amount: Decimal, 
    is_stars_balance: bool, 
    session
):
    try:
        # smart search
        if isinstance(identifier, int) or (isinstance(identifier, str) and identifier.isdigit()):
            user_query = select(User).where(User.id == int(identifier)).with_for_update()
        else:
            clean_username = str(identifier).replace('@', '')
            user_query = select(User).where(User.username.ilike(clean_username)).with_for_update()

        user = await session.scalar(user_query)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # top up on selected wallet
        if is_stars_balance:
            user.stars_balance += amount
        else:
            user.balance += amount

        # create log
        session.add(TransactionLog(
            user_id=user.id,
            amount=amount,
            wallet_type=WalletType.DEPOSITED if amount > 0 else WalletType.WITHDRAW,
            action_type=ActionType.ADMIN_TOPUP
        ))

        await session.commit()
        return {"message": "Balance updated successfully", "new_balance": user.stars_balance if is_stars_balance else user.balance}

    except HTTPException as http_exc:
        await session.rollback()
        raise http_exc
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

