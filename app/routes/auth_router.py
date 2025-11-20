from typing import Any
from fastapi import APIRouter
import app.schema.common_schema as common_schema
import app.schema.auth_schema as auth_schema
import app.service.auth_service as auth_service
import logging
import app.core.exception as exception


logger = logging.getLogger(__name__)

router = APIRouter(tags=["인증"], prefix="/auth")

@router.post("/login", response_model=common_schema.ApiResponse)
async def login(request: auth_schema.Login) -> Any:

    # 유저검증하여 토큰, 유저정보 반환
    result = auth_service.veryfy_user(input=request)
    if result == None : raise exception.AuthRequestException(code=exception.ErrorCode.NOT_AUTHENTICATED, message="로그인 정보가 올바르지 않습니다.")
    
    user, token = result
    logger.info(f"{user.__dict__}, {token}")
    login_response = auth_schema.LoginResponse(access_token=token, token_type="bearer", user=user)
    
    response = common_schema.ApiResponse[auth_schema.LoginResponse](success=True, message="로그인에 성공하였습니다.", data=login_response) 
    return response