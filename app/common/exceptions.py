# 全局异常处理
# 给后端搞一个 ‘总保安’ 无论哪个接口，只要抛出异常，就从这个py下找对应的错误，返回统一的
# JSON格式给后端，
# ===== 统一 =========

# HTTPException
# ValueException


# 优雅的做法：自定义一个业务异常类，遇到错误直接抛出去，让全局异常处理器去 抓
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.common.response import Response


class BusinessException(Exception):
    """
    自定义的业务异常

    == 业务异常：代码没写错，但用户的请求不符合业务规则
    比如密码输错，就是业务异常
    == 业务异常，统一的状态码都是200
    业务异常通常是用户操作问题（400，401，403）而500是系统崩溃
    """

    def __init__(self, message: str, code: int = 400):
        super().__init__(message)
        self.code = code
        self.message = message


async def business_exception_handler(request: Request, exc: BusinessException):
    """
    request:代表刚才发起的那个HTTP请求本身
    exc:是exception缩写，表示 raise出来的那个具体的异常对象
    """

    return JSONResponse(
        status_code=200,
        # model_dump 转为字典
        content=Response.error(code=exc.code, message=exc.message).model_dump(),
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """
    HTTPException ，fastapi自带的异常类
    """

    return JSONResponse(
        status_code=exc.status_code,
        # model_dump 转为字典
        content=Response.error(code=exc.status_code, message=exc.detail).model_dump(),
    )


async def valid_exception_handler(request: Request, exc: RequestValidationError):
    """
    RequestValidationError : pydantic抛出的异常，请求参数校验异常
    """
    error_msg = exc.errors()[0]["msg"]
    return JSONResponse(
        status_code=422,  # 422是fastapi默认的参数校验错误码
        # model_dump 转为字典
        content=Response.error(code=422, message=f"参数错误：{error_msg}").model_dump(),
    )


async def excep_exception_handler(request: Request, exc: Exception):
    """
    Exception : 最后兜底的异常
    """
    return JSONResponse(
        status_code=500,
        # model_dump 转为字典
        content=Response.error(
            code=500, message="服务器内部错误，请稍后再试"
        ).model_dump(),
    )
