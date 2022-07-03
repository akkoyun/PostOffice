from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection string
SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:00204063f4b4!N@localhost:5432/postgres'

# Database engine declaration
DB_Engine = create_engine(SQLALCHEMY_DATABASE_URL)

# DB session declaration
DB_Session = sessionmaker(autocommit=False, autoflush=False, bind=DB_Engine)

Base = declarative_base()

def get_db():
    db = DB_Session()
    try:
        yield db
    finally:
        db.close()