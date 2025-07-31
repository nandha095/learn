# blog/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from blog.database import Base
from datetime import datetime

# Association table for followers
followers_table = Table(
    "followers",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("users.id")),
    Column("followed_id", Integer, ForeignKey("users.id"))
)

# Association table for blocked users
blocks_table = Table(
    "blocks",
    Base.metadata,
    Column("blocker_id", Integer, ForeignKey("users.id")),
    Column("blocked_id", Integer, ForeignKey("users.id"))
)

post_likes = Table(
    "post_likes",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("post_id", Integer, ForeignKey("posts.id"))
)



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    dob = Column(DateTime, nullable=True)
    gender = Column(String(20), nullable=True)
    mobile_number = Column(String(20), nullable=True)
    name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=False)
    is_blocked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_private = Column(Boolean, default=False) 

    posts = relationship("blog.models.post.Post", back_populates="user")

    liked_posts = relationship(
        "blog.models.post.Post",
        secondary=post_likes,
        back_populates="liked_by"
    )

    followers = relationship(
        "User",
        secondary=followers_table,
        primaryjoin=id == followers_table.c.followed_id,
        secondaryjoin=id == followers_table.c.follower_id,
        backref="following"
    )

    blocked_users = relationship(
        "User",
        secondary=blocks_table,
        primaryjoin=id == blocks_table.c.blocker_id,
        secondaryjoin=id == blocks_table.c.blocked_id,
        backref="blocked_by"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', name='{self.name}')>"
