import datetime
import enum
from pydantic import BaseModel

class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"

class Patient(BaseModel):
    name: str
    surname: str
    age: int
    pesel: str
    gender: Gender
    appointment_time: datetime.time
