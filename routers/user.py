# blog/routers/user.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from blog.database import get_db
from blog.utils.jwt import get_current_user
from blog.models import user as models
from blog.schemas.post import PostStatusUpdate
from blog.models import user as user_model
from blog.models import post as post_model
from blog.models.user import User
from fastapi import APIRouter, Depends
from blog.utils.jwt import get_current_user
from blog.schemas.user import UpdatePrivacyRequest


router = APIRouter(prefix="/me", tags=["User"])


@router.get("/me")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "is_active": current_user.is_active,
        "is_private": current_user.is_private
    }


@router.patch("/{post_id}/status")
def update_post_status(
    post_id: int,
    payload: PostStatusUpdate,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    post = db.query(post_model.Post).filter_by(id=post_id, user_id=current_user.id).first() 
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.is_active = payload.is_active
    db.commit()
    return {"message": "Post status updated"}


@router.post("/follow/{user_id}")
def follow_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    target_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    if target_user in current_user.following:
        return {"message": "Already following this user"}
    current_user.following.append(target_user)
    db.commit()
    return {"message": "Followed user successfully"}


@router.post("/unfollow/{user_id}")
def unfollow_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    target_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    if target_user not in current_user.following:
        return {"message": "Not following this user"}
    current_user.following.remove(target_user)
    db.commit()
    return {"message": "Unfollowed user successfully"}


@router.post("/block/{user_id}")
def block_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    target_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    if target_user in current_user.blocked_users:
        return {"message": "Already blocked this user"}
    current_user.blocked_users.append(target_user)
    db.commit()
    return {"message": "User blocked successfully"}


@router.get("/followers")
def get_followers(
    current_user: models.User = Depends(get_current_user)
):
    return [{"id": user.id, "email": user.email} for user in current_user.followers]


@router.get("/following")
def get_following(
    current_user: models.User = Depends(get_current_user)
):
    return [{"id": user.id, "email": user.email} for user in current_user.following]


@router.get("/me")
def get_my_profile(current_user: models.User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "is_active": current_user.is_active,
        "is_blocked": current_user.is_blocked,
        "is_private": current_user.is_private
    }


@router.get("/user/{user_id}/posts")
def get_user_posts(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Private check: allow only self or followers to view
    if user.is_private and user.id != current_user.id and current_user not in user.followers:
        raise HTTPException(status_code=403, detail="This account is private")

    posts = db.query(post_model.Post).filter_by(user_id=user.id, is_active=True).all()
    return posts



@router.patch("/update-privacy")
def update_privacy(
    payload: UpdatePrivacyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_user.is_private = payload.is_private
    db.commit()
    return {"message": "Privacy updated", "is_private": current_user.is_private}

