"""FastAPI 认证依赖：从请求中提取并验证用户"""

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth.jwt_utils import decode_token

_bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer_scheme),
) -> dict:
    """
    从 Authorization: Bearer <token> 提取并验证用户。
    返回 {"user_id": int, "email": str}
    未登录或 token 无效时返回 401。
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未登录，请先使用 Google 登录",
        )
    try:
        payload = decode_token(credentials.credentials)
        return {"user_id": payload["user_id"], "email": payload["email"]}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="登录已过期，请重新登录",
        )
