from app.models import Order, Task, TaskCompletion, User
from app.models.withdrawal_request import WithdrawalRequest , WithdrawalStatus
from app.models.transaction_log import WalletType, ActionType, TransactionLog
from app.models.task import CompletionStatus
from sqlalchemy import select, update, delete, func, join, insert, and_, outerjoin
from sqlalchemy.orm import selectinload
from app.schemas.order import OrderCreate, OrderRead
from typing import List
import asyncio
from decimal import Decimal
from app.config import MIN_WITHDRAWAL
from fastapi import HTTPException

async def create_withdrawal_request(user_id:int, amount:int, session):
    try:
        if not isinstance(amount, int):
            raise HTTPException(status_code=400, detail='Amount can be only integer')

        user = await session.scalar(
            select(User)
            .where(User.id == user_id)
            .with_for_update())
        
        if not user:
            raise HTTPException(status_code=400, detail='User not found')
        
        if not user.username:
            raise HTTPException(status_code=400, detail='Set up @username to withdraw balance')
        
        if user.balance >= Decimal(str(amount)) and amount >= MIN_WITHDRAWAL:
    
            user.balance -= Decimal(str(amount))
            new_withdraw = WithdrawalRequest(
                user_id = user.id,
                amount=amount,
                username=user.username,
                status=WithdrawalStatus.PENDING
            )
            new_bill = TransactionLog(
                user_id=user.id,
                amount=amount,
                wallet_type=WalletType.EARNED,
                action_type=ActionType.WITHDRAWAL,
            )   
        
            session.add(new_withdraw)
            session.add(new_bill)
            await session.commit()
        else:
            raise HTTPException(status_code=400, detail='Not enough balance or amount less than minimal withdraw sum')
    
    except HTTPException as http_exc:
        await session.rollback()
        raise http_exc
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail='Something went wrong')
    
    