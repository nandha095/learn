from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use your actual MySQL credentials here
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Nec020602%40123@localhost:3306/fastblog"

# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:Nandha123@localhost:5433/fastblog"




engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
