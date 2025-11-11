from typing import Any
from fastapi import APIRouter
from app.schema.common import Request, Response
from app.schema.user import UserCreate, UserDelete, UserUpdate, UserPasswordChange
from app.crud.user import create_user

router = APIRouter(tags=["사용자"], prefix="/user")

@router.post("", response_model=Response)
async def create_user(user_in: UserCreate) -> Any:

    create_user(user_in=user_in)
    response = Response(success=True, message="회원가입이 성공적으로 완료되었습니다.") 

    return response

@router.delete("", response_model=Response)
async def delete_user(user_in: UserDelete) -> Any:

    response = Response(success=True, message="회원탈퇴가 성공적으로 완료되었습니다.") 

    return response

@router.put("", response_model=Response)
async def update_user(user_in: UserUpdate) -> Any:

    response = Response(success=True, message="회원정보 수정이 성공적으로 완료되었습니다.") 

    return response

@router.put("/password", response_model=Response)
async def update_password(user_in: UserPasswordChange) -> Any:

    response = Response(success=True, message="패스워드 변경이 성공적으로 완료되었습니다.") 

    return response