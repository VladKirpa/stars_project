import asyncio
from sqlalchemy import select, func
from celery import Celery
from app.config import settings
from app.database import async_session_factory, async_engine
from app.models import User, TaskCompletion, TransactionLog
from app.models.task import CompletionStatus
from app.models.transaction_log import WalletType, ActionType
from app.models.task import Task 

celery_app = Celery(
    "stars_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.beat_schedule = {
    'unlock-frozen-funds-every-minute': {
        'task': 'app.celery_app.unlock_funds_task',
        'schedule': 60.0,
    },
}

async def async_unlock_frozen_funds():
    async with async_session_factory() as session:
        try:
            query = select(TaskCompletion).where(
                TaskCompletion.status == CompletionStatus.FROZEN,
                TaskCompletion.unlock_date <= func.now()
            ).with_for_update()
            
            result = await session.scalars(query)
            frozen_tasks = result.all()

            if not frozen_tasks:
                return "No funds to unlock yet"

            unlocked_count = 0
            for completion in frozen_tasks:

                task_info = await session.get(Task, completion.task_id)
                if not task_info:
                    continue

                completion.status = CompletionStatus.COMPLETED
                
                user = await session.get(User, completion.user_complete, with_for_update=True)
                if user:
                    user.balance += completion.stars_reward
                    
                    session.add(TransactionLog(
                        user_id=user.id,
                        amount=completion.stars_reward,
                        wallet_type=WalletType.EARNED,
                        action_type=ActionType.TASK_PAYMENT,
                        order_id=task_info.order_id
                    ))
                    unlocked_count += 1

            await session.commit()
            print(f"DEBUG: Unlocked {unlocked_count} tasks")
            return f"Unlocked funds for {unlocked_count} tasks."

        except Exception as e:
            await session.rollback()
            print(f"CELERY CRITICAL ERROR: {str(e)}")
            return f"Error: {e}"
        
        finally:
            await async_engine.dispose()

@celery_app.task
def unlock_funds_task():
    return asyncio.run(async_unlock_frozen_funds())