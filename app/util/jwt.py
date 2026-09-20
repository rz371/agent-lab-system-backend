# 这里面实现的是 jwt的
from csv import Error
from datetime import datetime, timedelta

from fastapi import HTTPException
from app.config import settings
import jwt


def create_access_token(user_id: str):
    """
    对token进行加密
    -- 首先token要有payload（用户的唯一标识）
    注意：payload不可以放敏感信息
    -- 过期时间
    -- 官方印章 就是刚才的 JWT相关配置 JWT_SECRET_KEY
    -- 一种盖章算法

    jwt 三段：header.payload.signature
    -- header:描述token是用什么算法加密的，以及是什么类型
    -- payload：存放实际需要传递的数据
    -- signature:防止数据被篡改
    """
    # 计算过期时间
    expire = datetime.now() + timedelta(hours=settings.JWT_EXPIRE_HOURS)
    # exp 就这么写
    payload = {"user_id": user_id, "exp": expire}
    token = jwt.encode(
        payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return token


def decode_access_token(token: str):
    """解密token"""
    return jwt.decode(
        # 新版本要求algorithms必须是列表，且必须用关键字参数
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )
