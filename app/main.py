from fastapi import FastAPI
from .config import server_config
from fastapi import APIRouter
from app.routes import auth_router, user_router, post_router, comment_router
import logging


app = FastAPI(title="FastAPI + Poetry AI Server")

logging.basicConfig(
    level=logging.INFO,  # 로그 레벨을 INFO로 설정
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
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