from app.models import Order, Task, TaskCompletion, User
from app.models.transaction_log import WalletType, ActionType, TransactionLog
from app.models.task import CompletionStatus
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from app.config import SYSTEM_BANK_ID
from fastapi import HTTPException


async def find_available_task(user_id: int, session) -> list[Task]:
    # Select all tasks with antijoin where TaskCompletions is None to find available tasks for user
    query = (
            select(Task)
            .join(Order)
            .outerjoin(
                TaskCompletion,
                and_(
                    TaskCompletion.user_complete==user_id,
                    TaskCompletion.task_id==Task.id
                )
            )
            .where(
                TaskCompletion.id.is_(None),
                Order.status == 'pending'
            ).options(
                (selectinload(Task.order))
            )
        )
    
    result = await session.execute(query)
    return result.scalars().all()

    


async def complete_task_transaction(user_id: int, task_id: int, session):
    try: 
        is_complete = await session.scalar(select(TaskCompletion).where(
            TaskCompletion.user_complete==user_id,
            TaskCompletion.task_id==task_id
        ))      # block repeated execution

        if is_complete:
            raise HTTPException(status_code=400, detail='Task already done')
        
        #block order and check limits
        order = await session.scalar(select(Order)
        .join(Task, Order.id == Task.order_id)
        .where(Task.id == task_id)
        .with_for_update()
        ) 

        if not order or order.status != 'pending':      # check order status
            raise HTTPException(400, detail='Order not available')
        
        if order.current_subs >= order.subs_quantity:
            raise HTTPException(status_code=400, detail='Task limit reached')
        
        order.current_subs +=1
        if order.current_subs >= order.subs_quantity:
            order.status = 'completed'
        
        #Transaction 

        session.add(TaskCompletion(
            user_complete=user_id,
            task_id=task_id,
            stars_reward=order.worker_pay,
            status=CompletionStatus.FROZEN
        ))
        worker = await session.scalar(select(User).where(User.id == user_id).with_for_update()) # block race conditional for user
        
        if not worker:
            raise HTTPException(status_code=400, detail='User do not exists')
        
        system_bank = await session.scalar(select(User).where(User.id == SYSTEM_BANK_ID).with_for_update()) #  <--- system bank id (change in config) & block race conditional
    
        if not system_bank: 
            raise HTTPException(status_code=400, detail='Bank account not defined')

        system_bank.stars_balance -= order.reward_for_sub                # write off full price from Escrow

        #save bill for SYSTEM_BANK
        sys_bank_bill = TransactionLog(
            user_id=SYSTEM_BANK_ID,
            amount=order.reward_for_sub,
            wallet_type=WalletType.DEPOSITED,
            action_type=ActionType.TASK_PAYMENT,
            order_id=order.id
        )
        session.add(sys_bank_bill)

        system_bank.balance += order.reward_for_sub - order.worker_pay   # count service margin and put it to bank balance
        
        #save service revenue bill

        service_revenue_bill = TransactionLog(
            user_id=SYSTEM_BANK_ID,
            amount=order.reward_for_sub - order.worker_pay,
            wallet_type=WalletType.EARNED,
            action_type=ActionType.SYSTEM_REVENUE,
            order_id=order.id
        )
        session.add(service_revenue_bill)
        
        await session.commit()
        return {'message': 'Task compete successful'}

    except HTTPException as http_exc:
        await session.rollback()
        raise http_exc

    except Exception as e:
        await session.rollback()
        print(f'Critical error: {repr(e)}')
        raise HTTPException(status_code=500, detail='Something went wrong')
        
