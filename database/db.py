from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from pathlib import Path


env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
db_port = os.getenv("DATABASE_PORT")
db_password = os.getenv("DATABASE_PASSWORD")
db_host = os.getenv("DATABASE_HOST")

if db_host is None or db_password is None or db_port is None:
    raise ValueError("Database URL,password or host are not set in environment variables.")


DATABASE_URL = f"postgresql://postgres:{db_password}@{db_host}:{db_port}/leads_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
