from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QTabWidget, QPushButton, QLabel, QMessageBox,
                           QFileDialog, QTableWidgetItem, QApplication,
                           QToolBar, QStatusBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QAction
import sys
import os

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from views.teacher_form import TeacherForm
from views.teachers_table import TeachersTable
from views.subject_form import SubjectForm
from views.subjects_table import SubjectsTable
from database.database import SessionLocal
from models.teacher import Teacher
from models.subject import Subject
from utils.excel_import import import_teachers_from_excel, import_subjects_from_excel
from utils.excel_export import export_teachers_to_excel, export_subjects_to_excel, export_all_to_excel
import json
from views.settings_tab import SettingsTab
from utils.themes import set_dark_theme, set_light_theme
from views.load_tab import LoadTab
from views.teachers_tab import TeachersTab
from views.subjects_tab import SubjectsTab
from views.reports_tab import ReportsTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система распределения нагрузки")
        self.setMinimumSize(800, 600)
        
        # Инициализируем базу данных
        self.db = SessionLocal()
        
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Главный layout
        main_layout = QVBoxLayout(central_widget)
        
        # Заголовок
        header = QLabel("Система управления нагрузкой учителей")
        header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)
        
        # Создаем вкладки
        self.tabs = QTabWidget()
        
        # Добавляем вкладки
        self.tabs.addTab(self.create_teachers_tab(), "Учителя")
        self.tabs.addTab(self.create_subjects_tab(), "Предметы")
        
        # Добавляем вкладку настроек
        self.settings_tab = SettingsTab(main_window=self)
        self.settings_tab.theme_changed.connect(self.change_theme)
        self.tabs.addTab(self.settings_tab, "Настройки")
        
        # Добавляем вкладку нагрузки
        self.load_tab = LoadTab(self)
        self.tabs.addTab(self.load_tab, "Нагрузка")
        
        main_layout.addWidget(self.tabs)
        
        # Загружаем существующих учителей
        self.load_teachers()

    def create_teachers_tab(self):
        """Создание вкладки учителей"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Панель инструментов
        toolbar = QHBoxLayout()
        
        # Основные кнопки
        add_button = QPushButton("Добавить учителя")
        add_button.clicked.connect(self.on_add_teacher)
        edit_button = QPushButton("Редактировать")
        edit_button.clicked.connect(self.on_edit_teacher)
        delete_button = QPushButton("Удалить")
        delete_button.clicked.connect(self.on_delete_teacher)
        
        # Кнопки импорта/экспорта
        import_teachers_btn = QPushButton("Импорт из Excel")
        import_teachers_btn.clicked.connect(self.on_import_teachers)
        export_teachers_btn = QPushButton("Экспорт в Excel")
        export_teachers_btn.clicked.connect(self.on_export_teachers)
        
        toolbar.addWidget(add_button)
        toolbar.addWidget(edit_button)
        toolbar.addWidget(delete_button)
        toolbar.addWidget(import_teachers_btn)
        toolbar.addWidget(export_teachers_btn)
        toolbar.addStretch()
        
        layout.addLayout(toolbar)
        
        # Таблца
        self.teachers_table = TeachersTable()
        layout.addWidget(self.teachers_table)
        
        # Загружаем существующих учителей
        self.load_teachers()
        
        return widget

    def create_subjects_tab(self):
        """Создание вкладки предметов"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Панель инструментов
        toolbar = QHBoxLayout()
        
        # Основные кнопки
        add_button = QPushButton("Добавить предмет")
        add_button.clicked.connect(self.on_add_subject)
        edit_button = QPushButton("Редактировать")
        edit_button.clicked.connect(self.on_edit_subject)
        delete_button = QPushButton("Удалить")
        delete_button.clicked.connect(self.on_delete_subject)
        
        # Кно��ки импорта/экспорта
        import_subjects_btn = QPushButton("Импорт из Excel")
        import_subjects_btn.clicked.connect(self.on_import_subjects)
        export_subjects_btn = QPushButton("Экспорт в Excel")
        export_subjects_btn.clicked.connect(self.on_export_subjects)
        
        toolbar.addWidget(add_button)
        toolbar.addWidget(edit_button)
        toolbar.addWidget(delete_button)
        toolbar.addWidget(import_subjects_btn)
        toolbar.addWidget(export_subjects_btn)
        toolbar.addStretch()
        
        layout.addLayout(toolbar)
        
        # Таблица
        self.subjects_table = SubjectsTable()
        layout.addWidget(self.subjects_table)
        
        # Загружаем существующие предметы
        self.load_subjects()
        
        return widget

    def create_load_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("Раздел нагрузки в разработке"))
        return widget

    def load_teachers(self):
        """Загрузка учителей в таблицу"""
        try:
            # Очищаем таблицу
            self.teachers_table.setRowCount(0)
            
            # Получа��м всех учителей из базы данных
            teachers = self.db.query(Teacher).all()
            
            # Добавляем каждого учителя в таблицу
            for teacher in teachers:
                self.teachers_table.add_teacher(teacher.to_dict())
                
        except Exception as e:
            print(f"Ошибка при загрузке учителей: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке учителей: {str(e)}")

    def on_add_teacher(self):
        try:
            # Получаем список всех предметов для выбора
            subjects = [subject.name for subject in self.db.query(Subject).all()]
            
            dialog = TeacherForm(parent=self, available_subjects=subjects)
            if dialog.exec():
                teacher_data = dialog.get_data()
                
                if not teacher_data['name']:
                    QMessageBox.warning(self, "Ошибка", "ФИО учителя не может быть пустым!")
                    return
                
                # Проверяем, существует ли уже учитель с таким именем
                existing_teacher = self.db.query(Teacher).filter(
                    Teacher.name == teacher_data['name']
                ).first()
                
                if existing_teacher:
                    QMessageBox.warning(self, "Ошибка", "Учитель с таким ФИО уже существует!")
                    return
                
                # Создаем объект Teacher
                new_teacher = Teacher(
                    name=teacher_data['name'],
                    qualification=teacher_data['qualification'],
                    max_hours=teacher_data['max_hours'],
                    subjects=json.dumps(teacher_data['subjects']),
                    last_year_load=json.dumps({}),
                    is_active=True
                )
                
                try:
                    # Добавляем в базу данных
                    self.db.add(new_teacher)
                    self.db.commit()
                    self.db.refresh(new_teacher)  # Обновляем объект, чтобы получить ID
                    
                    # Обновляем таблицу
                    self.load_teachers()  # Перезагружаем всю таблицу
                    
                except Exception as e:
                    self.db.rollback()
                    print(f"Ошибка при сохранении учителя: {str(e)}")
                    QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении: {str(e)}")
                
        except Exception as e:
            print(f"Ошибка при добавлении учителя: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def on_import_teachers(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Выберите файл Excel с данными учителей",
                "",
                "Excel Files (*.xlsx *.xls)"
            )
            
            if file_path:
                teachers_data = import_teachers_from_excel(file_path)
                for teacher_data in teachers_data:
                    # Проверяем существование учителя
                    existing_teacher = self.db.query(Teacher).filter(
                        Teacher.name == teacher_data['name']
                    ).first()
                    
                    if existing_teacher:
                        # Обновляем существующего учитея
                        existing_teacher.qualification = teacher_data['qualification']
                        existing_teacher.max_hours = teacher_data['max_hours']
                        existing_teacher.subjects = json.dumps(teacher_data['subjects'])
                        existing_teacher.last_year_load = json.dumps(teacher_data['last_year_load'])
                    else:
                        # Создаем нового учителя
                        new_teacher = Teacher(
                            name=teacher_data['name'],
                            qualification=teacher_data['qualification'],
                            max_hours=teacher_data['max_hours'],
                            subjects=json.dumps(teacher_data['subjects']),
                            last_year_load=json.dumps(teacher_data['last_year_load']),
                            is_active=True
                        )
                        self.db.add(new_teacher)
                
                try:
                    self.db.commit()
                    # Обновляем таблицу
                    self.load_teachers()
                    QMessageBox.information(self, "Успех", "Импорт учителей успешно завершен")
                except Exception as e:
                    self.db.rollback()
                    print(f"Ошибка при сохранении данных: {str(e)}")
                    QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении: {str(e)}")
                
        except Exception as e:
            print(f"Ошибка при импорте учителей: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка при импорте: {str(e)}")

    def on_export_teachers(self):
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Сохранить данные учителей",
                "",
                "Excel Files (*.xlsx)"
            )
            
            if file_path:
                if not file_path.endswith('.xlsx'):
                    file_path += '.xlsx'
                
                teachers = self.db.query(Teacher).all()
                export_teachers_to_excel(teachers, file_path)
                QMessageBox.information(self, "Успех", "Экспорт учителей успешно завершен")
                
        except Exception as e:
            print(f"Ошибка при экспорте учителей: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка при экспорте: {str(e)}")

    def on_edit_teacher(self):
        current_row = self.teachers_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите учителя для редактирования")
            return
            
        try:
            name_item = self.teachers_table.item(current_row, 0)
            teacher_id = name_item.data(Qt.ItemDataRole.UserRole)
            
            # Получаем список всех предметов для выбора
            available_subjects = [subject.name for subject in self.db.query(Subject).all()]
            
            teacher = self.db.query(Teacher).filter(Teacher.id == teacher_id).first()
            
            if not teacher:
                QMessageBox.warning(self, "Ошибка", "Учитель не найден в базе данных")
                return
            
            dialog = TeacherForm(self, available_subjects)
            dialog.setWindowTitle("Редактирование учителя")
            
            # Заполняем форму текущими данными
            dialog.name_edit.setText(teacher.name)
            dialog.qual_combo.setCurrentText(teacher.qualification)
            dialog.hours_spin.setValue(teacher.max_hours)
            
            # Заполняем список выбранных предметов
            current_subjects = json.loads(teacher.subjects) if teacher.subjects else []
            
            # Добавляем текущие предметы в список выбранных
            for subject in current_subjects:
                if subject in available_subjects:
                    # Удаляем из доступных и добавляем в выбранные
                    index = dialog.available_list.findItems(subject, Qt.MatchFlag.MatchExactly)
                    if index:
                        item = dialog.available_list.takeItem(dialog.available_list.row(index[0]))
                        dialog.selected_list.addItem(item.text())
            
            if dialog.exec():
                teacher_data = dialog.get_data()
                
                # Проверяем, не занято ли новое имя другим учителем
                if teacher_data['name'] != teacher.name:
                    existing_teacher = self.db.query(Teacher).filter(
                        Teacher.name == teacher_data['name']
                    ).first()
                    if existing_teacher:
                        QMessageBox.warning(self, "Ошибка", "Учитель с таким ФИО уже существует!")
                        return
                
                # Обновляем данные
                teacher.name = teacher_data['name']
                teacher.qualification = teacher_data['qualification']
                teacher.max_hours = teacher_data['max_hours']
                teacher.subjects = json.dumps(teacher_data['subjects'])
                
                try:
                    self.db.commit()
                    # Обновляем таблицу
                    self.load_teachers()
                    print("Учитель успешно обновлен")
                except Exception as e:
                    self.db.rollback()
                    print(f"Ошибка при сохранении изменений: {str(e)}")
                    QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении изменений: {str(e)}")
                
        except Exception as e:
            print(f"Ошибка при редактировании: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка при редактировании: {str(e)}")

    def on_delete_teacher(self):
        current_row = self.teachers_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите учителя для удаления")
            return
            
        try:
            # Получаем ID учителя из таблицы
            name_item = self.teachers_table.item(current_row, 0)  # Берем ячейку с именем
            if not name_item:
                QMessageBox.warning(self, "Ошибка", "Не удалось получить данные учителя")
                return
                
            teacher_id = name_item.data(Qt.ItemDataRole.UserRole)  # Получаем ID из данных ячейки
            if not teacher_id:
                QMessageBox.warning(self, "Ошибка", "Не удалось получить ID учителя")
                return
            
            # Подтверждение удаления
            reply = QMessageBox.question(
                self, 
                'Подтверждение', 
                'Вы уверены, что хотите удалить этого учителя?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # Получаем учителя из базы данных
                teacher = self.db.query(Teacher).filter(Teacher.id == teacher_id).first()
                if not teacher:
                    QMessageBox.warning(self, "Ошибка", "Учитель не найден в базе данных")
                    return
                
                # Удаляем учителя
                self.db.delete(teacher)
                self.db.commit()
                
                # Удаляем строку из таблицы
                self.teachers_table.removeRow(current_row)
                print(f"Учитель с ID {teacher_id} успешно удален")
                
        except Exception as e:
            self.db.rollback()
            print(f"Ошибка при удалении учителя: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении: {str(e)}")

    def load_subjects(self):
        try:
            subjects = self.db.query(Subject).all()
            for subject in subjects:
                self.subjects_table.add_subject(subject.to_dict())
        except Exception as e:
            print(f"Ошибка при загрузке предмето��: {str(e)}")

    def on_add_subject(self):
        try:
            # Получаем список всех предметов
            existing_subjects = [subject.name for subject in self.db.query(Subject).all()]
            
            dialog = SubjectForm(self, existing_subjects)
            if dialog.exec():
                subject_data = dialog.get_data()
                
                if not subject_data['name']:
                    QMessageBox.warning(self, "Ошибка", "Название предмета не может быть пустым!")
                    return
                
                # Создаем объект Subject
                new_subject = Subject(
                    name=subject_data['name'],
                    level=subject_data['level'],
                    hours_10_class=subject_data['hours_10_class'],
                    hours_11_class=subject_data['hours_11_class'],
                    min_qualification=subject_data['min_qualification']
                )
                new_subject.set_related_subjects(subject_data['related_subjects'])
                
                try:
                    self.db.add(new_subject)
                    self.db.commit()
                    self.db.refresh(new_subject)
                    self.subjects_table.add_subject(new_subject.to_dict())
                except Exception as e:
                    self.db.rollback()
                    print(f"Ошибка при сохранении предмета: {str(e)}")
                    QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении: {str(e)}")
                
        except Exception as e:
            print(f"Ошибка при добавлении предмета: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def on_edit_subject(self):
        current_row = self.subjects_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите предмет для редактирования")
            return
            
        try:
            name_item = self.subjects_table.item(current_row, 0)
            subject_id = name_item.data(Qt.ItemDataRole.UserRole)
            
            # Получаем список всех предметов для связанных предметов
            existing_subjects = [subject.name for subject in self.db.query(Subject).all()]
            
            subject = self.db.query(Subject).filter(Subject.id == subject_id).first()
            
            if not subject:
                QMessageBox.warning(self, "Ошибка", "Предмет не найден в базе данных")
                return
            
            dialog = SubjectForm(self, existing_subjects)
            dialog.setWindowTitle("Редактирование предмета")
            
            # Заполняем форму текущими данными
            dialog.name_edit.setText(subject.name)
            dialog.level_combo.setCurrentText(subject.level)
            dialog.hours_10_spin.setValue(subject.hours_10_class)
            dialog.hours_11_spin.setValue(subject.hours_11_class)
            dialog.qual_combo.setCurrentText(subject.min_qualification)
            
            # Заполняем связанные предметы
            related_subjects = json.loads(subject.related_subjects) if subject.related_subjects else []
            for related_subject in related_subjects:
                dialog.related_list.addItem(related_subject)
            
            if dialog.exec():
                subject_data = dialog.get_data()
                
                # Обновляем данные
                subject.name = subject_data['name']
                subject.level = subject_data['level']
                subject.hours_10_class = subject_data['hours_10_class']
                subject.hours_11_class = subject_data['hours_11_class']
                subject.min_qualification = subject_data['min_qualification']
                subject.set_related_subjects(subject_data['related_subjects'])
                
                try:
                    self.db.commit()
                    self.subjects_table.update_subject_row(current_row, subject.to_dict())
                    print("Предмет успешно обновлен")
                except Exception as e:
                    self.db.rollback()
                    print(f"Ошибка при сохранении изменений: {str(e)}")
                    QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении изменений: {str(e)}")
                
        except Exception as e:
            print(f"Ошибка ри редактировании: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка при редактировании: {str(e)}")

    def on_delete_subject(self):
        current_row = self.subjects_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите предмет для удаления")
            return
            
        try:
            name_item = self.subjects_table.item(current_row, 0)
            subject_id = name_item.data(Qt.ItemDataRole.UserRole)
            
            reply = QMessageBox.question(self, 'Подтверждение', 
                                       'Вы уверены, что хотите удалить этот предмет?',
                                       QMessageBox.StandardButton.Yes | 
                                       QMessageBox.StandardButton.No)
            
            if reply == QMessageBox.StandardButton.Yes:
                subject = self.db.query(Subject).filter(Subject.id == subject_id).first()
                if subject:
                    self.db.delete(subject)
                    self.db.commit()
                    self.subjects_table.removeRow(current_row)
                else:
                    QMessageBox.warning(self, "Ошибка", "Предмет не найден в базе данных")
                    
        except Exception as e:
            print(f"Ошибка при удалении: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении: {str(e)}")

    def closeEvent(self, event):
        if self.db:
            self.db.close()
        super().closeEvent(event)

    def create_toolbar(self):
        """Создание верхней панели инсрументов"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Общий экспорт
        export_all_btn = QPushButton("Экспорт всех данных")
        export_all_btn.clicked.connect(self.on_export_all)
        toolbar.addWidget(export_all_btn)

        # Разделитель
        toolbar.addSeparator()

        return toolbar

    def on_export_all(self):
        """Экспорт всех данных"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Сохранить все данные",
                "",
                "Excel Files (*.xlsx)"
            )
            
            if file_path:
                if not file_path.endswith('.xlsx'):
                    file_path += '.xlsx'
                
                teachers = self.db.query(Teacher).all()
                subjects = self.db.query(Subject).all()
                export_all_to_excel(teachers, subjects, file_path)
                QMessageBox.information(self, "Успех", "Экспорт всех данных успешно завершен")
                
        except Exception as e:
            print(f"Ошибка при экспорте всех данных: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка при экспорте: {str(e)}")

    def on_export_teachers(self):
        """Экспорт данных учителей"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Сохранить данные учителей",
                "",
                "Excel Files (*.xlsx)"
            )
            
            if file_path:
                if not file_path.endswith('.xlsx'):
                    file_path += '.xlsx'
                
                teachers = self.db.query(Teacher).all()
                export_teachers_to_excel(teachers, file_path)
                QMessageBox.information(self, "Успех", "Экспорт учителей успешно завершен")
                
        except Exception as e:
            print(f"Ошибка при экспорте учителей: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка при экспорте: {str(e)}")

    def on_export_subjects(self):
        """Экспорт данных предметов"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Сохранить данные предметов",
                "",
                "Excel Files (*.xlsx)"
            )
            
            if file_path:
                if not file_path.endswith('.xlsx'):
                    file_path += '.xlsx'
                
                subjects = self.db.query(Subject).all()
                export_subjects_to_excel(subjects, file_path)
                QMessageBox.information(self, "Успех", "Экспорт предметов успешно завершен")
                
        except Exception as e:
            print(f"Ошибка при экспорте предметов: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка при экспорте: {str(e)}")

    def on_import_subjects(self):
        """Импорт данных предметов из Excel"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Выберите файл Excel с данными предметов",
                "",
                "Excel Files (*.xlsx *.xls)"
            )
            
            if file_path:
                subjects_data = import_subjects_from_excel(file_path)
                for subject_data in subjects_data:
                    # Проверяем существование предмета
                    existing_subject = self.db.query(Subject).filter(
                        Subject.name == subject_data['name']
                    ).first()
                    
                    if existing_subject:
                        # Обновляем существующий предмет
                        existing_subject.level = subject_data['level']
                        existing_subject.hours_10_class = subject_data['hours_10_class']
                        existing_subject.hours_11_class = subject_data['hours_11_class']
                        existing_subject.min_qualification = subject_data['min_qualification']
                        existing_subject.set_related_subjects(subject_data['related_subjects'])
                    else:
                        # Создаем новый предмет
                        new_subject = Subject(
                            name=subject_data['name'],
                            level=subject_data['level'],
                            hours_10_class=subject_data['hours_10_class'],
                            hours_11_class=subject_data['hours_11_class'],
                            min_qualification=subject_data['min_qualification']
                        )
                        new_subject.set_related_subjects(subject_data['related_subjects'])
                        self.db.add(new_subject)
                
                try:
                    self.db.commit()
                    # Обновляем таблицу
                    self.load_subjects()
                    QMessageBox.information(self, "Успех", "Импорт предметов успешно завершен")
                except Exception as e:
                    self.db.rollback()
                    print(f"Ошибка при сохранении данных: {str(e)}")
                    QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении: {str(e)}")
                
        except Exception as e:
            print(f"Ошибка при импорте предметов: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка при импорте: {str(e)}")

    def load_subjects(self):
        """Загрузка предметов в таблицу"""
        try:
            self.subjects_table.setRowCount(0)
            subjects = self.db.query(Subject).all()
            for subject in subjects:
                self.subjects_table.add_subject(subject.to_dict())
        except Exception as e:
            print(f"Ошибка при загрузке предметов: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке предметов: {str(e)}")

    def change_theme(self, theme_name):
        if theme_name == "Тёмная":
            set_dark_theme(QApplication.instance())
        else:
            set_light_theme(QApplication.instance())

    def on_import_all(self):
        """Импорт всех данных"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Выберите файл Excel с данными",
                "",
                "Excel Files (*.xlsx *.xls)"
            )
            
            if file_path:
                # Импорт учителей
                try:
                    teachers_data = import_teachers_from_excel(file_path)
                    for teacher_data in teachers_data:
                        existing_teacher = self.db.query(Teacher).filter(
                            Teacher.name == teacher_data['name']
                        ).first()
                        
                        if existing_teacher:
                            # Обновляем существующего учителя
                            existing_teacher.qualification = teacher_data['qualification']
                            existing_teacher.max_hours = teacher_data['max_hours']
                            existing_teacher.subjects = json.dumps(teacher_data['subjects'])
                            existing_teacher.last_year_load = json.dumps(teacher_data['last_year_load'])
                        else:
                            # Создаем нового учителя
                            new_teacher = Teacher(
                                name=teacher_data['name'],
                                qualification=teacher_data['qualification'],
                                max_hours=teacher_data['max_hours'],
                                subjects=json.dumps(teacher_data['subjects']),
                                last_year_load=json.dumps(teacher_data['last_year_load']),
                                is_active=True
                            )
                            self.db.add(new_teacher)
                except Exception as e:
                    print(f"Ошибка при импорте учителей: {str(e)}")
                
                # Импорт предметов
                try:
                    subjects_data = import_subjects_from_excel(file_path)
                    for subject_data in subjects_data:
                        existing_subject = self.db.query(Subject).filter(
                            Subject.name == subject_data['name']
                        ).first()
                        
                        if existing_subject:
                            # Обновляем существующий предмет
                            existing_subject.level = subject_data['level']
                            existing_subject.hours_10_class = subject_data['hours_10_class']
                            existing_subject.hours_11_class = subject_data['hours_11_class']
                            existing_subject.min_qualification = subject_data['min_qualification']
                            existing_subject.set_related_subjects(subject_data['related_subjects'])
                        else:
                            # Создаем новый предмет
                            new_subject = Subject(
                                name=subject_data['name'],
                                level=subject_data['level'],
                                hours_10_class=subject_data['hours_10_class'],
                                hours_11_class=subject_data['hours_11_class'],
                                min_qualification=subject_data['min_qualification']
                            )
                            new_subject.set_related_subjects(subject_data['related_subjects'])
                            self.db.add(new_subject)
                except Exception as e:
                    print(f"Ошибка при импорте предметов: {str(e)}")
                
                try:
                    self.db.commit()
                    self.load_teachers()
                    self.load_subjects()
                    QMessageBox.information(self, "Успех", "Импорт данных успешно завершен")
                except Exception as e:
                    self.db.rollback()
                    print(f"Ошибка при сохранении данных: {str(e)}")
                    QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении: {str(e)}")
        
        except Exception as e:
            print(f"Ошибка при импорте данных: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка при импорте: {str(e)}")