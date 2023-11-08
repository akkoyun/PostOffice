# Setup Root Path
import sys
sys.path.append('/root/PostOffice/')

# Import Packages
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, JSON
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from Setup.Database import Base, DB_Engine

# WeatherStat_Measurement Database Model
class WeatherStat_Measurement(Base):

	# Define Table Name
	__tablename__ = 'WeatherStat_Measurement' 
	__table_args__ = {'autoload': True, 'autoload_with': DB_Engine}

	# Define Columns
	Measurement_ID = Column(Integer, primary_key=True)
	Device_ID = Column(String())
	Stream_ID = Column(Integer)
	Variable = Column(String())
	Value = Column(Float)
	Create_Time = Column(TIMESTAMP(timezone=True))
	Max = Column(Float)
	Min = Column(Float)
	Max_Time = Column(TIMESTAMP(timezone=True))
	Min_Time = Column(TIMESTAMP(timezone=True))
	PreviousValue = Column(Float)
	Trend = Column(Integer)