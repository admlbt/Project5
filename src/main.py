import sys
import os

# Добавляем путь к корневой директории проекта
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from PyQt6.QtWidgets import QApplication
from src.views.main_window import MainWindow
from src.database.database import init_db
from src.utils.migrate_db import migrate_database

def main():
    # Инициализация базы данных
    init_db()
    
    # Выполняем миграцию при первом запуске
    migrate_database()
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 