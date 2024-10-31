from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
                           QSpinBox, QComboBox, QPushButton, QMessageBox)

class SubjectDialog(QDialog):
    def __init__(self, parent=None, subject=None):
        super().__init__(parent)
        self.subject = subject
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()
        
        # Существующие поля
        self.name_edit = QLineEdit(self.subject.name if self.subject else "")
        self.hours_10_spin = QSpinBox()
        self.hours_11_spin = QSpinBox()
        self.qualification_combo = QComboBox()
        
        # Новые поля для групп
        self.groups_10_base_spin = QSpinBox()
        self.groups_10_advanced_spin = QSpinBox()
        self.groups_11_base_spin = QSpinBox()
        self.groups_11_advanced_spin = QSpinBox()
        
        # Настройка спинбоксов для групп
        for spin in [self.groups_10_base_spin, self.groups_10_advanced_spin,
                    self.groups_11_base_spin, self.groups_11_advanced_spin]:
            spin.setRange(0, 5)  # Максимум 5 групп
        
        # Заполняем значения если редактируем существующий предмет
        if self.subject:
            self.groups_10_base_spin.setValue(self.subject.groups_10_base)
            self.groups_10_advanced_spin.setValue(self.subject.groups_10_advanced)
            self.groups_11_base_spin.setValue(self.subject.groups_11_base)
            self.groups_11_advanced_spin.setValue(self.subject.groups_11_advanced)
        
        # Добавляем поля в форму
        form.addRow("Название:", self.name_edit)
        form.addRow("Часов в 10 классе:", self.hours_10_spin)
        form.addRow("Часов в 11 классе:", self.hours_11_spin)
        form.addRow("Мин. квалификация:", self.qualification_combo)
        form.addRow("Групп 10 класс (базовый):", self.groups_10_base_spin)
        form.addRow("Групп 10 класс (углубленный):", self.groups_10_advanced_spin)
        form.addRow("Групп 11 класс (базовый):", self.groups_11_base_spin)
        form.addRow("Групп 11 класс (углубленный):", self.groups_11_advanced_spin)
        
        # ... остальной код ... 