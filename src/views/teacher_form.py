from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QSpinBox, QComboBox, QPushButton,
                           QListWidget, QListWidgetItem)

class TeacherForm(QDialog):
    def __init__(self, parent=None, available_subjects=None):
        super().__init__(parent)
        self.available_subjects = available_subjects or []
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Добавление учителя")
        layout = QVBoxLayout(self)
        
        # ФИО
        name_layout = QHBoxLayout()
        name_label = QLabel("ФИО:")
        self.name_edit = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)
        
        # Квалификация
        qual_layout = QHBoxLayout()
        qual_label = QLabel("Квалификация:")
        self.qual_combo = QComboBox()
        self.qual_combo.addItems([
            "Без категории",
            "Первая категория",
            "Высшая категория"
        ])
        qual_layout.addWidget(qual_label)
        qual_layout.addWidget(self.qual_combo)
        layout.addLayout(qual_layout)
        
        # Максимальные часы
        hours_layout = QHBoxLayout()
        hours_label = QLabel("Макс. часов:")
        self.hours_spin = QSpinBox()
        self.hours_spin.setRange(1, 40)
        self.hours_spin.setValue(18)
        hours_layout.addWidget(hours_label)
        hours_layout.addWidget(self.hours_spin)
        layout.addLayout(hours_layout)
        
        # Предметы
        subjects_label = QLabel("Предметы:")
        layout.addWidget(subjects_label)
        
        subjects_layout = QHBoxLayout()
        
        # Список доступных предметов
        self.available_list = QListWidget()
        self.available_list.addItems(self.available_subjects)
        subjects_layout.addWidget(self.available_list)
        
        # Кнопки добавления/удаления
        buttons_layout = QVBoxLayout()
        add_button = QPushButton(">")
        remove_button = QPushButton("<")
        add_button.clicked.connect(self.add_subject)
        remove_button.clicked.connect(self.remove_subject)
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(remove_button)
        subjects_layout.addLayout(buttons_layout)
        
        # Список выбранных предметов
        self.selected_list = QListWidget()
        subjects_layout.addWidget(self.selected_list)
        
        layout.addLayout(subjects_layout)
        
        # Кнопки OK и Cancel
        buttons_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Отмена")
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        layout.addLayout(buttons_layout)
        
    def add_subject(self):
        current_item = self.available_list.currentItem()
        if current_item:
            self.selected_list.addItem(current_item.text())
            self.available_list.takeItem(self.available_list.row(current_item))
            
    def remove_subject(self):
        current_item = self.selected_list.currentItem()
        if current_item:
            self.available_list.addItem(current_item.text())
            self.selected_list.takeItem(self.selected_list.row(current_item))
            
    def get_data(self):
        selected_subjects = []
        for i in range(self.selected_list.count()):
            selected_subjects.append(self.selected_list.item(i).text())
            
        return {
            'name': self.name_edit.text(),
            'qualification': self.qual_combo.currentText(),
            'max_hours': self.hours_spin.value(),
            'subjects': selected_subjects
        }