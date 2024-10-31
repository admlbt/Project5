from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QLabel, QComboBox, QGroupBox, QMainWindow)
from PyQt6.QtCore import pyqtSignal

class SettingsTab(QWidget):
    theme_changed = pyqtSignal(str)  # Сигнал для изменения темы
    
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window  # Сохраняем ссылку на главное окно
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Группа настроек темы
        theme_group = QGroupBox("Настройки темы")
        theme_layout = QHBoxLayout()
        
        theme_label = QLabel("Тема приложения:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Светлая", "Тёмная"])
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        
        theme_group.setLayout(theme_layout)
        
        # Группа импорта/экспорта
        io_group = QGroupBox("Импорт/Экспорт данных")
        io_layout = QVBoxLayout()
        
        # Кнопки импорта/экспорта
        import_btn = QPushButton("Импорт всех данных из Excel")
        import_btn.clicked.connect(self.main_window.on_import_all)
        
        export_btn = QPushButton("Экспорт всех данных в Excel")
        export_btn.clicked.connect(self.main_window.on_export_all)
        
        io_layout.addWidget(import_btn)
        io_layout.addWidget(export_btn)
        
        io_group.setLayout(io_layout)
        
        # Добавляем группы в основной layout
        layout.addWidget(theme_group)
        layout.addWidget(io_group)
        layout.addStretch()
        
    def on_theme_changed(self, theme_name):
        self.theme_changed.emit(theme_name)