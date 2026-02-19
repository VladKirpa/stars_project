import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase, mapped_column
from sqlalchemy import URL, create_engine, text
from app.config import settings
from typing import Annotated
from sqlalchemy import BIGINT, Identity

# async engine

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
    max_overflow=10,
    hide_parameters=True
) 

async_session_factory = async_sessionmaker(
        async_engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False
    )


class Base(DeclarativeBase):
    pass
 

async def get_db():    # DRY func for api
    async with async_session_factory() as session:
        yield session
    

#Short models 
bigint_pk = Annotated[int, mapped_column(BIGINT, Identity(always=True),primary_key=True)]



