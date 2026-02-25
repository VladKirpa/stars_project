from app.models import Order, Task, TaskCompletion, User,
from app.models.pending_payments import PaymentStatus, PendingPayment
from app.models.transaction_log import WalletType, ActionType, TransactionLog
from sqlalchemy import select, update, delete, func, join, insert, and_, outerjoin
from sqlalchemy.orm import selectinload
from app.schemas.order import OrderCreate, OrderRead
from typing import List
import asyncio
from decimal import Decimal
from app.config import SYSTEM_BANK_ID, STARS_TO_USDT
from fastapi import HTTPException



async def confirm_payment(external_id:str, session) -> dict:
    try:
        payment = await session.scalar(
            select(PendingPayment)
            .where(PendingPayment.external_id == external_id)
            .with_for_update())
        
        if not payment or payment.status == PaymentStatus.PAID:
            raise HTTPException(status_code=400, detail='Order has been already paid')
        
        #find user who payied
        user = await session.scalar(
            select(User)
            .where(User.id == payment.user_id)
            .with_for_update()
        )

        if not user:
            raise HTTPException(status_code=400, detail='User not found')
        
        user.stars_balance += payment.amount_stars

        #write on user top up
        user_topup_bill = TransactionLog(
                            user_id=payment.user_id,
                            amount=payment.amount_stars,
                            wallet_type=WalletType.DEPOSITED,
                            action_type=ActionType.DEPOSIT
                        )
        session.add(user_topup_bill)    

        payment.status = PaymentStatus.PAID
        await session.commit()
    
    except HTTPException as http_exc:
        await session.rollback()
        raise http_exc
    
    except Exception as e: 
        await session.rollback()
        print(f'Error {e}')
        raise HTTPException(status_code=500, detail='Something went wrong')
    
