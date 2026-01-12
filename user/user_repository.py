from sqlalchemy.orm import Session
from user.user_entity import User

def find_by_provider(db: Session, provider: str, provider_id: str):
    return db.query(User).filter(
        User.provider == provider,
        User.provider_id == provider_id
    ).first()

def save(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
