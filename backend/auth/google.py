"""Google OAuth：用 authorization code 换取用户信息"""

import httpx
from config import settings

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


async def exchange_code_for_user(code: str, redirect_uri: str) -> dict:
    """
    用 Google authorization code 换取用户信息。
    返回: {"google_id": "...", "email": "...", "name": "...", "avatar_url": "..."}
    """
    async with httpx.AsyncClient() as client:
        # Step 1: code → access_token
        token_resp = await client.post(GOOGLE_TOKEN_URL, data={
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        })
        token_resp.raise_for_status()
        token_data = token_resp.json()
        access_token = token_data["access_token"]

        # Step 2: access_token → user info
        user_resp = await client.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_resp.raise_for_status()
        user_data = user_resp.json()

        return {
            "google_id": user_data["id"],
            "email": user_data["email"],
            "name": user_data.get("name", ""),
            "avatar_url": user_data.get("picture", ""),
        }
