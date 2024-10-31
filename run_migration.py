import os
import sys

# Добавляем путь к проекту в PYTHONPATH
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from src.utils.migrate_db import migrate_database

if __name__ == "__main__":
    migrate_database() 