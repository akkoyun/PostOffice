from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL Set
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:00204063f4b4!N@localhost/PostOffice'

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