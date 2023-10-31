# Setup Root Path
import sys
sys.path.append('/root/PostOffice/')

# Import Packages
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Setup.Config import APP_Settings

# Define Database Connection
SQLALCHEMY_DATABASE_URL = f'postgresql://{APP_Settings.DB_USERNAME}:{APP_Settings.DB_PASSWORD}@{APP_Settings.DB_HOSTNAME}:{APP_Settings.DB_PORT}/{APP_Settings.DB_NAME}?sslmode=require'

# Create Database Engine
DB_Engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=20, max_overflow=0)

# Create Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=DB_Engine)

# Define Base Class
Base = declarative_base()

# Create DataBase
def Create_Database():

	# Create Database
	db = SessionLocal()

	# Create Tables
	try:

		# Commit Database
		yield db

	finally:

		# Close Database
		db.close()
