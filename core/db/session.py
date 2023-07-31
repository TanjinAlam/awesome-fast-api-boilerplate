from fastapi import Depends
from sqlalchemy.orm import DeclarativeBase
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

