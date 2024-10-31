from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt

class SubjectsTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setup_table()
        
    def setup_table(self):
        # Настройка колонок
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels([
            "Название предмета",
            "Уровень",
            "Часы (10 класс)",
            "Часы (11 класс)",
            "Мин. квалификация",
            "Связанные предметы"
        ])
        
        # Настройка заголовков
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        
        # Настройка поведения таблицы
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setAlternatingRowColors(True)

    def add_subject(self, subject_data):
        row = self.rowCount()
        self.insertRow(row)
        
        name_item = QTableWidgetItem(str(subject_data['name']))
        name_item.setData(Qt.ItemDataRole.UserRole, subject_data['id'])
        self.setItem(row, 0, name_item)
        
        self.setItem(row, 1, QTableWidgetItem(str(subject_data['level'])))
        self.setItem(row, 2, QTableWidgetItem(str(subject_data['hours_10_class'])))
        self.setItem(row, 3, QTableWidgetItem(str(subject_data['hours_11_class'])))
        self.setItem(row, 4, QTableWidgetItem(str(subject_data['min_qualification'])))
        self.setItem(row, 5, QTableWidgetItem(", ".join(subject_data['related_subjects'])))

    def update_subject_row(self, row, subject_data):
        name_item = QTableWidgetItem(str(subject_data['name']))
        name_item.setData(Qt.ItemDataRole.UserRole, subject_data['id'])
        self.setItem(row, 0, name_item)
        
        self.setItem(row, 1, QTableWidgetItem(str(subject_data['level'])))
        self.setItem(row, 2, QTableWidgetItem(str(subject_data['hours_10_class'])))
        self.setItem(row, 3, QTableWidgetItem(str(subject_data['hours_11_class'])))
        self.setItem(row, 4, QTableWidgetItem(str(subject_data['min_qualification'])))
        self.setItem(row, 5, QTableWidgetItem(", ".join(subject_data['related_subjects'])))