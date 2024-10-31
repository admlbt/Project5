from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.database import Base

class Subject(Base):
    __tablename__ = 'subjects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    hours_10_class = Column(Integer)
    hours_11_class = Column(Integer)
    min_qualification = Column(String)
    related_subjects = Column(String)
    
    groups_10_base = Column(Integer, default=1)
    groups_10_advanced = Column(Integer, default=0)
    groups_11_base = Column(Integer, default=1)
    groups_11_advanced = Column(Integer, default=0)
    
    loads = relationship("TeacherLoad", back_populates="subject")