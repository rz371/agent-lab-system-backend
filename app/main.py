from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from fastapi.middleware.cors import CORSMiddleware


from app.common.exceptions import (
    BusinessException,
    business_exception_handler,
    excep_exception_handler,
    http_exception_handler,
    valid_exception_handler,
)

from app.database import Base, engine
from app.api import api

# 导入 User 是为了告诉程序我有这个表，记得去创建
from app.models.user import User

Base.metadata.create_all(bind=engine)  # 自动创建表

app = FastAPI()
app.include_router(api)
# 跨域
origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许前端访问的接口，不要写 *
    allow_methods=["*"],  # 所有的请求方法
    allow_headers=["*"],  # 所有的请求头
    allow_credentials=True,  # 关键点：允许前端携带 Authorization token
)
# 注册全局异常处理器 (按顺序！)
# 参数1：异常类，
# 参数2：处理函数
app.add_exception_handler(BusinessException, business_exception_handler)  # 1
app.add_exception_handler(HTTPException, http_exception_handler)  # 2
app.add_exception_handler(RequestValidationError, valid_exception_handler)  # 3
# 这个必须写到最后！
app.add_exception_handler(Exception, excep_exception_handler)  # 4
# 1 不是 ，去找2 ，按顺序判断类型


@app.get("/")
def login():
    return {"msg": "进入"}
