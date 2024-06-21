# Import Required Libraries
from enum import Enum


# Variable Data Segment Enum Class
class Variable_Segment(Enum):

    # Define Enumerations
    Unknown = 0
    Device = 1
    Power = 2
    GSM = 3
    Location = 4
    Environment = 5
    Water = 6
    Energy = 7
    FOTA = 9
