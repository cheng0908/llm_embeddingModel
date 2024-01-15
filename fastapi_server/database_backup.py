from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

MYSQL_USERNAME = os.getenv("MYSQL_USERNAME")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")

MYSQL_DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@localhost:3306/{DATABASE_NAME}"

engine = create_engine(MYSQL_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
