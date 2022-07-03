from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Define Schema
class Device_Post(BaseModel):
    Type: int
    ID: str
    Location: Optional[str]
    Owner: Optional[str]
    IP: Optional[str]

    class Config:
        orm_mode = True