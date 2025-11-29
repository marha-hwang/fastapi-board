from fastapi import FastAPI, Request, status
from .config import server_config
from fastapi import APIRouter
from app.routes import auth_router, user_router, post_router, comment_router, file_router
import logging
from fastapi.exceptions import RequestValidationError
import app.schema.common_schema as common_schema
from fastapi.responses import JSONResponse
from app.core.exception import CustomException, ErrorCode
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import AsyncOpenAI

app = FastAPI(title="FastAPI + Poetry AI Server")

logging.basicConfig(
    level=logging.INFO,  # 로그 레벨을 INFO로 설정
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


# 1. 실제 이미지가 저장된 폴더 이름
UPLOAD_DIR = "images"
# (폴더가 없으면 에러나니까 안전하게 생성)
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
# 2. mount 설정 (핵심 코드)
app.mount("/images", StaticFiles(directory=UPLOAD_DIR), name="images")

# 기본 에러처리
@app.exception_handler(Exception)
async def default_exception_handler(request: Request, exc: Exception):
    error_msg = str(exc)
    print(f"🚨 500 Internal Server Error: {error_msg}")

    response = common_schema.ApiResponse(success=False, 
                                         code=ErrorCode.INTERNAL_SERVER_ERROR, 
                                         message="서버 내부 오류가 발생했습니다.")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response.model_dump()
    )

# 요청데이터가 pydantic검증에 실패하는 경우
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(str(exc.errors))
    error_msg = str(exc)
    print(f" Error: {error_msg}")
    for error in exc.errors():
        msg = error["msg"].replace("Value error, ", "")

    response = common_schema.ApiResponse(success=False, 
                                         code=ErrorCode.INVALID_INPUT_VALUE, 
                                         message=msg)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=response.model_dump()
    )

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    error_msg = str(exc)
    print(f" Error: {error_msg}")
    response = common_schema.ApiResponse(success=False, 
                                         code=exc.code, 
                                         message=exc.message)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=response.model_dump()
    )

@app.get("/")
async def root():
    return {"message": "AI Model Server is running 🚀"}

################################### llm모델 api ###################################
# 1. vLLM 서버 연결 설정
public_url = "https://unresumed-maya-hyperaccurately.ngrok-free.dev"
model_name = "Qwen/Qwen2.5-32B-Instruct-AWQ"

VLLM_API_URL = f"{public_url}/v1" 
client = AsyncOpenAI(base_url=VLLM_API_URL, api_key="EMPTY")

class ChatRequest(BaseModel):
    message: str = "애국가 가사를 알려줘"
    model: str = model_name

# 2. 스트림 제너레이터 함수 (핵심)
async def stream_generator(prompt: str, model: str):
    # vLLM에 요청 (stream=True 필수!)
    stream = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,  # <--- 이게 켜져 있어야 vLLM이 한 글자씩 줍니다.
        temperature=0.7
    )

    # vLLM에서 오는 조각(chunk)을 받자마자 yield로 던짐
    async for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            # 그대로 텍스트만 보낼 수도 있고, SSE 포맷으로 보낼 수도 있음
            yield content 

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    # 3. StreamingResponse로 감싸서 반환
    return StreamingResponse(
        stream_generator(request.message, request.model),
        media_type="text/event-stream"  # 스트리밍 표준 MIME 타입
    )

######################################################################



api_router = APIRouter()
api_router.include_router(router=auth_router.router)
api_router.include_router(router=user_router.router)
api_router.include_router(router=post_router.router)
api_router.include_router(router=comment_router.router)
api_router.include_router(router=file_router.router)

app.include_router(api_router)