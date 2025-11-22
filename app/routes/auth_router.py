from typing import Any
from fastapi import APIRouter
import app.schema.common_schema as common_schema
import app.schema.auth_schema as auth_schema
import app.service.auth_service as auth_service
import logging
from app.core.exception import ErrorCode, CustomException

from app.repository.base_user_repository import BaseUserRepository
from app.repository.db.db_user_repository import UserRepositoryDB
from app.repository.csv.csv_user_repository import UserRepositoryCSV

from fastapi import Depends
from app.core.database import get_db
from sqlalchemy.orm import Session
import app.config as config

def get_user_repository(db:Session = Depends(get_db)):
    if config.db_type == "database" :
        return UserRepositoryDB(db)
    else:
        return UserRepositoryCSV()

logger = logging.getLogger(__name__)

router = APIRouter(tags=["인증"], prefix="/auth")

@router.post("/login", response_model=common_schema.ApiResponse)
async def login(request: auth_schema.Login, repo:BaseUserRepository = Depends(get_user_repository)) -> Any:

    # 유저검증하여 토큰, 유저정보 반환
    user, token = auth_service.veryfy_user(repo, request)

    login_response = auth_schema.LoginResponse(access_token=token, token_type="bearer", user=user)
    response = common_schema.ApiResponse[auth_schema.LoginResponse](success=True, message="로그인에 성공하였습니다.", data=login_response) 
    return response