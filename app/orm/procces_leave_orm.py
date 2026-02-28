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
        task_completion = await session.scalar(
            select(TaskCompletion)
            .join(Task, Task.id == TaskCompletion.task_id)
            .where(Task.order_id == order_id, TaskCompletion.user_complete == user_id)
            .with_for_update()
        )
        if not task_completion or task_completion.status == CompletionStatus.CANCELED:
            return 

        user = await session.scalar(select(User).where(User.id == user_id).with_for_update())
        if user:
            user.strikes += 1
            if user.strikes >= 5:
                user.is_banned = True

        if task_completion.status == CompletionStatus.FROZEN:
            task_completion.status = CompletionStatus.CANCELED

            #return money to bank
            system_bank = await session.scalar(select(User).where(User.id == SYSTEM_BANK_ID).with_for_update())
            if system_bank:
                system_bank.balance += task_completion.stars_reward
                session.add(TransactionLog(
                    user_id=SYSTEM_BANK_ID,
                    amount=task_completion.stars_reward,
                    wallet_type=WalletType.EARNED,
                    action_type=ActionType.SYSTEM_REVENUE,
                    order_id=order_id
                ))

            # return place in order for new sub
            order = await session.scalar(select(Order).where(Order.id == order_id).with_for_update())
            if order and order.status == "pending":
                order.current_subs -= 1
                    
        await session.commit()
        
        return {"status": "success", "message": f"User {user_id} leave processed"}

    except Exception as e:
        await session.rollback()
        print(f"Background Task Error (process_user_leave): {repr(e)}")