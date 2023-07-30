from typing import Optional, List

from sqlalchemy import or_, select, and_

from app.user.models import User
from app.user.schemas.user import LoginResponseSchema
from core.db import Transactional, session
from core.exceptions import (
    PasswordDoesNotMatchException,
    DuplicateEmailOrNicknameException,
    UserNotFoundException,
)
from core.utils.token_helper import TokenHelper
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, Mapped, mapped_column

from core.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import  Depends
from sqlalchemy.sql import func, text
from app.user.models import User
class UserService:
    def __init__(self, db: Session):
        self.db = db

    async def get_user_list(
        self,
        limit: int = 12,
        prev: Optional[int] = None,
    ) -> List[User]:
        query = select(User)

        if prev:
            query = query.where(User.id < prev)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    # @Transactional()
    # async def create_user(
    #     self, email: str, password1: str, password2: str, nickname: str,
    #     # db: AsyncSession = Depends(get_db)
    # ) -> None:
    #     if password1 != password2:
    #         raise PasswordDoesNotMatchException

    #     query = select(User).where(or_(User.email == email, User.nickname == nickname))
    #     result = await session.execute(query)
    #     is_exist = result.scalars().first()
    #     if is_exist:
    #         raise DuplicateEmailOrNicknameException

    #     user = User(email=email, password=password1, nickname=nickname)
    #     session.add(user)

    # @Transactional()
    async def create(
    self, email: str, password1: str, password2: str, nickname: str,
    ) -> None:
        # print("SERVICE",password1, password2)
        if password1 != password2:
            raise PasswordDoesNotMatchException

        result = await self.db.execute(
            select(User).where(User.email == email))
        
        is_exist = result.scalars().first()

        # # statement = select(User).where(User.email == email)
        # # result = await self.db.execute(statement)

        # print("result...", result)
        # if(result):
        #     is_exist = result.scalars().one()



        # query = select(User).where(or_(User.email == email, User.nickname == nickname))
        # result = await self.db.execute(stmt).all()
        # is_exist = result.scalars().first()
        if is_exist:
            raise DuplicateEmailOrNicknameException

        user = User(email=email, password=password1, nickname=nickname)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

    async def is_admin(self, user_id: int) -> bool:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            return False

        if user.is_admin is False:
            return False

        return True

    async def login(self, email: str, password: str) -> LoginResponseSchema:

        result = await self.db.execute(
            select(User).where(and_(User.email == email, password == password))
        )
        user = result.scalars().first()

        if not user:
            raise UserNotFoundException

        response = LoginResponseSchema(
            token=TokenHelper.encode(payload={"user_id": user.id}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
        )
        return response
