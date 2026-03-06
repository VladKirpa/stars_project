import datetime
import enum
from sqlalchemy import (
    DECIMAL, BIGINT, ForeignKey, VARCHAR, TIMESTAMP, UniqueConstraint, func,
    Enum as SQLEnum
    )
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal # Decimal for Mapped
from app.database import bigint_pk


class WalletType(enum.Enum):
    EARNED='EARNED'
    DEPOSITED='DEPOSITED'
    WITHDRAW='WITHDRAW'



class ActionType(enum.Enum):
    DEPOSIT='DEPOSIT'
    ORDER_CREATION='ORDER_CREATION'
    ORDER_REFUND='ORDER_REFUND'

    TASK_PAYMENT='TASK_PAYMENT'
    SYSTEM_REVENUE='SYSTEM_REVENUE'
    WITHDRAWAL='WITHDRAWAL'
    ADMIN_EMISSION='ADMIN_EMISSION'
    ADMIN_TOPUP='admin_topup'

    WITHDRAW_APPROVED='WITHDRAW_APPROVED'
    WITHDRAW_REJECTED='WITHDRAW_REJECTED'


class TransactionLog(Base):
    __tablename__='transactions_log'

    id: Mapped[bigint_pk]
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.id'))
    amount: Mapped[Decimal] = mapped_column(DECIMAL)
    wallet_type: Mapped[WalletType] = mapped_column(SQLEnum(WalletType))
    action_type: Mapped[ActionType] = mapped_column(SQLEnum(ActionType))
    order_id: Mapped[int | None] = mapped_column(BIGINT, ForeignKey('orders.id'), nullable=True) 
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow,
                                                        server_default=func.now(), nullable=False)



