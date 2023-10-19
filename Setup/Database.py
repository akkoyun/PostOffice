from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Setup.Config import APP_Settings
import Models

# Define Database Connection
SQLALCHEMY_DATABASE_URL = f'postgresql://{APP_Settings.POSTOFFICE_DB_USERNAME}:{APP_Settings.POSTOFFICE_DB_PASSWORD}@{APP_Settings.POSTOFFICE_DB_HOSTNAME}:{APP_Settings.POSTOFFICE_DB_PORT}/{APP_Settings.POSTOFFICE_DB_NAME}?sslmode=require'

# Create Database Engine
DB_Engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=20, max_overflow=0)

# Insert Initial Data
event.listen(Models.GSM_MNC.__table__, 'after_create', Models.Insert_Initial_GSM_MNC)
event.listen(Models.GSM_MCC.__table__, 'after_create', Models.Insert_Initial_GSM_MCC)

# Create Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=DB_Engine)

# Define Base Class
Base = declarative_base()

# Create DataBase
def Create_Database():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()