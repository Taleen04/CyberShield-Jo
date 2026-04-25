import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# SQLite file will be created at the project root
DATABASE_URL = os.getenv("DATABASE_URL")

# Fallback to SQLite locally
if not DATABASE_URL:
    DATABASE_URL = "postgresql://neondb_owner:npg_87pxFyruiflD@ep-bitter-paper-amnpbrdc.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require"
    #DATABASE_URL = "sqlite:///./test.db"
# SQLite vs PostgreSQL handling
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"sslmode": "require"}
    )

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)



Base = declarative_base()

# Dependency — injects a DB session into any route that needs it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()