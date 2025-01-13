import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Define Base to be used by models
Base = declarative_base()

# Database URL (SQLite file in the data directory)
DATABASE_URL = "sqlite:///../data/interview_system.db"

# Ensure the directory exists
db_directory = os.path.dirname(os.path.abspath(DATABASE_URL.replace("sqlite:///", "")))
if not os.path.exists(db_directory):
    os.makedirs(db_directory)

# Create an engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency for getting DB sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Function to create all tables
def create_all_tables():
    # This will create the tables inside the existing database file
    Base.metadata.create_all(bind=engine)

