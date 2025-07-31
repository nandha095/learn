from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from authentication.config import Base

import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True) 
    password = Column(String(128)) 
    email = Column(String(255))
    Phone_number = Column(String(20)) 
    first_name = Column(String(100))
    last_name = Column(String(100))
    create_date = Column(DateTime, default=datetime.datetime.now)
    update_date = Column(DateTime) 