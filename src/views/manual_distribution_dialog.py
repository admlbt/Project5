from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QTableWidget, QLabel)

class ManualDistributionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Ручное распределение нагрузки")
        layout = QVBoxLayout(self)
        
        # Таблица для перетаскивания предметов
        self.distribution_table = QTableWidget()
        layout.addWidget(self.distribution_table)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        save_btn = QPushButton("Сохранить")
        cancel_btn = QPushButton("Отмена")
        
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)
        layout.addLayout(buttons_layout) 