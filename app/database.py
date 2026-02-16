import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker 
from sqlalchemy import URL, create_engine, text
from config import settings


# async engine

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
    max_overflow=10,
    hide_parameters=True
) 


async def get_start():
    async with async_engine.connect() as conn:
        res = await conn.execute(text('SELECT 123'))
        print(f'REsult from db {res.all()}')


asyncio.run(get_start())