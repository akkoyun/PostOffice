from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Define database url
DATABASE_URL = 'postgresql://postgres:00204063f4b4!N@localhost/postgres'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=false, autoflush=false, bind=engine)

Base = declarative_base()