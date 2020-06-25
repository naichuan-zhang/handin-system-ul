import os
import re
import sys
import yaml

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox

from const import DIR_ROOT
from ui.impl.create_new_module_dialog import Ui_Dialog as Ui_Dialog_Create_New_Module
from ui.impl.create_weekly_assignment_dialog import Ui_Dialog as Ui_Dialog_Create_Weekly_Assignment
from ui.impl.handin_lecturer_main_window import Ui_MainWindow as Ui_MainWindow


def check_if_module_exists(module_code: str) -> bool:
    path = DIR_ROOT + "/module/"
    if os.path.exists(path):
        modules = [name.lower() for name in os.listdir(path)]
        if module_code.lower() in modules:
            return True
    return False


def check_if_week_exists(module_code: str, week_number: str) -> bool:
    path = DIR_ROOT + "/module/" + module_code + "/"
    if os.path.exists(path):
        weeks = [name for name in os.listdir(path)]
        if week_number in weeks:
            return True
    return False


def create_message_box(text):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText(text)
    msgBox.setWindowTitle("Message")
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(lambda: self.create_new_module())
        self.pushButton_2.clicked.connect(lambda: self.manage_student_marks())
        self.pushButton_3.clicked.connect(lambda: self.create_weekly_assignment())

    def create_new_module(self):
        dialog = CreateNewModuleDialog(self)
        dialog.show()

    def manage_student_marks(self):
        # TODO: manage student marks
        pass

    def create_weekly_assignment(self):
        dialog = CreateWeeklyAssignmentDialog(self)
        dialog.show()


def isMatchRegex(regex: str, text: str) -> bool:
    return bool(re.match(regex, text))


class CreateNewModuleDialog(QDialog, Ui_Dialog_Create_New_Module):
    def __init__(self, parent=None):
        super(CreateNewModuleDialog, self).__init__(parent)
        self.setupUi(self)
        self.dateEdit_startSemester.setDate(QDate.currentDate())
        self.dateEdit_endSemester.setDate(QDate.currentDate())
        # Academic Year format: 2019/2020SEM1
        self.regex = "\\d{4}/\\d{4}SEM[1,2]"
        self.lineEdit_academicYear.setPlaceholderText('2019/2020SEM1')
        self.accepted.connect(lambda: self.create_module())
        self.buttonBox.setEnabled(False)
        self.lineEdit_academicYear.textChanged.connect(self.disable_buttonbox)

    def disable_buttonbox(self):
        if len(self.lineEdit_academicYear.text()) > 0 and \
                isMatchRegex(regex=self.regex, text=self.lineEdit_academicYear.text()):
            self.buttonBox.setEnabled(True)
        else:
            self.buttonBox.setEnabled(False)

    def create_module(self):
        module_code: str = self.lineEdit.text().strip()
        academic_year: str = self.lineEdit_academicYear.text().strip()
        start_semester: str = self.dateEdit_startSemester.text().strip()
        end_semester: str = self.dateEdit_endSemester.text().strip()

        if not check_if_module_exists(module_code=module_code):
            path = "/module/" + module_code + "/"
            module_dir = DIR_ROOT + path
            self.create_files(module_dir)
            self.update_definitions_file(
                academicYear=academic_year, startSemester=start_semester, endSemester=end_semester)
        else:
            create_message_box(f"Module {module_code} already exists!")

    def update_definitions_file(self, **kwargs):
        # TODO: any more defs to add??
        with open(self.definitions_path, 'a') as file:
            yaml.dump(kwargs, file, default_flow_style=False)

    def create_files(self, module_dir):
        """create class-list and definitions file"""
        if not os.path.exists(module_dir):
            os.makedirs(module_dir)
        self.class_list_path = os.path.join(module_dir, "class-list")
        if not os.path.exists(self.class_list_path):
            with open(self.class_list_path, "w"):
                pass
        self.definitions_path = os.path.join(module_dir, "definitions.yaml")
        if not os.path.exists(self.definitions_path):
            with open(self.definitions_path, "w"):
                pass


class CreateWeeklyAssignmentDialog(QDialog, Ui_Dialog_Create_Weekly_Assignment):
    def __init__(self, parent=None):
        super(CreateWeeklyAssignmentDialog, self).__init__(parent)
        self.setupUi(self)
        self.dateTimeEdit_startDay.setDate(QDate.currentDate())
        self.dateTimeEdit_endDay.setDate(QDate.currentDate())
        self.dateTimeEdit_cutoffDay.setDate(QDate.currentDate())
        self.lineEdit_penaltyPerDay.setPlaceholderText('0')
        # only allow Integers for PenaltyPerDay
        regex = QRegExp("\\d+")
        self.lineEdit_penaltyPerDay.setValidator(QRegExpValidator(regex))
        self.accepted.connect(lambda: self.create_weekly_assignment())
        self.buttonBox.setEnabled(False)
        self.comboBox_moduleCode.editTextChanged.connect(self.disable_buttonbox)
        self.lineEdit_penaltyPerDay.textChanged.connect(self.disable_buttonbox)
        # set up initial available module codes
        self.comboBox_moduleCode.addItems(self.get_module_codes())
        # set up week numbers
        self.comboBox_weekNumber.addItems(["w01", "w02", "w03", "w04", "w05", "w06",
                                           "w07", "w08", "w09", "w10", "w11", "w12", "w13"])

    @staticmethod
    def get_module_codes() -> list:
        path = DIR_ROOT + "/module/"
        return [name for name in os.listdir(path)]

    def disable_buttonbox(self):
        if len(self.lineEdit_penaltyPerDay.text()) > 0 \
                and len(self.comboBox_moduleCode.currentText()) > 0:
            self.buttonBox.setEnabled(True)
        else:
            self.buttonBox.setEnabled(False)

    def create_weekly_assignment(self):
        module_code = self.comboBox_moduleCode.currentText().strip()
        week_number = self.comboBox_weekNumber.currentText().strip()
        start_day = self.dateTimeEdit_startDay.text().strip()
        end_day = self.dateTimeEdit_startDay.text().strip()
        cutoff_day = self.dateTimeEdit_cutoffDay.text().strip()
        penalty_per_day = int(self.lineEdit_penaltyPerDay.text())

        if not check_if_week_exists(module_code=module_code, week_number=week_number):
            path = "/module/" + module_code + "/"
            module_dir = DIR_ROOT + path
            self.create_week_directory(module_dir, week_number)
            self.update_params_file(
                moduleCode=module_code, weekNumber=week_number, startDay=start_day,
                endDay=end_day, cutoffDay=cutoff_day, penaltyPerDay=penalty_per_day)
        else:
            create_message_box(f"{week_number} for module {module_code} already exists!")

    def create_week_directory(self, module_dir, week_number):
        if not os.path.exists(module_dir + week_number):
            print(module_dir + week_number)
            os.mkdir(module_dir + week_number)
        self.params_path = os.path.join(module_dir + week_number, "params.yaml")
        if not os.path.exists(self.params_path):
            with open(self.params_path, "w"):
                pass

    def update_params_file(self, **kwargs):
        with open(self.params_path, 'a') as file:
            # TODO: any more params to add??
            yaml.dump(kwargs, file, default_flow_style=False)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())