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
    EARNED='earned'
    DEPOSITED='deposited'


class ActionType(enum.Enum):
    DEPOSIT='deposit'
    ORDER_CREATION='order_creation'
    TASK_PAYMENT='task_payment'
    SYSTEM_REVENUE='system_revenue'
    WITHDRAWAL='withdrawal'


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



