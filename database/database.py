from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get the absolute path of the 'database' folder (where this file lives)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the path to the SQLite folder inside 'database'
SQLITE_DIR = os.path.join(BASE_DIR, "sqlite")

# Create the sqlite folder if it doesn't exist
if not os.path.exists(SQLITE_DIR):
    os.makedirs(SQLITE_DIR)

# Define the full path to the .db file
DB_FILE_PATH = os.path.join(SQLITE_DIR, "training_assistant.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE_PATH}"

# Create the engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()