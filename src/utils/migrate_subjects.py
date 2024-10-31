import os
import sys
import sqlite3

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)

from src.database.database import SessionLocal, init_db, Base, engine
from src.models.subject import Subject
from sqlalchemy import Column, Integer

def migrate_subjects():
    """
    Миграция таблицы subjects:
    Добавление столбцов для групп
    """
    try:
        # Получаем путь к базе данных
        db_path = os.path.join(project_root, 'school.db')
        
        # Создаем подключение к базе данных
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Добавляем новые столбцы
        new_columns = [
            ('groups_10_base', 'INTEGER DEFAULT 1'),
            ('groups_10_advanced', 'INTEGER DEFAULT 0'),
            ('groups_11_base', 'INTEGER DEFAULT 1'),
            ('groups_11_advanced', 'INTEGER DEFAULT 0')
        ]
        
        for column_name, column_type in new_columns:
            try:
                cursor.execute(f'ALTER TABLE subjects ADD COLUMN {column_name} {column_type}')
                print(f"Добавлен столбец {column_name}")
            except sqlite3.OperationalError as e:
                if 'duplicate column name' in str(e):
                    print(f"Столбец {column_name} уже существует")
                else:
                    raise e
        
        # Устанавливаем значения по умолчанию для существующих записей
        cursor.execute('''
            UPDATE subjects 
            SET groups_10_base = 1,
                groups_10_advanced = 0,
                groups_11_base = 1,
                groups_11_advanced = 0
            WHERE groups_10_base IS NULL
        ''')
        
        # Применяем изменения
        conn.commit()
        print("Миграция subjects успешно завершена")
        
    except Exception as e:
        print(f"Ошибка при миграции subjects: {str(e)}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    migrate_subjects() 