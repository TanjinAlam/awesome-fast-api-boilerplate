# from contextvars import ContextVar, Token
# from typing import Union

# from sqlalchemy.ext.asyncio import (
#     AsyncSession,
#     create_async_engine,
#     async_scoped_session,
# )
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, Session 
# from sqlalchemy.sql.expression import Update, Delete, Insert

# from core.config import config

# session_context: ContextVar[str] = ContextVar("session_context")


# def get_session_context() -> str:
#     return session_context.get()


# def set_session_context(session_id: str) -> Token:
#     return session_context.set(session_id)


# def reset_session_context(context: Token) -> None:
#     session_context.reset(context)


# engines = {
#     "writer": create_async_engine(config.WRITER_DB_URL, pool_recycle=3600),
#     "reader": create_async_engine(config.READER_DB_URL, pool_recycle=3600),
# }


# class RoutingSession(Session):
#     def get_bind(self, mapper=None, clause=None, **kw):
#         if self._flushing or isinstance(clause, (Update, Delete, Insert)):
#             return engines["writer"].sync_engine
#         else:
#             return engines["reader"].sync_engine


# async_session_factory = sessionmaker(
#     class_=AsyncSession,
#     sync_session_class=RoutingSession,
# )
# session: Union[AsyncSession, async_scoped_session] = async_scoped_session(
#     session_factory=async_session_factory,
#     scopefunc=get_session_context,
# )

# Base = declarative_base()

# async def get_db() -> AsyncSession:
#     async with engines.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     db = session()
#     try:
#         yield db
#     finally:
#         await db.close()

# Define your SQLAlchemy models here as subclasses of Base

from fastapi import FastAPI, Depends,HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import asyncio
from sqlalchemy_utils import database_exists
# SQLALCHEMY 
engine = create_async_engine("postgresql+asyncpg://manuel:jw8s0F4@localhost:5432/profile",pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()







class DatabaseHandler:
    def __init__(self, user_name : str, password : str, host_name : str, database : str, port : str):
        self.engine = create_async_engine(f"postgresql+asyncpg://{user_name}:{password}@{host_name}:{port}/{database}",pool_pre_ping=True)
        self.SessionLocal = async_sessionmaker(self.engine)
    # class Base(DeclarativeBase):
    #     pass
    async def get_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        db = self.SessionLocal()
        try:
            yield db
        finally:
            await db.close()



# Function to check if a database exists asynchronously
async def check_database_exists(db_url : str) -> bool:
    return await asyncio.to_thread(database_exists, db_url)



# Create a function to get the async session
async def get_async_session(
    user_name : str, password : str, host_name : str, database_name : str, port : str
) -> AsyncSession:
    # Verify the credentials, you can implement your own logic here
    # if user_name != "valid_username" or password != "valid_password" or database_name != "valid_database_name":
    #     raise HTTPException(status_code=401, detail="Invalid credentials")

    # Form the database URL based on the input parameters
    db_url = f"postgresql+asyncpg://{user_name}:{password}@{host_name}:{port}/{database_name}"
    # Create the async engine for the specified database URL
    is_database = await check_database_exists(db_url)
    if not is_database:
        raise 
    async_engine = create_async_engine(db_url)

    # Create the session factory
    sessionmaker_class = async_sessionmaker(
        async_engine
        #   class_=AsyncSession, expire_on_commit=False
    )
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        db = sessionmaker_class()
        try:
            yield db
        finally:
            await db.close()

    # # Create the async session
    # async with sessionmaker_class() as session:
    #     yield session
