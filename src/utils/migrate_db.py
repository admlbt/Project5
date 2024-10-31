import os
import sys
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

from src.database.database import SessionLocal, init_db, Base, engine
from src.models.teacher import Teacher
from src.models.subject import Subject
from src.models.teacher_load import TeacherLoad, LevelType
from src.utils.migrate_subjects import migrate_subjects

def migrate_database():
    """
    Миграция базы данных
    """
    try:
        # Сначала мигрируем таблицу subjects
        migrate_subjects()
        
        # Затем выполняем миграцию teacher_loads
        TeacherLoad.__table__.drop(engine, checkfirst=True)
        Base.metadata.create_all(bind=engine)
        
        db = SessionLocal()
        try:
            # Получаем всех учителей
            teachers = db.query(Teacher).all()
            
            # Для каждого учителя
            for teacher in teachers:
                if teacher.last_year_load:
                    try:
                        last_year_data = json.loads(teacher.last_year_load)
                        
                        # Для каждого предмета в нагрузке
                        for subject_name, hours in last_year_data.items():
                            # Находим предмет
                            subject = db.query(Subject).filter(
                                Subject.name == subject_name
                            ).first()
                            
                            if subject:
                                # Создаем записи для 10 и 11 классов
                                for grade, hours_count in hours.items():
                                    if hours_count > 0:
                                        load = TeacherLoad(
                                            teacher_id=teacher.id,
                                            subject_id=subject.id,
                                            level=LevelType.BASE.value,  # По умолчанию базовый
                                            grade=int(grade),
                                            hours=hours_count,
                                            academic_year="2022-2023"
                                        )
                                        db.add(load)
                    except json.JSONDecodeError:
                        print(f"Ошибка при разборе JSON для учителя {teacher.name}")
                    except Exception as e:
                        print(f"Ошибка при миграции данных учителя {teacher.name}: {str(e)}")
                        continue
            
            # Сохраняем изменения
            db.commit()
            print("Миграция успешно завершена")
            
        except Exception as e:
            db.rollback()
            print(f"Ошибка при миграции данных: {str(e)}")
        finally:
            db.close()
            
    except Exception as e:
        print(f"Критическая ошибка при миграции: {str(e)}")

if __name__ == "__main__":
    migrate_database()