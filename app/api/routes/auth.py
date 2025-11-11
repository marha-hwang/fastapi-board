from typing import Any
from fastapi import APIRouter
from pydantic import BaseModel
from app.schema.common import Request, Response

class LoginRequest(BaseModel):
    user_id:str
    password:str
    nickname:str
    img_id:str

router = APIRouter(tags=["인증"], prefix="/auth")

@router.post("/login", response_model=Response)
async def login(user_in: LoginRequest) -> Any:
    """
    login user.
    """
    print(user_in) # id='haram' pwd='1234qwer'

    response = Response(success=True, message="로그인이 성공적으로 완료되었습니다.") 
    # {
    #     "resp_msg": "hello",
    #     "resp_code": "200"
    # }

    return response

@router.post("/logout", response_model=Response)
async def logout(user_in: Request) -> Any:
    """
    login user.
    """
    print(user_in) # id='haram' pwd='1234qwer'

    response = Response(success=True, message="로그아웃이 성공적으로 완료되었습니다.") 
    # {
    #     "resp_msg": "hello",
    #     "resp_code": "200"
    # }

    return response
