from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router

# 导入 User 是为了告诉程序我有这个表，记得去创建
from app.models.user import User
from app.database import Base,engine
Base.metadata.create_all(bind=engine) # 自动创建表
# app.add_middleware({
#     CORSMiddleware,
# })
app = FastAPI()
app.include_router(auth_router)
@app.get('/')
def login():
    return {'msg':'进入'}
