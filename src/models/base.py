from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

Base = declarative_base()

class Teacher(Base):
    __tablename__ = 'teachers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    qualification = Column(String, nullable=False)
    max_hours = Column(Integer, default=36)
    availability = Column(String)  # JSON строка с расписанием
    
    # Отношения
    subjects = relationship('TeacherSubject', back_populates='teacher')
    loads = relationship('TeacherLoad', back_populates='teacher')

class Subject(Base):
    __tablename__ = 'subjects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    profile = Column(String)
    required_hours = Column(Integer, nullable=False)
    is_elective = Column(Boolean, default=False)
    
    # Отношения
    teacher_subjects = relationship('TeacherSubject', back_populates='subject') 