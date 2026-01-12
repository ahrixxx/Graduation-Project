from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from common.database import get_db
from auth.auth_service import kakao_login
from auth.auth_schema import (
    LoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse
)
from refresh_token.refresh_repository import find_by_token
from common.security import create_access_token
from common.config import settings

router = APIRouter(prefix="/api/auth")

@router.get("/kakao/login")
def kakao_login_redirect():
    kakao_url = (
        "https://kauth.kakao.com/oauth/authorize"
        "?response_type=code"
        f"&client_id={settings.kakao_client_id}"
        f"&redirect_uri={settings.kakao_redirect_uri}"
    )
    return {"redirectUrl": kakao_url}

@router.get("/kakao/callback", response_model=LoginResponse)
def kakao_callback(
    code: str = Query(...),
    db: Session = Depends(get_db)
):
    return kakao_login(db, code)

@router.post("/refresh-token", response_model=RefreshTokenResponse)
def refresh_token(
    req: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    rt = find_by_token(db, req.refreshToken)
    if not rt:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access = create_access_token(rt.user_id)
    return {"accessToken": access}
