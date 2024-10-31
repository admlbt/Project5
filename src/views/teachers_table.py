from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
import json

class TeachersTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        # Настройка колонок
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels([
            "ФИО", "Квалификация", "Макс. часов", 
            "Предметы", "Нагрузка прошлого года"
        ])
        
        # Настройка внешнего вида
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        # Растягиваем колонки
        header = self.horizontalHeader()
        for i in range(self.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
    
    def add_teacher(self, teacher_data):
        row = self.rowCount()
        self.insertRow(row)
        
        # Создаем и заполняем ячейки
        name_item = QTableWidgetItem(teacher_data['name'])
        name_item.setData(Qt.ItemDataRole.UserRole, teacher_data['id'])  # Сохраняем ID
        
        qual_item = QTableWidgetItem(teacher_data['qualification'])
        hours_item = QTableWidgetItem(str(teacher_data['max_hours']))
        
        subjects = json.loads(teacher_data['subjects']) if teacher_data['subjects'] else []
        subjects_item = QTableWidgetItem(', '.join(subjects))
        
        last_year = json.loads(teacher_data['last_year_load']) if teacher_data['last_year_load'] else {}
        last_year_item = QTableWidgetItem(str(last_year))
        
        # Устанавливаем ячейки
        self.setItem(row, 0, name_item)
        self.setItem(row, 1, qual_item)
        self.setItem(row, 2, hours_item)
        self.setItem(row, 3, subjects_item)
        self.setItem(row, 4, last_year_item)