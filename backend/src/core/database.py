from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import create_db_url


DATABASE_URL = create_db_url()

async_engine = create_async_engine(DATABASE_URL, echo=True)

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    Session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with Session() as session:
        yield session