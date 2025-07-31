# blog/crud/auth.py
from sqlalchemy.orm import Session
from blog.models.user import User

def get_or_create_user(db: Session, email: str, name: str | None = None):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, name=name)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user
