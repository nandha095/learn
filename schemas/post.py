from pydantic import BaseModel
from typing import Optional,List
import datetime

class PostCreate(BaseModel):
    title: str
    content: str
    is_public: Optional[bool] = True

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    is_active: bool
    is_deleted: bool
    is_public: bool
    created_at: datetime.datetime
    user_id: int
    like_count: Optional[int] = 0
    liked_by: Optional[List[str]] = []

    model_config = {
        "arbitrary_types_allowed": True,
        "from_attributes": True  
    }

class PostStatusUpdate(BaseModel):
    is_active: bool

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_active: Optional[bool] = None
