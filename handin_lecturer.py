import re
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QMainWindow, QDialog

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
        # TODO: Create module here ... DB or File?
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

    def disable_buttonbox(self):
        if len(self.lineEdit_penaltyPerDay.text()) > 0 \
                and len(self.comboBox_moduleCode.currentText()) > 0:
            self.buttonBox.setEnabled(True)
        else:
            self.buttonBox.setEnabled(False)

    def create_weekly_assignment(self):
        # TODO: Create weekly assignment here ... DB or File?
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
