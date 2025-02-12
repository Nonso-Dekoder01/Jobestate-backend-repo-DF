from datetime import date
from pydantic import BaseModel

class AddEducation(BaseModel):
    degree: str
    institution_name: str
    course: str
    admission_date: date
    completion_date: date


class DisplayEducation(AddEducation):
    date_added: date

    class Config:
        from_attributes=True