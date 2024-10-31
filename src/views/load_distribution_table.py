import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.teacher import Teacher
from models.subject import Subject
from models.teacher_load import TeacherLoad, LevelType

from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QSpinBox, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
import json

class LoadDistributionTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.warning_color = QColor(255, 200, 200)  # Светло-красный для предупреждений
        self.conflict_color = QColor(255, 165, 0)   # Оранжевый для конфликтов
        
    def setup_ui(self):
        # Настройка таблицы
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels([
            "Предмет", "Уровень", "Класс", "Часы", "Учитель"
        ])
        
        # Настройка внешнего вида
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        # Растягиваем заголовки
        header = self.horizontalHeader()
        for i in range(self.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
    
    def add_load_row(self, subject_name="", level="Базовый", grade=10, group=1, hours=0, teacher_name=""):
        row = self.rowCount()
        self.insertRow(row)
        
        # Добавляем информацию о группе в отображение
        subject_text = f"{subject_name} (группа {group})"
        
        # Предмет (комбобокс)
        subject_combo = QComboBox()
        subjects = self.parent().main_window.db.query(Subject).all()
        subject_combo.addItems([f"{s.name} (группа {i+1})" 
                              for s in subjects 
                              for i in range(self.get_groups_count(s, grade, level))])
        if subject_text:
            subject_combo.setCurrentText(subject_text)
        self.setCellWidget(row, 0, subject_combo)
        
        # При изменении предмета обновляем часы и список учителей
        subject_combo.currentTextChanged.connect(lambda text: self.on_subject_changed(row))
        
        # Уровень (комбобокс)
        level_combo = QComboBox()
        level_combo.addItems([level.value for level in LevelType])
        level_combo.setCurrentText(level)
        level_combo.currentTextChanged.connect(lambda text: self.update_available_teachers(row))
        self.setCellWidget(row, 1, level_combo)
        
        # Класс (комбобокс)
        grade_combo = QComboBox()
        grade_combo.addItems(["10", "11"])
        grade_combo.setCurrentText(str(grade))
        grade_combo.currentTextChanged.connect(lambda text: self.on_subject_changed(row))
        self.setCellWidget(row, 2, grade_combo)
        
        # Часы (спинбокс)
        hours_spin = QSpinBox()
        hours_spin.setRange(0, 12)
        hours_spin.setValue(hours)
        hours_spin.valueChanged.connect(lambda value: self.check_teacher_load(row))
        self.setCellWidget(row, 3, hours_spin)
        
        # Учитель (комбобокс)
        teacher_combo = QComboBox()
        self.setCellWidget(row, 4, teacher_combo)
        self.update_available_teachers(row)
        if teacher_name:
            teacher_combo.setCurrentText(teacher_name)
        teacher_combo.currentTextChanged.connect(lambda text: self.check_teacher_load(row))
        
        # Проверяем конфликты после добавления строки
        self.check_conflicts()

    def on_subject_changed(self, row):
        """Обработчик изменения предмета"""
        subject_combo = self.cellWidget(row, 0)
        if subject_combo:
            self.update_hours_for_subject(row, subject_combo.currentText())
            self.update_available_teachers(row)
            self.check_conflicts()

    def update_available_teachers(self, row):
        """Обновление списка доступных учителей для предмета"""
        try:
            subject_name = self.cellWidget(row, 0).currentText()
            level = self.cellWidget(row, 1).currentText()
            
            # Получаем всех учителей
            all_teachers = self.parent().main_window.db.query(Teacher).all()
            
            # Фильтруем учителей
            available_teachers = []
            for teacher in all_teachers:
                if self.can_teach_subject(teacher, subject_name, level):
                    available_teachers.append(teacher)
            
            # Обновляем комбобокс
            teacher_combo = self.cellWidget(row, 4)
            current_teacher = teacher_combo.currentText()
            
            teacher_combo.clear()
            teacher_combo.addItems([t.name for t in available_teachers])
            
            # Восстанавливаем выбранного учителя, если он доступен
            if current_teacher in [t.name for t in available_teachers]:
                teacher_combo.setCurrentText(current_teacher)
                
        except Exception as e:
            print(f"Ошибка при обновлении списка учителей: {str(e)}")

    def can_teach_subject(self, teacher, subject_name, level):
        """Проверка может ли учитель вести предмет"""
        try:
            teacher_subjects = json.loads(teacher.subjects)
            
            # Проверяем, есть ли предмет в списке предметов учителя
            if subject_name not in teacher_subjects:
                return False
            
            # Для углубленного уровня нужна высшая или первая категория
            if level == LevelType.ADVANCED.value:
                return teacher.qualification in ['Высшая категория', 'Первая категория']
                
            return True
            
        except Exception as e:
            print(f"Ошибка при проверке возможности преподавания: {str(e)}")
            return False

    def check_teacher_load(self, changed_row):
        """Проверка нагрузки учителя"""
        try:
            teacher_combo = self.cellWidget(changed_row, 4)
            teacher_name = teacher_combo.currentText()
            
            if not teacher_name:
                return
                
            teacher = self.parent().main_window.db.query(Teacher).filter(
                Teacher.name == teacher_name
            ).first()
            
            if not teacher:
                return
                
            # Подсчитываем общую нагрузку учителя
            total_hours = 0
            for row in range(self.rowCount()):
                if self.cellWidget(row, 4).currentText() == teacher_name:
                    total_hours += self.cellWidget(row, 3).value()
            
            # Проверяем превышение максимальной нагрузки
            if total_hours > teacher.max_hours:
                self.highlight_row(changed_row, self.warning_color)
                QMessageBox.warning(
                    self,
                    "Превышение нагрузки",
                    f"Общая нагрузка учителя {teacher_name} "
                    f"превышает максимальную ({total_hours} > {teacher.max_hours})"
                )
            else:
                self.highlight_row(changed_row, None)
                
        except Exception as e:
            print(f"Ошибк при проверке нагрузки: {str(e)}")

    def check_conflicts(self):
        """Проверка конфликтов в распределении"""
        try:
            conflicts = []
            
            # Проверяем каждую пару строк
            for i in range(self.rowCount()):
                for j in range(i + 1, self.rowCount()):
                    # Получаем данные из строк
                    subject1 = self.cellWidget(i, 0).currentText()
                    subject2 = self.cellWidget(j, 0).currentText()
                    teacher1 = self.cellWidget(i, 4).currentText()
                    teacher2 = self.cellWidget(j, 4).currentText()
                    grade1 = self.cellWidget(i, 2).currentText()
                    grade2 = self.cellWidget(j, 2).currentText()
                    
                    # Проверяем конфликты
                    if (subject1 == subject2 and grade1 == grade2 and 
                        teacher1 != teacher2):
                        conflicts.append((i, j, "Один предмет ведут разные учителя"))
                    
                    # Проверяем связанные предметы
                    subject1_obj = self.parent().main_window.db.query(Subject).filter(
                        Subject.name == subject1
                    ).first()
                    
                    if subject1_obj and subject1_obj.related_subjects:
                        related = json.loads(subject1_obj.related_subjects)
                        if subject2 in related and teacher1 != teacher2:
                            conflicts.append((i, j, "Связанные предметы ведут разные учителя"))
            
            # Подсвечиваем конфликты
            for row1, row2, message in conflicts:
                self.highlight_row(row1, self.conflict_color)
                self.highlight_row(row2, self.conflict_color)
                QMessageBox.warning(self, "Конфликт", message)
                
        except Exception as e:
            print(f"Ошибка при проверке конфликтов: {str(e)}")

    def highlight_row(self, row, color):
        """Подсветка строки определенным цветом"""
        for col in range(self.columnCount()):
            widget = self.cellWidget(row, col)
            if widget:
                if color:
                    widget.setStyleSheet(f"background-color: {color.name()}")
                else:
                    widget.setStyleSheet("")

    def update_hours_for_subject(self, row, subject_name):
        """Обновление часов при изменении предмета или класса"""
        try:
            subject = self.parent().main_window.db.query(Subject).filter(
                Subject.name == subject_name
            ).first()
            
            if subject:
                grade_combo = self.cellWidget(row, 2)
                if grade_combo:
                    grade = int(grade_combo.currentText())
                    hours = subject.hours_10_class if grade == 10 else subject.hours_11_class
                    hours_spin = self.cellWidget(row, 3)
                    if hours_spin:
                        hours_spin.setValue(hours)
        except Exception as e:
            print(f"Ошибка при обновлении часов: {str(e)}")