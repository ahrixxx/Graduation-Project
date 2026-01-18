from sqlalchemy.orm import Session
from refresh_token.refresh_entity import RefreshToken
from datetime import datetime, timedelta

def save_refresh_token(db: Session, user_id: int, token: str):
    rt = RefreshToken(
        user_id=user_id,
        refresh_token=token,
        expires_at=datetime.utcnow() + timedelta(days=14)
    )
    db.add(rt)
    db.commit()

def find_by_token(db: Session, token: str):
    return db.query(RefreshToken).filter(
        RefreshToken.refresh_token == token,
        RefreshToken.revoked_at.is_(None),
        RefreshToken.expires_at > datetime.utcnow()
    ).first()

def revoke_all(db: Session, user_id: int):
    db.query(RefreshToken).filter(
        RefreshToken.user_id == user_id,
        RefreshToken.revoked_at.is_(None)
    ).update({"revoked_at": datetime.utcnow()})
    db.commit()
