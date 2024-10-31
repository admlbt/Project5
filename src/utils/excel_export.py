import pandas as pd
import json
from datetime import datetime

def export_teachers_to_excel(teachers, file_path):
    try:
        # Преобразуем данные в формат для DataFrame
        data = []
        for teacher in teachers:
            data.append({
                'ФИО': teacher.name,
                'Квалификация': teacher.qualification,
                'Макс. часов': teacher.max_hours,
                'Предметы': ', '.join(json.loads(teacher.subjects) if teacher.subjects else []),
                'Нагрузка прошлого года': teacher.last_year_load if teacher.last_year_load else '{}'
            })
        
        # Создаем DataFrame
        df = pd.DataFrame(data)
        
        # Если путь не указан, генерируем имя файла с текущей датой и временем
        if not file_path:
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = f"teachers_export_{current_time}.xlsx"
        
        # Создаем writer для сохранения в Excel
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            # Сохраняем на лист "Учителя"
            df.to_excel(writer, sheet_name='Учителя', index=False)
        
    except Exception as e:
        raise Exception(f"Ошибка при экспорте учителей: {str(e)}")

def export_subjects_to_excel(subjects, file_path):
    try:
        # Преобразуем данные в формат для DataFrame
        data = []
        for subject in subjects:
            data.append({
                'Название предмета': subject.name,
                'Уровень': subject.level,
                'Часы (10 класс)': subject.hours_10_class,
                'Часы (11 класс)': subject.hours_11_class,
                'Мин. квалификация': subject.min_qualification,
                'Связанные предметы': ', '.join(json.loads(subject.related_subjects) if subject.related_subjects else [])
            })
        
        # Создаем DataFrame
        df = pd.DataFrame(data)
        
        # Генерируем имя файла с текущей датой и временем
        if not file_path:
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = f"subjects_export_{current_time}.xlsx"
        
        try:
            # Пытаемся открыть существующий файл
            with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
                df.to_excel(writer, sheet_name='Предметы', index=False)
        except FileNotFoundError:
            # Если файл не существует, создаем новый
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Предметы', index=False)
        
    except Exception as e:
        raise Exception(f"Ошибка при экспорте предметов: {str(e)}")

def export_all_to_excel(teachers, subjects, file_path):
    """Экспортирует и учителей, и предметы в один файл"""
    try:
        # Если путь не указан, генерируем имя файла с текущей датой и временем
        if not file_path:
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = f"school_export_{current_time}.xlsx"
            
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            # Экспорт учителей
            teachers_data = []
            for teacher in teachers:
                teachers_data.append({
                    'ФИО': teacher.name,
                    'Квалификация': teacher.qualification,
                    'Макс. часов': teacher.max_hours,
                    'Предметы': ', '.join(json.loads(teacher.subjects) if teacher.subjects else []),
                    'Нагрузка прошлого года': teacher.last_year_load if teacher.last_year_load else '{}'
                })
            pd.DataFrame(teachers_data).to_excel(writer, sheet_name='Учителя', index=False)
            
            # Экспорт предметов
            subjects_data = []
            for subject in subjects:
                subjects_data.append({
                    'Название предмета': subject.name,
                    'Уровень': subject.level,
                    'Часы (10 класс)': subject.hours_10_class,
                    'Часы (11 класс)': subject.hours_11_class,
                    'Мин. квалификация': subject.min_qualification,
                    'Связанные предметы': ', '.join(json.loads(subject.related_subjects) if subject.related_subjects else [])
                })
            pd.DataFrame(subjects_data).to_excel(writer, sheet_name='Предметы', index=False)
            
    except Exception as e:
        raise Exception(f"Ошибка при экспорте данных: {str(e)}")