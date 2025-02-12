from pydantic import BaseModel

class AddWorkExperience(BaseModel):
    job_role: str
    company_name: str
    job_description: str
    duration: str


class DisplayWorkExperience(AddWorkExperience):
    class Config:
        from_attributes = True