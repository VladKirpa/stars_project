from sqlalchemy import select, func
from app.models import User, TaskCompletion, TransactionLog, WithdrawalRequest
from app.models.task import CompletionStatus
from app.models.transaction_log import ActionType
from app.models.withdrawal_request import WithdrawalStatus
from app.config import SYSTEM_BANK_ID
from decimal import Decimal

async def get_global_financial_stats(session) -> dict:

    # all users money in BALANCE = user can withdraw that money
    user_bal_query = select(func.coalesce(func.sum(User.balance), Decimal('0'))).where(User.id != SYSTEM_BANK_ID)
    total_user_balances = await session.scalar(user_bal_query)

    # Hold money
    frozen_query = select(func.coalesce(func.sum(TaskCompletion.stars_reward), Decimal('0'))).where(
        TaskCompletion.status == CompletionStatus.FROZEN)
    total_frozen_funds = await session.scalar(frozen_query)

    # clear revenue
    revenue_query = select(func.coalesce(func.sum(TransactionLog.amount), Decimal('0'))).where(
        TransactionLog.action_type == ActionType.SYSTEM_REVENUE)
    total_system_revenue = await session.scalar(revenue_query)

    # Amdin emission (when create custom tasks)
    emission_query = select(func.coalesce(func.sum(TransactionLog.amount), Decimal('0'))).where(
        TransactionLog.action_type == ActionType.ADMIN_EMISSION)
    admin_emission_debt = await session.scalar(emission_query)

    # Money earned by users for all time 
    withdrawn_query = select(func.coalesce(func.sum(WithdrawalRequest.amount), Decimal('0'))).where(
        WithdrawalRequest.status == WithdrawalStatus.APPROVED)
    total_withdrawn = await session.scalar(withdrawn_query)

    return {
        "total_user_balances": float(total_user_balances or 0),
        "total_frozen_funds": float(total_frozen_funds or 0 ),
        "total_system_revenue": float(total_system_revenue or 0),
        "admin_emission_debt": float(admin_emission_debt or 0),
        "total_withdrawn": float(total_withdrawn or 0 )
    }

