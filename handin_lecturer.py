import os
import re
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QMainWindow, QDialog

from const import DIR_ROOT
from ui.impl.create_new_module_dialog import Ui_Dialog as Ui_Dialog_Create_New_Module
from ui.impl.create_weekly_assignment_dialog import Ui_Dialog as Ui_Dialog_Create_Weekly_Assignment
from ui.impl.handin_lecturer_main_window import Ui_MainWindow as Ui_MainWindow


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
        path = "/module/" + module_code + "/"
        module_dir = DIR_ROOT + path
        self.create_files(module_dir)
        self.update_definitions_file(module_dir)
        self.update_params_file(module_dir)

    @staticmethod
    def update_definitions_file(module_dir):
        # TODO: update definitions file
        pass

    @staticmethod
    def create_files(module_dir):
        """create class-list and definitions file"""
        if not os.path.exists(module_dir):
            os.makedirs(module_dir)
        class_list_path = os.path.join(module_dir, "class-list")
        if not os.path.exists(class_list_path):
            with open(class_list_path, "w"):
                pass
        definitions_path = os.path.join(module_dir, "definitions")
        if not os.path.exists(definitions_path):
            with open(definitions_path, "w"):
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
        path = "/module/" + module_code + "/"
        module_dir = DIR_ROOT + path
        self.create_week_directory(module_dir, week_number)

    @staticmethod
    def create_week_directory(module_dir, week_number):
        if not os.path.exists(module_dir + week_number):
            print(module_dir + week_number)
            os.mkdir(module_dir + week_number)
        params_path = os.path.join(module_dir + week_number, "params")
        if not os.path.exists(params_path):
            with open(params_path, "w"):
                pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
