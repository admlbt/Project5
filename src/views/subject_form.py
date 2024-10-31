from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QSpinBox, QPushButton, QComboBox,
                           QListWidget)

class SubjectForm(QDialog):
    def __init__(self, parent=None, all_subjects=None):
        super().__init__(parent)
        self.setWindowTitle("Добавление предмета")
        self.setMinimumWidth(500)
        self.all_subjects = all_subjects or []
        
        layout = QVBoxLayout(self)
        
        # Название предмета
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Название:"))
        self.name_edit = QLineEdit()
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)
        
        # Уровень обучения
        level_layout = QHBoxLayout()
        level_layout.addWidget(QLabel("Уровень обучения:"))
        self.level_combo = QComboBox()
        self.level_combo.addItems(["Базовый", "Углубленный"])
        level_layout.addWidget(self.level_combo)
        layout.addLayout(level_layout)
        
        # Часы для 10 класса
        hours_10_layout = QHBoxLayout()
        hours_10_layout.addWidget(QLabel("Часов в неделю (10 класс):"))
        self.hours_10_spin = QSpinBox()
        self.hours_10_spin.setRange(1, 12)
        self.hours_10_spin.setValue(1)
        hours_10_layout.addWidget(self.hours_10_spin)
        layout.addLayout(hours_10_layout)
        
        # Часы для 11 класса
        hours_11_layout = QHBoxLayout()
        hours_11_layout.addWidget(QLabel("Часов в неделю (11 класс):"))
        self.hours_11_spin = QSpinBox()
        self.hours_11_spin.setRange(1, 12)
        self.hours_11_spin.setValue(1)
        hours_11_layout.addWidget(self.hours_11_spin)
        layout.addLayout(hours_11_layout)
        
        # Минимальная квалификация
        qual_layout = QHBoxLayout()
        qual_layout.addWidget(QLabel("Минимальная квалификация:"))
        self.qual_combo = QComboBox()
        self.qual_combo.addItems([
            "Без категории",
            "Первая категория",
            "Высшая категория"
        ])
        qual_layout.addWidget(self.qual_combo)
        layout.addLayout(qual_layout)
        
        # Связанные предметы
        layout.addWidget(QLabel("Связанные предметы:"))
        self.related_list = QListWidget()
        layout.addWidget(self.related_list)
        
        # Кнопки управления связанными предметами
        related_buttons = QHBoxLayout()
        add_related_btn = QPushButton("Добавить предмет")
        add_related_btn.clicked.connect(self.add_related_subject)
        remove_related_btn = QPushButton("Удалить предмет")
        remove_related_btn.clicked.connect(self.remove_related_subject)
        related_buttons.addWidget(add_related_btn)
        related_buttons.addWidget(remove_related_btn)
        layout.addLayout(related_buttons)
        
        # Кнопки формы
        buttons = QHBoxLayout()
        save_btn = QPushButton("Сохранить")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)
        buttons.addWidget(save_btn)
        buttons.addWidget(cancel_btn)
        layout.addLayout(buttons)

    def add_related_subject(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить связанный предмет")
        layout = QVBoxLayout(dialog)
        
        combo = QComboBox()
        # Фильтруем текущий предмет из списка
        current_name = self.name_edit.text().strip()
        available_subjects = [subj for subj in self.all_subjects 
                            if subj != current_name and 
                            subj not in [self.related_list.item(i).text() 
                                       for i in range(self.related_list.count())]]
        combo.addItems(available_subjects)
        layout.addWidget(combo)
        
        buttons = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(dialog.accept)
        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(dialog.reject)
        buttons.addWidget(ok_btn)
        buttons.addWidget(cancel_btn)
        layout.addLayout(buttons)
        
        if dialog.exec() and combo.currentText():
            self.related_list.addItem(combo.currentText())

    def remove_related_subject(self):
        current_item = self.related_list.currentItem()
        if current_item:
            self.related_list.takeItem(self.related_list.row(current_item))

    def get_data(self):
        return {
            'name': self.name_edit.text().strip(),
            'level': self.level_combo.currentText(),
            'hours_10_class': self.hours_10_spin.value(),
            'hours_11_class': self.hours_11_spin.value(),
            'min_qualification': self.qual_combo.currentText(),
            'related_subjects': [self.related_list.item(i).text() 
                               for i in range(self.related_list.count())]
        }

    def set_data(self, data):
        """Заполняет форму данными"""
        self.name_edit.setText(data['name'])
        self.level_combo.setCurrentText(data['level'])
        self.hours_10_spin.setValue(data['hours_10_class'])
        self.hours_11_spin.setValue(data['hours_11_class'])
        self.qual_combo.setCurrentText(data['min_qualification'])
        
        # Очищаем и заполняем список связанных предметов
        self.related_list.clear()
        for subject in data['related_subjects']:
            self.related_list.addItem(subject)