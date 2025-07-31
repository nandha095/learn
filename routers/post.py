from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from blog.database import get_db
from blog.models import post as post_model, user as user_model
from blog.schemas.post import PostCreate, PostOut, PostUpdate
from blog.utils.jwt import get_current_user
from blog.schemas.post import PostStatusUpdate
from blog.schemas.post import PostUpdate
from blog.schemas.post import PostOut
from blog.models.post import Post
from fastapi.responses import JSONResponse




router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("", response_model=PostOut)
def create_post(payload: PostCreate, db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    new_post = post_model.Post(
        title=payload.title,
        content=payload.content,
        user_id=current_user.id,
        is_public=payload.is_public
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("", response_model=list[PostOut])
def get_feed(db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    from sqlalchemy import or_

    followed_ids = [user.id for user in current_user.following]
    
    posts = db.query(post_model.Post).join(user_model.User).filter(
        post_model.Post.is_active == True,
        post_model.Post.is_deleted == False,
        or_(
            user_model.User.is_private == False,
            post_model.Post.user_id.in_(followed_ids)
        )
    ).all()

   
    response = []
    for post in posts:
        response.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "is_active": post.is_active,
            "is_deleted": post.is_deleted,
            "is_public": post.is_public,
            "created_at": post.created_at,
            "user_id": post.user_id,
            "like_count": len(post.liked_by),
            "liked_by": [user.email for user in post.liked_by]
        })

    return response

@router.patch("/{post_id}", response_model=PostOut)
def partial_update_post(
    post_id: int,
    payload: PostUpdate,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    post = db.query(post_model.Post).filter_by(id=post_id, user_id=current_user.id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Apply only the fields provided
    if payload.title is not None:
        post.title = payload.title
    if payload.content is not None:
        post.content = payload.content
    if payload.is_active is not None:
        post.is_active = payload.is_active
    if payload.is_public is not None:
        post.is_public = payload.is_public

    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}")
def soft_delete_post(post_id: int, db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    post = db.query(post_model.Post).filter_by(id=post_id, user_id=current_user.id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.is_deleted = True
    db.commit()
    return {"message": "Post deleted (soft)"}


@router.post("/{post_id}/like")
def like_post(post_id: int, db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    post = db.query(post_model.Post).filter_by(id=post_id, is_deleted=False).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if current_user in post.liked_by:
        return {"message": "Already liked this post"}

    post.liked_by.append(current_user)
    db.commit()
    return {"message": "Post liked successfully"}


@router.post("/{post_id}/unlike")
def unlike_post(post_id: int, db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    post = db.query(post_model.Post).filter_by(id=post_id, is_deleted=False).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if current_user not in post.liked_by:
        return {"message": "You haven't liked this post"}

    post.liked_by.remove(current_user)
    db.commit()
    return {"message": "Post unliked successfully"}

@router.get("/{post_id}/likes")
def get_post_likes(post_id: int, db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    post = db.query(post_model.Post).filter_by(id=post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return {
        "post_id": post.id,
        "liked_by": [user.email for user in post.liked_by]
    }

