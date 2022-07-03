from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from .Database import Base

class Devices(Base):
    __tablename__ = "Devices"

    ID = Column(String, primary_key=True, nullable=False)
    Type = Column(Integer, nullable=False)
    Location = Column(String, nullable=True)
    Owner = Column(String, nullable=True)
    IP = Column(String, nullable=False)
