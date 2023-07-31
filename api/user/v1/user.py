from typing import List

from fastapi import APIRouter, Depends, Query
from core.db import get_db, get_async_session
from api.user.v1.request.user import LoginRequest
from api.user.v1.response.user import LoginResponse
from app.user.schemas import (
    ExceptionResponseSchema,
    GetUserListResponseSchema,
    CreateUserRequestSchema,
    CreateUserResponseSchema,
)
from app.user.services import UserService
from core.fastapi.dependencies import (
    PermissionDependency,
    IsAdmin,
)
from typing import Optional, Union
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, select

from fastapi.security import HTTPAuthorizationCredentials
from core.utils.token_helper import TokenHelper
from app.user.models import User
from app.database.schemas import DatabaseCredential

user_router = APIRouter()




@user_router.post('/test-token')
async def dummy_token(
    cred :DatabaseCredential
    ):
    return TokenHelper.encode(payload=cred.dict())

@user_router.post('/test-user')
async def dummy_user(
    cred :DatabaseCredential
    ):
    return TokenHelper.encode(payload=cred.dict())

@user_router.get('/test-all-user')
async def all_user(db : HTTPAuthorizationCredentials = Depends(get_async_session)):
    all_users= await UserService(db).get_user_list(limit=2, prev=0)
    return all_users



@user_router.get(
    "",
    # response_model=List[GetUserListResponseSchema],
    # response_model_exclude={"id"},
    # responses={"400": {"model": ExceptionResponseSchema}},
    # dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def get_user_list(
    limit: int = Query(10, description="Limit"),
    prev: int = Query(None, description="Prev ID"),
    db: AsyncSession = Depends(get_db),
    # token: HTTPAuthorizationCredentials = Depends(TokenHelper.is_valid_token),
):
    return await UserService(db).get_user_list(limit=limit, prev=prev)




@user_router.post(
    "",
    response_model=CreateUserResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def create_user(request: CreateUserRequestSchema, db: AsyncSession = Depends(get_db)):

    # statement = select(User).where(User.email == request.email)

    # result = await db.execute(statement)

    # user = result.scalars().one()

    # print(user.email)
    # # results = await db.execute(select(User)).filter(User.email == request.email).first()
    # # users = results.__dict__
    # # user_data = [{key: value for key, value in user.__dict__.items() if not key.startswith('_')} for user in users]
    # print("user_data:", user.__dict__)

    # user_data = [user.__dict__() for user in is_exist]
    # print("user_data:", user_data)
    email = request.email
    password1 = request.password1
    password2 = request.password2
    nickname = request.nickname
    
    await UserService(db).create(email, password1, password2, nickname)

    return {"email": request.email, "nickname": request.nickname}



@user_router.post(
    "/login",
    # response_model=LoginResponse,
    responses={"404": {"model": ExceptionResponseSchema}},
)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    token = await UserService(db).login(email=request.email, password=request.password)
    return {"token": token.token, "refresh_token": token.refresh_token}
