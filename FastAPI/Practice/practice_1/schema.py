from pydantic import BaseModel

class Student(BaseModel):
    id: int
    name: str
    dept: str
    subjects: list[str]
