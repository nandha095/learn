from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from blog.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True)
    name = Column(String(255))
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime,
     default=datetime.utcnow)
    password = Column(String(255), nullable=False)

class OTP(Base):
    __tablename__ = 'otp_codes'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), ForeignKey('users.email'), nullable=False)
    code = Column(String(6), nullable=False)
    expires_at = Column(DateTime)
    

