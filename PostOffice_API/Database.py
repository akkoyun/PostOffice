from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .Config import settings

# Database URL Set
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# Declare Database Engine
DB_Engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Set Local Session
Local_Session = sessionmaker(autocommit=False, autoflush=False, bind=DB_Engine)

# Declare Base Model
Base = declarative_base()

# Get DB
def Get_DataBase():
	db = Local_Session()
	try:
		yield db
	finally:
		db.close()