from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session,  declarative_base
from dotenv import load_dotenv
import os
# 1. Database Connection
load_dotenv(override=True)
DB_URL = os.getenv("DB_URL")
if DB_URL is None:
    raise ImportError("DB_URL not found. Please check your .env file.")
engine = create_engine(DB_URL,echo=True)
sessionlocal = sessionmaker(autocommit=False, autoflush=False,bind = engine)
Base = declarative_base()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
 