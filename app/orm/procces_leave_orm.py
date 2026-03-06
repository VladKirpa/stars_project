from app.models import Order, Task, TaskCompletion, User
from app.models.transaction_log import WalletType, ActionType, TransactionLog
from app.models.task import CompletionStatus
from sqlalchemy import select
from app.config import SYSTEM_BANK_ID

# This block might check if somebody leave from channel 
# if somebody leave order that have status pending could open new place for enother sub
# user could have strike by sistem, 5 strikes = ban


async def process_user_leave(user_id: int, order_id: int, session):
    try:
        user = await session.scalar(
            select(User).where(User.tg_id == user_id).with_for_update()
        )
        if not user: return

        task_completion = await session.scalar(
            select(TaskCompletion)
            .join(Task, Task.id == TaskCompletion.task_id)
            .where(
                Task.order_id == order_id, 
                TaskCompletion.user_complete == user.id,
                TaskCompletion.status == CompletionStatus.FROZEN
            )
            .with_for_update()
        )

        if not task_completion:
            print(f"no frozen balance {user.id} in {order_id}")
            return

        user.strikes += 1
        print(f" User {user.id} got strike!")

        if user.strikes >= 5:
            user.is_banned = True

        task_completion.status = CompletionStatus.CANCELED
        
        system_bank = await session.scalar(
            select(User).where(User.id == SYSTEM_BANK_ID).with_for_update()
        )
        if system_bank:
            system_bank.balance += task_completion.stars_reward
            session.add(TransactionLog(
                user_id=SYSTEM_BANK_ID,
                amount=task_completion.stars_reward,
                wallet_type=WalletType.EARNED,
                action_type=ActionType.SYSTEM_REVENUE,
                order_id=order_id
            ))

        order = await session.scalar(
            select(Order).where(Order.id == order_id).with_for_update()
        )
        if order and order.current_subs > 0:
            order.current_subs -= 1
                    
        await session.commit()
        print(f"[SUCCESS] strike given.")
        
    except Exception as e:
        await session.rollback()
        print(f"Background Task Error: {repr(e)}")