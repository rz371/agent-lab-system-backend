from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.util.jwt import create_access_token, decode_access_token

# 意思是如果前端没有token，那么就去这个接口获取
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_schema), db: Session = Depends(get_db)
):
    """拿到token，判断token是否有效，无效抛出401，禁用抛出403，有效抛出用户信息"""
    try:
        payload = decode_access_token(token)

    except Exception:
        raise HTTPException(status_code=401, detail="登录用户已失效，请重新登录")

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="无效的登录凭证")

    user = db.query(User).filter(User.id == user_id).first()
    print(user)
    return user
