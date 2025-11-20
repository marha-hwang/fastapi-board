from fastapi import FastAPI, Request, status
from .config import server_config
from fastapi import APIRouter
from app.routes import auth_router, user_router, post_router, comment_router
import logging
from fastapi.exceptions import RequestValidationError
import app.schema.common_schema as common_schema
from fastapi.responses import JSONResponse
import app.core.exception as custom_exception

app = FastAPI(title="FastAPI + Poetry AI Server")

logging.basicConfig(
    level=logging.INFO,  # 로그 레벨을 INFO로 설정
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# 기본 에러처리
@app.exception_handler(Exception)
async def default_exception_handler(request: Request, exc: Exception):
    error_msg = str(exc)
    print(f"🚨 500 Internal Server Error: {error_msg}")

    response = common_schema.ApiResponse(success=False, 
                                         code=custom_exception.ErrorCode.INTERNAL_SERVER_ERROR, 
                                         message="서버 내부 오류가 발생했습니다.")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response.model_dump()
    )

# 요청데이터가 pydantic검증에 실패하는 경우
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    
    for error in exc.errors():
        msg = error["msg"].replace("Value error, ", "")

    response = common_schema.ApiResponse(success=False, 
                                         code=custom_exception.ErrorCode.INVALID_INPUT_VALUE, 
                                         message=msg)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=response.model_dump()
    )

# 로그인 정보가 올바르지 않은 경우
@app.exception_handler(custom_exception.AuthRequestException)
async def auth_exception_handler(request: Request, exc: custom_exception.AuthRequestException):

    response = common_schema.ApiResponse(success=False, 
                                         code=exc.code, 
                                         message=exc.message)
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=response.model_dump()
    )



@app.get("/")
async def root():
    return {"message": "AI Model Server is running 🚀"}

api_router = APIRouter()
api_router.include_router(router=auth_router.router)
api_router.include_router(router=user_router.router)
api_router.include_router(router=post_router.router)
api_router.include_router(router=comment_router.router)


app.include_router(api_router)