import sys
import os
import json

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.teacher_load import TeacherLoad, LevelType
from models.teacher import Teacher
from models.subject import Subject

class LoadDistributor:
    def __init__(self, db_session):
        self.db = db_session
        
    def distribute_load(self, teachers, subjects):
        distribution = {}
        
        # Сортируем учителей по квалификации
        sorted_teachers = sorted(teachers, 
                               key=lambda t: self.get_qualification_level(t.qualification),
                               reverse=True)
        
        # Для каждого предмета
        for subject in subjects:
            # Для каждого класса
            for grade in [10, 11]:
                # Для каждого уровня
                for level in [LevelType.BASE.value, LevelType.ADVANCED.value]:
                    # Получаем количество групп для данного класса и уровня
                    groups = self.get_groups_count(subject, grade, level)
                    if groups == 0:
                        continue
                        
                    # Получаем часы для данного класса
                    base_hours = subject.hours_10_class if grade == 10 else subject.hours_11_class
                    
                    # Для каждой группы
                    for group in range(groups):
                        # Находим подходящего учителя
                        suitable_teacher = self.find_suitable_teacher(
                            subject, sorted_teachers, grade, level, base_hours
                        )
                        
                        if suitable_teacher:
                            if suitable_teacher.id not in distribution:
                                distribution[suitable_teacher.id] = {}
                            
                            # Создаем уникальный ключ для предмета с учетом группы
                            load_key = f"{subject.id}_{grade}_{level}_{group}"
                            distribution[suitable_teacher.id][load_key] = {
                                'subject_id': subject.id,
                                'grade': grade,
                                'level': level,
                                'group': group + 1,
                                'hours': base_hours
                            }
        
        return distribution

    def get_groups_count(self, subject, grade, level):
        """Получение количества групп для предмета, класса и уровня"""
        if grade == 10:
            return subject.groups_10_base if level == LevelType.BASE.value else subject.groups_10_advanced
        else:
            return subject.groups_11_base if level == LevelType.BASE.value else subject.groups_11_advanced

    def find_suitable_teacher(self, subject, teachers, grade, level, hours):
        """Поиск подходящего учителя с учетом нагрузки"""
        suitable_teachers = []
        
        for teacher in teachers:
            if self.can_teach_subject(teacher, subject.name, level):
                current_load = self.get_teacher_current_load(teacher)
                
                # Проверяем, не превысит ли максимальную нагрузку
                if current_load + hours <= teacher.max_hours:
                    suitable_teachers.append({
                        'teacher': teacher,
                        'current_load': current_load,
                        'had_last_year': self.had_subject_last_year(teacher, subject, grade),
                        'qualification_level': self.get_qualification_level(teacher.qualification)
                    })
        
        if not suitable_teachers:
            return None
            
        # Сортируем учителей по приоритету
        suitable_teachers.sort(key=lambda x: (
            x['had_last_year'],  # Сначала те, кто вел в прошлом году
            -x['current_load'],  # Затем с меньшей нагрузкой
            x['qualification_level']  # Затем по квалификации
        ), reverse=True)
        
        return suitable_teachers[0]['teacher']

    def can_teach_subject(self, teacher, subject, level):
        """Проверка может ли учитель вести предмет"""
        try:
            teacher_subjects = json.loads(teacher.subjects)
            
            # Проверяем, есть ли предмет в списке предметов учителя
            if subject not in teacher_subjects:
                return False
            
            # Для углубленного уровня нужна высшая или первая категория
            if level == LevelType.ADVANCED.value:
                return teacher.qualification in ['Высшая категория', 'Первая категория']
                
            return True
            
        except Exception as e:
            print(f"Ошибка при проверке возможности преподавания: {str(e)}")
            return False

    def get_teacher_current_load(self, teacher):
        """Получение текущей нагрузки учителя"""
        try:
            loads = self.db.query(TeacherLoad).filter(
                TeacherLoad.teacher_id == teacher.id,
                TeacherLoad.academic_year == "2023-2024"
            ).all()
            
            return sum(load.hours for load in loads)
            
        except Exception as e:
            print(f"Ошибка при подсчете нагрузки: {str(e)}")
            return 0

    def had_subject_last_year(self, teacher, subject, grade):
        """Проверка вел ли учитель предмет в прошлом году"""
        try:
            last_year_load = self.db.query(TeacherLoad).filter(
                TeacherLoad.teacher_id == teacher.id,
                TeacherLoad.subject_id == subject.id,
                TeacherLoad.grade == grade,
                TeacherLoad.academic_year == "2022-2023"
            ).first()
            
            return last_year_load is not None
            
        except Exception as e:
            print(f"Ошибка при проверке прошлогодней нагрузки: {str(e)}")
            return False

    def get_qualification_level(self, qualification):
        """Получение числового уровня квалификации"""
        levels = {
            'Высшая категория': 3,
            'Первая категория': 2,
            'Без категории': 1
        }
        return levels.get(qualification, 0)
    
    # ... остальные вспомогательные методы 