import pandas as pd
import json

def import_teachers_from_excel(file_path):
    try:
        # Пробуем прочитать лист "Учителя", если его нет - читаем первый лист
        try:
            df = pd.read_excel(file_path, sheet_name='Учителя')
        except ValueError:
            df = pd.read_excel(file_path)  # Читаем первый лист по умолчанию
            
        required_columns = ['ФИО', 'Квалификация', 'Макс. часов', 'Предметы', 'Нагрузка прошлого года']
        
        # Проверяем наличие всех необходимых колонок
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"В файле отсутствуют колонки: {', '.join(missing_columns)}")
        
        teachers_data = []
        for _, row in df.iterrows():
            # Обработка предметов (строка с разделителями)
            subjects = []
            if pd.notna(row['Предметы']):
                subjects = [s.strip() for s in str(row['Предметы']).split(',') if s.strip()]
            
            # Обработка нагрузки прошлого года (JSON строка)
            last_year_load = {}
            if pd.notna(row['Нагрузка прошлого года']):
                try:
                    last_year_load = json.loads(str(row['Нагрузка прошлого года']))
                except:
                    print(f"Ошибка при разборе нагрузки для учителя {row['ФИО']}")
            
            teacher_data = {
                'name': str(row['ФИО']).strip(),
                'qualification': str(row['Квалификация']).strip(),
                'max_hours': int(row['Макс. часов']),
                'subjects': subjects,
                'last_year_load': last_year_load,
                'is_active': True
            }
            teachers_data.append(teacher_data)
            
        return teachers_data
        
    except Exception as e:
        raise Exception(f"Ошибка при импорте учителей: {str(e)}")

def import_subjects_from_excel(file_path):
    try:
        # Пробуем прочитать лист "Предметы", если его нет - читаем первый лист
        try:
            df = pd.read_excel(file_path, sheet_name='Предметы')
        except ValueError:
            df = pd.read_excel(file_path)  # Читаем первый лист по умолчанию
            
        required_columns = ['Название предмета', 'Уровень', 'Часы (10 класс)', 
                          'Часы (11 класс)', 'Мин. квалификация', 'Связанные предметы']
        
        # Проверяем наличие всех необходимых колонок
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"В файле отсутствуют колонки: {', '.join(missing_columns)}")
        
        subjects_data = []
        for _, row in df.iterrows():
            # Обработка связанных предметов (строка с разделителями)
            related_subjects = []
            if pd.notna(row['Связанные предметы']):
                related_subjects = [s.strip() for s in str(row['Связанные предметы']).split(',') if s.strip()]
            
            subject_data = {
                'name': str(row['Название предмета']).strip(),
                'level': str(row['Уровень']).strip(),
                'hours_10_class': int(row['Часы (10 класс)']),
                'hours_11_class': int(row['Часы (11 класс)']),
                'min_qualification': str(row['Мин. квалификация']).strip(),
                'related_subjects': related_subjects
            }
            subjects_data.append(subject_data)
            
        return subjects_data
        
    except Exception as e:
        raise Exception(f"Ошибка при импорте предметов: {str(e)}")