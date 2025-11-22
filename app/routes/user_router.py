from typing import Any
from fastapi import APIRouter
from app.core.security import get_current_user
import app.schema.common_schema as common_schema
import app.schema.user_schema as user_schema
import app.service.user_service as user_service
import app.config as config
from app.repository.base_user_repository import BaseUserRepository
from app.repository.db.db_user_repository import UserRepositoryDB
from app.repository.csv.csv_user_repository import UserRepositoryCSV

from fastapi import Depends
from app.core.database import get_db
from sqlalchemy.orm import Session

def get_user_repository(db:Session = Depends(get_db)):
    if config.db_type == "database" :
        return UserRepositoryDB(db)
    else:
        return UserRepositoryCSV()


router = APIRouter(tags=["사용자"], prefix="/user")

@router.post("", response_model=common_schema.ApiResponse)
async def create_user(request: user_schema.UserCreate, repo:BaseUserRepository = Depends(get_user_repository)) -> Any:

    user_service.create_user(repo, request)
    response = common_schema.ApiResponse(success=True, message="회원가입이 성공적으로 완료되었습니다.") 

    return response

@router.delete("", response_model=common_schema.ApiResponse)
async def remove_user(current_user: str = Depends(get_current_user), repo:BaseUserRepository = Depends(get_user_repository)) -> Any:

    user_service.remove_user(repo, current_user)
    response = common_schema.ApiResponse(success=True, message="회원 삭제가 성공적으로 완료되었습니다.") 

    return response

@router.put("", response_model=common_schema.ApiResponse)
async def update_user(request: user_schema.UserUpdate, current_user: str = Depends(get_current_user), repo:BaseUserRepository = Depends(get_user_repository)) -> Any:

    user_service.update_user(repo, request, current_user)
    response = common_schema.ApiResponse(success=True, message="회원 업데이트가 성공적으로 완료되었습니다.") 

    return response

@router.put("/password", response_model=common_schema.ApiResponse)
async def update_password(request: user_schema.UserPasswordChange, current_user: str = Depends(get_current_user), repo:BaseUserRepository = Depends(get_user_repository)) -> Any:

    user_service.update_password(repo, request, current_user)
    response = common_schema.ApiResponse(success=True, message="비밀번호 업데이트가 성공적으로 완료되었습니다.") 

    return response