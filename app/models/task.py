import datetime
from sqlalchemy import (
    DECIMAL, BIGINT, ForeignKey, VARCHAR, TIMESTAMP, UniqueConstraint
    )
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal # Decimal for Mapped
from app.database import bigint_pk



class Task(Base):
    __tablename__ = 'tasks'


    #Relationship
    order: Mapped['Order'] = relationship(back_populates='tasks')
    completions: Mapped[list['TaskCompletion']] = relationship(back_populates='task')

    id: Mapped[bigint_pk] #Generated alwyas as identity
    order_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('orders.id'), nullable=False)


class TaskCompletion(Base):
    __tablename__ = 'task_completions'
    __table_args__ = (UniqueConstraint('task_id', 'user_complete', name='idx_uniq_user_task'),)

    #Relationship
    task:Mapped['Task'] = relationship(back_populates='completions')

    id: Mapped[bigint_pk]
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'))
    user_complete: Mapped[int] = mapped_column(ForeignKey('users.id'))
    completed_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP)
    

