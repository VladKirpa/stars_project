from sqlalchemy import select
from app.models import Order, User, TransactionLog
from app.models.transaction_log import WalletType, ActionType
from app.config import SYSTEM_BANK_ID
from decimal import Decimal
from fastapi import HTTPException

async def cancel_order_by_admin(order_id: int, session):
    try:
        # block order
        order = await session.scalar(select(Order).where(Order.id == order_id).with_for_update())
        
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        if order.status != 'pending':
            raise HTTPException(status_code=400, detail=f"Cannot cancel order in status: {order.status}")

        # find unused budget
        remaining_subs = order.subs_quantity - order.current_subs
        if remaining_subs <= 0:
            raise HTTPException(status_code=400, detail="Order has no remaining subs to refund")
            
        refund_amount = Decimal(str(remaining_subs)) * order.reward_for_sub

        #cancel order
        order.status = 'canceled'

        # return money to customer
        user = await session.scalar(select(User).where(User.id == order.creator_id).with_for_update())
        if user:
            user.stars_balance += refund_amount
            session.add(TransactionLog(
                user_id=user.id,
                amount=refund_amount,
                wallet_type=WalletType.DEPOSITED,
                action_type=ActionType.ORDER_REFUND,
                order_id=order.id
            ))

        # take money from our sys bank
        system_bank = await session.scalar(select(User).where(User.id == SYSTEM_BANK_ID).with_for_update())
        if system_bank:
            system_bank.stars_balance -= refund_amount
            
        await session.commit()
        return {"message": "Order canceled, unused budget refunded", "refunded_amount": refund_amount}

    except HTTPException as http_exc:
        await session.rollback()
        raise http_exc
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")