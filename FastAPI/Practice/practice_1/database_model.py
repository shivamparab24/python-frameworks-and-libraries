from sqlalchemy import Column, Integer, String, JSON

from sqlalchemy.orm import declarative_base

Base = declarative_base()

class StudentDB(Base):

    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    dept = Column(String)
    subjects = Column(JSON)