# api文件只管路由！！

# 写这里自动引入了

from fastapi import APIRouter
from app.api.auth import router as auth_router
from app.api.user import router as user_router

api = APIRouter()
api.include_router(auth_router)
api.include_router(user_router)
