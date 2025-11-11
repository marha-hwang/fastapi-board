from fastapi import APIRouter

# from app.api.routes import items, login, private, users, utils
from app.api.routes import auth,user

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(user.router)
# api_router.include_router(utils.router)
# api_router.include_router(items.router)


# if settings.ENVIRONMENT == "local":
#     api_router.include_router(private.router)
