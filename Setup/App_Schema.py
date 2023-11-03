# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

# Define App Base Model
# Version 01.00.00

# Device Info
class Device(BaseModel):

	# Timestamp
	LastUpdate: str = Field(description="Last Measurement time stamp.", example="2022-07-19T08:28:32Z")
