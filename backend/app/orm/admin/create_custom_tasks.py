from app.models import Order, Task, TaskCompletion, User
from app.models.transaction_log import WalletType, ActionType, TransactionLog
from sqlalchemy import select
from decimal import Decimal
from app.config import SYSTEM_BANK_ID
from fastapi import HTTPException

async def create_custom_admin_order(
    admin_tg_id: int, 
    channel_url: str, 
    subs_quantity: int, 
    custom_worker_pay: Decimal,
    description: str,
    session
):
    try:
        admin = await session.scalar(select(User).where(User.tg_id == admin_tg_id))
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found in database")
        
        admin_internal_id = admin.id

        # woker pay cannot be less than reward_for_sub
        if subs_quantity <= 0 or custom_worker_pay <= 0:
            raise HTTPException(status_code=400, detail="Values must be greater than zero")

        # add custom task cost to bank
        system_bank = await session.scalar(select(User).where(User.id == SYSTEM_BANK_ID).with_for_update())
        if not system_bank:
            raise HTTPException(status_code=500, detail="System bank not found")

        # count budget
        total_emission = Decimal(str(subs_quantity)) * custom_worker_pay
        
        # bank get money on own account
        # after complete_transaction could use that money to earn reward
        system_bank.stars_balance += total_emission 

        new_order = Order(
            creator_id=admin_internal_id,
            channel_id=channel_url,
            subs_quantity=subs_quantity,
            current_subs=0,
            worker_pay=custom_worker_pay,
            reward_for_sub=custom_worker_pay,
            status='pending',
            action_type='SUBSCRIBE_CHANNEL',
            description=description
        )
        session.add(new_order)
        await session.flush() # make flush to get order id

        # make log to avoid that when we will count revenue
        emission_bill = TransactionLog(
            user_id=SYSTEM_BANK_ID,
            amount=total_emission,
            wallet_type=WalletType.DEPOSITED, 
            action_type=ActionType.ADMIN_EMISSION,
            order_id=new_order.id
        )
        session.add(emission_bill)

        await session.commit()
        return {"message": "Custom order created", "order_id": new_order.id}

    except HTTPException as http_exc:
        await session.rollback()
        raise http_exc
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")