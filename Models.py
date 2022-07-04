from sqlalchemy import Column, Integer, String
from .Database import Base

class Device(Base):
    __tablename__ : "Devices"

    id = Column(Integer, primary_key=True, nullable=False)
    Device_ID = Column(String, nullable=False)
    IP = Column(String, nullable=False)