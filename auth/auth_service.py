from sqlalchemy.orm import Session
from auth.kakao_service import get_access_token, get_user_info
from user.user_entity import User
from user.user_repository import find_by_provider, save
from common.security import create_access_token, create_refresh_token
from refresh_token.refresh_repository import save_refresh_token

def kakao_login(db: Session, code: str):
    kakao_token = get_access_token(code)
    kakao_user = get_user_info(kakao_token)

    provider_id = str(kakao_user["id"])
    email = kakao_user["kakao_account"].get("email")

    user = find_by_provider(db, "kakao", provider_id)
    is_new = False

    if not user:
        user = User(
            provider="kakao",
            provider_id=provider_id,
            email=email
        )
        save(db, user)
        is_new = True

    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)

    save_refresh_token(db, user.id, refresh)

    return {
        "accessToken": access,
        "refreshToken": refresh,
        "userId": user.id,
        "isNewUser": is_new
    }
