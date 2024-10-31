from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.database import Base

class Teacher(Base):
    __tablename__ = 'teachers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    qualification = Column(String)
    subjects = Column(String)
    max_hours = Column(Integer)
    last_year_load = Column(String)
    
    loads = relationship("TeacherLoad", back_populates="teacher")