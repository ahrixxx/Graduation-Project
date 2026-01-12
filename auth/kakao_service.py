import requests
from common.config import settings

def get_access_token(code: str):
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": settings.kakao_client_id,
        "client_secret": settings.kakao_client_secret,
        "redirect_uri": settings.kakao_redirect_uri,
        "code": code,
    }
    return requests.post(url, data=data).json()["access_token"]

def get_user_info(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    return requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers=headers
    ).json()
