from app.models import Order, Task, TaskCompletion, User
from app.models.transaction_log import WalletType, ActionType, TransactionLog
from app.models.task import CompletionStatus
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from app.config import SYSTEM_BANK_ID
from fastapi import HTTPException
from aiogram.exceptions import TelegramBadRequest
from tg_bot.run_bot import bot


async def find_available_task(internal_user_id: int, session) -> list[Task]:
    query = (
        select(Task)
        .join(Order)
        .outerjoin(
            TaskCompletion,
            and_(
                TaskCompletion.task_id == Task.id,
                TaskCompletion.user_complete == internal_user_id
            )
        )
        .where(
            TaskCompletion.id.is_(None),
            Order.status == 'pending'
        )
        .options(selectinload(Task.order))
    )
    
    result = await session.execute(query)
    return result.scalars().all()
    


async def complete_task_transaction(user_id: int, task_id: int, session):
    try: 
        # find worker by tg_id
        worker = await session.scalar(
            select(User).where(User.tg_id == user_id).with_for_update()
        )
        if not worker:
            raise HTTPException(status_code=400, detail='User not found')

        is_complete = await session.scalar(select(TaskCompletion).where(
            TaskCompletion.user_complete == worker.id, 
            TaskCompletion.task_id == task_id
        ))
        if is_complete:
            raise HTTPException(status_code=400, detail='Already done')
        
        #get  & block order
        order = await session.scalar(select(Order)
            .join(Task, Order.id == Task.order_id)
            .where(Task.id == task_id)
            .with_for_update()
        ) 
        if not order or order.status != 'pending':
            raise HTTPException(400, detail='Order unavailable')

        raw_target = str(order.channel_id).strip()
        
        if raw_target.startswith("-100"):
            chat_identifier = int(raw_target)
        else:
            clean_name = raw_target.replace("https://", "").replace("http://", "").replace("t.me/", "").replace("@", "").split("/")[0]
            chat_identifier = f"@{clean_name}"

        try:
            chat_member = await bot.get_chat_member(chat_id=chat_identifier, user_id=worker.tg_id)
            
            if chat_member.status in ['left', 'kicked', 'banned']:
                raise HTTPException(status_code=400, detail='You are not subscribed!')
                
        except Exception as e:
            print(f"DEBUG: Chat ID tried: {chat_identifier}")
            print(f"Telegram API Error: {e}")
            raise HTTPException(status_code=400, detail='Make @StarvsTakeBot as admin in channel')

        order.current_subs += 1
        if order.current_subs >= order.subs_quantity:
            order.status = 'completed'
        
        session.add(TaskCompletion(
            user_complete=worker.id,
            task_id=task_id,
            stars_reward=order.worker_pay,
            status=CompletionStatus.FROZEN
        ))
        
        system_bank = await session.scalar(select(User).where(User.id == SYSTEM_BANK_ID).with_for_update())
        if system_bank:
            system_bank.stars_balance -= order.reward_for_sub
        
        await session.commit()
        return {'message': 'Success'}

    except HTTPException as http_exc:
        await session.rollback()
        raise http_exc
    except Exception as e:
        await session.rollback()
        print(f'Critical: {repr(e)}')
        raise HTTPException(status_code=500, detail='Internal error')