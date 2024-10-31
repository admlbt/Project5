from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from src.database.database import Base

class LevelType(enum.Enum):
    BASE = "Базовый"
    ADVANCED = "Углубленный"

class TeacherLoad(Base):
    __tablename__ = 'teacher_loads'
    
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    level = Column(String)
    grade = Column(Integer)
    hours = Column(Integer)
    academic_year = Column(String)
    
    teacher = relationship("Teacher", back_populates="loads")
    subject = relationship("Subject", back_populates="loads") 