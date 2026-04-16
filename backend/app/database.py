from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# SQLite file will be created at the project root
DATABASE_URL = "sqlite:///./Cybershield.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # required for SQLite + FastAPI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



Base = declarative_base()

# Dependency — injects a DB session into any route that needs it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()