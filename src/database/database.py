from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Получаем путь к текущей директории
current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Создаем путь к файлу базы данных
DATABASE_URL = f"sqlite:///{os.path.join(current_dir, 'school.db')}"

# Создаем движок базы данных
engine = create_engine(DATABASE_URL)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем базовый класс для моделей
Base = declarative_base()

def init_db():
    """Инициализирует базу данных и применяет миграции"""
    from database.migrations import run_migrations
    
    # Создаем все таблицы, если их нет
    Base.metadata.create_all(bind=engine)
    
    # Запускаем миграции
    run_migrations()
    
    print("База данных успешно инициализирована!")

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()