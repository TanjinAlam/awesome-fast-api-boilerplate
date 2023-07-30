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
from core.exceptions import DatabaseTokenException
from app.database.schemas import DatabaseCredential
from core.utils.token_helper import TokenHelper


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





async def get_async_session(credentials: DatabaseCredential= Depends(TokenHelper.is_valid_database_token)) -> AsyncSession:
    db_url = f"postgresql+asyncpg://{credentials.user_name}:{credentials.password}@{credentials.host_name}:{credentials.port}/{credentials.database_name}"
   
    # Create the async engine for the specified database URL
    try:
        async_engine = create_async_engine(db_url)
    except Exception as e:
        raise DatabaseTokenException
    
    # Create the session factory
    sessionmaker_class = async_sessionmaker(async_engine)
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
        db = sessionmaker_class()
        try:
            yield db
        finally:
            await db.close()
    except Exception:
        raise DatabaseTokenException



# # Create a function to get the async session
# async def get_async_session(
#         credentials : DatabaseCredential
#     # user_name : str, password : str, host_name : str, database_name : str, port : str
# ) -> AsyncSession:
#     # Form the database URL based on the input parameters
#     db_url = f"postgresql+asyncpg://{credentials.user_name}:{credentials.password}@{credentials.host_name}:{credentials.port}/{credentials.database_name}"
   
#     # Create the async engine for the specified database URL
#     try:
#         async_engine = create_async_engine(db_url)
#     except Exception as e:
#         raise DatabaseTokenException
    
#     # Create the session factory
#     sessionmaker_class = async_sessionmaker(
#         async_engine
#     )
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

#         db = sessionmaker_class()
#         try:
#             yield db
#         finally:
#             await db.close()
