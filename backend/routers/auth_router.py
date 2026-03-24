"""认证路由：Google OAuth 登录"""

import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from auth.google import exchange_code_for_user
from auth.jwt_utils import create_token
from auth.dependencies import get_current_user
from config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/auth", tags=["auth"])


class GoogleLoginRequest(BaseModel):
    code: str
    redirect_uri: str


class LoginResponse(BaseModel):
    token: str
    user: dict


@router.post("/google", response_model=LoginResponse)
async def google_login(req: GoogleLoginRequest):
    """Google OAuth 登录：前端传 authorization code，后端换取用户信息并签发 JWT"""
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="未配置 Google OAuth")

    try:
        user_info = await exchange_code_for_user(req.code, req.redirect_uri)
    except Exception as e:
        logger.exception("Google OAuth 交换失败")
        raise HTTPException(status_code=400, detail=f"Google 登录失败: {e}")

    # 如果配置了数据库，则 upsert 用户
    user_record = None
    if settings.DATABASE_URL:
        try:
            from database import get_session
            from models import User

            session = get_session()
            try:
                user_record = session.query(User).filter_by(google_id=user_info["google_id"]).first()
                if user_record:
                    user_record.last_login_at = datetime.utcnow()
                    user_record.name = user_info["name"]
                    user_record.avatar_url = user_info["avatar_url"]
                else:
                    user_record = User(
                        google_id=user_info["google_id"],
                        email=user_info["email"],
                        name=user_info["name"],
                        avatar_url=user_info["avatar_url"],
                    )
                    session.add(user_record)
                session.commit()
                session.refresh(user_record)
            finally:
                session.close()
        except Exception:
            logger.warning("数据库操作失败，使用无数据库模式")

    user_id = user_record.id if user_record else 0
    token = create_token(user_id, user_info["email"])

    return LoginResponse(
        token=token,
        user={
            "id": user_id,
            "email": user_info["email"],
            "name": user_info["name"],
            "avatar_url": user_info["avatar_url"],
        },
    )


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    """获取当前登录用户信息"""
    return current_user
