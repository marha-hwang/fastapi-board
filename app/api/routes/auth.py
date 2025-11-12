from typing import Any
from fastapi import APIRouter
from pydantic import BaseModel
from app.schema.common import ApiRequest, ApiResponse
from app.schema.auth import LoginRequest, LoginResponse
from app.crud.auth import verify_user

router = APIRouter(tags=["인증"], prefix="/auth")

@router.post("/login", response_model=ApiResponse)
async def login(user_in: LoginRequest) -> Any:
    """
    login user.
    """
    print(user_in) # id='haram' pwd='1234qwer'

    result = await verify_user(user=user_in)
    if result == None : return ApiResponse(success=True, message="잘못된 로그인 정보입니다.")
    else :  return ApiResponse[LoginResponse](success=True, message="로그인에 성공하였습니다.", data=result) 


# @router.post("/logout", response_model=ApiResponse)
# async def logout(user_in: Request) -> Any:
#     """
#     login user.
#     """
#     print(user_in) # id='haram' pwd='1234qwer'

#     response = Response(success=True, message="로그아웃이 성공적으로 완료되었습니다.") 
#     # {
#     #     "resp_msg": "hello",
#     #     "resp_code": "200"
#     # }

#     return response
