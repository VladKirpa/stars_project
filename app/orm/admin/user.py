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



async def get_user_logs_paginated(identifier:str | int, session, 
                                  limit:int = 10, 
                                  offset:int = 0) -> list[TransactionLog]:
    try: 
        # smart search
        if isinstance(identifier, int) or (isinstance(identifier, str) and identifier.isdigit()):
            user_query = select(User.id).where(User.id == int(identifier))
        else:
            clean_username = str(identifier).replace('@', '')
            user_query = select(User.id).where(User.username.ilike(clean_username))

        user_id = await session.scalar(user_query)
        
        if not user_id:
            raise HTTPException(status_code=404, detail='User not found')

        # find logs from new to old 
        logs_query = (
            select(TransactionLog)
            .where(TransactionLog.user_id == user_id)
            .order_by(TransactionLog.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        
        result = await session.scalars(logs_query)
        return result.all()

    except HTTPException as http_exc: 
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error: {str(e)}')


async def ban_user(user_id:int, session):
    try:
        user = await session.scalar(select(User).where(User.id==user_id).with_for_update())

        if user:
            user.is_banned = True
            sys_bank = await session.scalar(select(User).where(User.id==SYSTEM_BANK_ID).with_for_update())
            sys_bank.balance += user.balance
            sys_bill = TransactionLog(
                user_id=SYSTEM_BANK_ID,
                amount=user.balance,
                wallet_type=WalletType.EARNED,
                action_type=ActionType.SYSTEM_REVENUE
            )
            user_bill = TransactionLog(
                user_id=user.id,
                amount=user.balance,
                wallet_type=WalletType.EARNED,
                action_type=ActionType.SYSTEM_REVENUE
            )
            user.balance = Decimal('0')

            session.add(sys_bill)
            session.add(user_bill)

            completed_tasks = await session.scalars(
                select(TaskCompletion)
                .where(TaskCompletion.user_complete==user_id, 
                       TaskCompletion.status == CompletionStatus.FROZEN))

            for task in completed_tasks.all():
                task.status = CompletionStatus.CANCELED
                sys_bank.balance += task.stars_reward
                bill = TransactionLog(
                    user_id=SYSTEM_BANK_ID,
                    amount=task.stars_reward,
                    wallet_type=WalletType.EARNED,
                    action_type=ActionType.SYSTEM_REVENUE
                )
                session.add(bill)
                order = await session.scalar(select(Order)
                    .join(Task, Order.id == Task.order_id)
                    .where(Task.id == task.task_id)
                    .with_for_update())
                if order and order.status == "pending":
                    order.current_subs -= 1

            withdraw_request = await session.scalar(
                select(WithdrawalRequest)
                .where(WithdrawalRequest.user_id == user_id,
                 WithdrawalRequest.status == WithdrawalStatus.PENDING)
                .with_for_update())
            
            if withdraw_request:
                withdraw_request.status = WithdrawalStatus.REJECTED 

            await session.commit()
                

            
        else:
            raise HTTPException(status_code=400, detail='User not found')
    
    
    except HTTPException as http_exc:
        await session.rollback()
        raise http_exc
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f'Error: {str(e)}')

    
    
async def unban_user(user_id:int, session):

    try:
        user = await session.scalar(select(User).where(User.id==user_id).with_for_update())

        if not user:
            raise HTTPException(status_code=400, detail='User not found')
        
        user.is_banned=False
        user.strikes = 0
        await session.commit()

    except HTTPException as http:
        await session.rollback()
        raise http
    except Exception as e:
        await session.rollback()
        

