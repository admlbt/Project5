from sqlalchemy import text
from database.database import engine, SessionLocal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migrations():
    """Выполняет все необходимые миграции"""
    db = SessionLocal()
    try:
        # Проверяем существование таблицы migrations
        create_migrations_table(db)
        
        # Список всех миграций
        migrations = [
            {
                'id': 1,
                'name': 'recreate_subjects_table',
                'function': recreate_subjects_table
            },
            # Добавляйте новые миграции сюда
        ]
        
        # Получаем последнюю выполненную миграцию
        last_migration = db.execute(text("SELECT migration_id FROM migrations ORDER BY migration_id DESC LIMIT 1")).scalar()
        if last_migration is None:
            last_migration = 0
            
        # Выполняем все невыполненные миграции
        for migration in migrations:
            if migration['id'] > last_migration:
                logger.info(f"Applying migration {migration['id']}: {migration['name']}")
                migration['function'](db)
                db.execute(
                    text("INSERT INTO migrations (migration_id, name) VALUES (:id, :name)"),
                    {'id': migration['id'], 'name': migration['name']}
                )
                db.commit()
                logger.info(f"Migration {migration['id']} completed successfully")
        
    except Exception as e:
        logger.error(f"Error during migration: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

def create_migrations_table(db):
    """Создает таблицу для отслеживания миграций"""
    db.execute(text("""
        CREATE TABLE IF NOT EXISTS migrations (
            migration_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))
    db.commit()

def recreate_subjects_table(db):
    """Миграция 1: Пересоздание таблицы subjects с новой структурой"""
    try:
        # Сохраняем существующие данные
        existing_data = []
        try:
            existing_data = db.execute(text("SELECT * FROM subjects")).fetchall()
        except:
            pass

        # Удаляем старую таблицу
        db.execute(text("DROP TABLE IF EXISTS subjects"))
        
        # Создаем новую таблицу с правильной структурой
        db.execute(text("""
            CREATE TABLE subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                level TEXT NOT NULL,
                hours_10_class INTEGER NOT NULL,
                hours_11_class INTEGER NOT NULL,
                related_subjects TEXT NOT NULL DEFAULT '[]',
                min_qualification TEXT NOT NULL
            )
        """))
        
        # Восстанавливаем данные, если они были
        for row in existing_data:
            try:
                db.execute(text("""
                    INSERT INTO subjects (name, level, hours_10_class, hours_11_class, 
                                        related_subjects, min_qualification)
                    VALUES (:name, :level, :hours_10, :hours_11, :related, :qual)
                """), {
                    'name': row.name,
                    'level': 'Базовый',  # значение по умолчанию
                    'hours_10': 1,        # значение по умолчанию
                    'hours_11': 1,        # значение по умолчанию
                    'related': '[]',      # значение по умолчанию
                    'qual': 'Без категории'  # значение по умолчанию
                })
            except Exception as e:
                logger.warning(f"Could not migrate data for subject {row.name}: {str(e)}")
        
        db.commit()
        logger.info("Subjects table recreated successfully")
        
    except Exception as e:
        logger.error(f"Error recreating subjects table: {str(e)}")
        db.rollback()
        raise