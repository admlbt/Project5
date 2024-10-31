from sqlalchemy.orm import Session
from models.teacher import Teacher
from typing import List, Optional

class TeacherService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_teacher(self, name: str, qualification: str, max_hours: int) -> Teacher:
        teacher = Teacher(
            name=name,
            qualification=qualification,
            max_hours=max_hours
        )
        self.db.add(teacher)
        self.db.commit()
        self.db.refresh(teacher)
        return teacher
    
    def get_all_teachers(self) -> List[Teacher]:
        return self.db.query(Teacher).all()
    
    def get_teacher_by_id(self, teacher_id: int) -> Optional[Teacher]:
        return self.db.query(Teacher).filter(Teacher.id == teacher_id).first()
    
    def update_teacher(self, teacher_id: int, **kwargs) -> Optional[Teacher]:
        teacher = self.get_teacher_by_id(teacher_id)
        if teacher:
            for key, value in kwargs.items():
                setattr(teacher, key, value)
            self.db.commit()
            self.db.refresh(teacher)
        return teacher
    
    def delete_teacher(self, teacher_id: int) -> bool:
        teacher = self.get_teacher_by_id(teacher_id)
        if teacher:
            self.db.delete(teacher)
            self.db.commit()
            return True
        return False 