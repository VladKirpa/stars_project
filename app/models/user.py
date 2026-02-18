import datetime
from sqlalchemy import (
    DECIMAL, BIGINT, ForeignKey,
    )
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal # Decimal for Mapped
from app.database import bigint_pk



## TABLES 

class User(Base):
    __tablename__ = 'users'

    id: Mapped[bigint_pk] 
    tg_id: Mapped[int] = mapped_column(BIGINT,nullable=False,unique=True)
    username: Mapped[str | None]
    referral_id: Mapped[int | None] = mapped_column(BIGINT, ForeignKey('users.tg_id'), default=None)
    balance: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), default=0)
    stars_balance: Mapped[Decimal] = mapped_column(DECIMAL(12,2), default=0)






# class Tasks(Base):
#     __tablename__ ='tasks'

#     id: Mapped[int_primary_key]
#     title: Mapped[str] = mapped_column(String(30), nullable=False)
#     description: Mapped[str | None] = mapped_column(String(60), nullable=True)
#     reward: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), nullable=False)
#     url: Mapped[str] = mapped_column(String(100))
#     is_active: Mapped[bool] = mapped_column(BOOLEAN, default=True)


# class AdOrder(Base):
#     __tablename__ = 'AdOrder'

#     id: Mapped[int_primary_key]
#     creator_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.id'))
#     channel_link: Mapped[str] = mapped_column(VARCHAR(250))
#     total_subs: Mapped[int] = mapped_column(INTEGER) 
#     current_subs: Mapped[int] = mapped_column(INTEGER)
#     cost: Mapped[int] = mapped_column(DECIMAL(12, 2))


# class TaskCompletion(Base):
#     __tablename__ = 'TaskCompletion'
    
#     id: Mapped[int_primary_key]
#     user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.id'))
#     task_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('Tasks.id'))
#     status: Mapped[bool] = mapped_column(BOOLEAN)
#     created_at: Mapped[str] = mapped_column(DATETIME)


# class Withdrawal(Base):
#     id: Mapped[int_primary_key]
#     user_id: Mapped[int] = mapped_column()