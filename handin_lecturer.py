import os
import re
import sys
import yaml

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate, QRegExp, QDateTime
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox, QLineEdit, QGroupBox

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
        self.dateTimeEdit_startDay.setDisplayFormat("dd/MM/yyyy HH:mm")
        self.dateTimeEdit_endDay.setDisplayFormat("dd/MM/yyyy HH:mm")
        self.dateTimeEdit_cutoffDay.setDisplayFormat("dd/MM/yyyy HH:mm")
        self.dateTimeEdit_startDay.setDateTime(QDateTime.currentDateTime())
        self.dateTimeEdit_endDay.setDateTime(QDateTime.currentDateTime())
        self.dateTimeEdit_cutoffDay.setDateTime(QDateTime.currentDateTime())
        self.lineEdit_penaltyPerDay.setPlaceholderText('0')
        # only allow Integers for PenaltyPerDay and totalAttempts
        regex = QRegExp("\\d+")
        self.lineEdit_penaltyPerDay.setValidator(QRegExpValidator(regex))
        self.lineEdit_totalAttempts.setValidator(QRegExpValidator(regex))
        self.lineEdit_attendance_marks.setValidator(QRegExpValidator(regex))
        self.lineEdit_compilation_marks.setValidator(QRegExpValidator(regex))
        self.lineEdit_test1_marks.setValidator(QRegExpValidator(regex))
        self.lineEdit_test2_marks.setValidator(QRegExpValidator(regex))
        self.lineEdit_test3_marks.setValidator(QRegExpValidator(regex))
        self.lineEdit_test4_marks.setValidator(QRegExpValidator(regex))
        self.accepted.connect(lambda: self.create_weekly_assignment())
        self.buttonBox.setEnabled(False)
        self.comboBox_moduleCode.editTextChanged.connect(self.disable_buttonbox)
        # register listeners for all line edits
        for line_edit in self.findChildren(QLineEdit):
            line_edit.textChanged.connect(self.disable_buttonbox)
        # register listeners for all group boxes
        for group_box in self.findChildren(QGroupBox):
            group_box.toggled.connect(self.disable_buttonbox)
            group_box.toggled.connect(self.update_total_marks)
            group_box.toggled.connect(self.disable_groupbox)
        self.lineEdit_attendance_marks.textChanged.connect(self.update_total_marks)
        self.lineEdit_compilation_marks.textChanged.connect(self.update_total_marks)
        self.lineEdit_test1_marks.textChanged.connect(self.update_total_marks)
        self.lineEdit_test2_marks.textChanged.connect(self.update_total_marks)
        self.lineEdit_test3_marks.textChanged.connect(self.update_total_marks)
        self.lineEdit_test4_marks.textChanged.connect(self.update_total_marks)
        # set up initial available module codes
        self.comboBox_moduleCode.addItems(self.get_module_codes())
        # set up week numbers
        self.comboBox_weekNumber.addItems(["w01", "w02", "w03", "w04", "w05", "w06",
                                           "w07", "w08", "w09", "w10", "w11", "w12", "w13"])
        self.groupBox_customTest1.setCheckable(False)
        self.groupBox_customTest1.setChecked(True)
        self.checkBox_test1_inputDataFile.stateChanged.connect(self.add_input_data_file)
        self.checkBox_test2_inputDataFile.stateChanged.connect(self.add_input_data_file)
        self.checkBox_test3_inputDataFile.stateChanged.connect(self.add_input_data_file)
        self.checkBox_test4_inputDataFile.stateChanged.connect(self.add_input_data_file)

    @staticmethod
    def get_module_codes() -> list:
        path = DIR_ROOT + "/module/"
        return [name for name in os.listdir(path)]

    def add_input_data_file(self):
        """add input data file -- signal"""
        if self.checkBox_test1_inputDataFile.isChecked():
            dialog = QtWidgets.QFileDialog()
            dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
            filename, file_type = QtWidgets.QFileDialog.getOpenFileName(
                self, "Choose file", "./", "All Files (*)")
            self.label_test1_inputDataFile.setText(filename)
        else:
            self.label_test1_inputDataFile.setText("")

        if self.checkBox_test2_inputDataFile.isChecked():
            dialog = QtWidgets.QFileDialog()
            dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
            filename, file_type = QtWidgets.QFileDialog.getOpenFileName(
                self, "Choose file", "./", "All Files (*)")
            self.label_test2_inputDataFile.setText(filename)
        else:
            self.label_test2_inputDataFile.setText("")

        if self.checkBox_test3_inputDataFile.isChecked():
            dialog = QtWidgets.QFileDialog()
            dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
            filename, file_type = QtWidgets.QFileDialog.getOpenFileName(
                self, "Choose file", "./", "All Files (*)")
            self.label_test3_inputDataFile.setText(filename)
        else:
            self.label_test3_inputDataFile.setText("")

        if self.checkBox_test4_inputDataFile.isChecked():
            dialog = QtWidgets.QFileDialog()
            dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
            filename, file_type = QtWidgets.QFileDialog.getOpenFileName(
                self, "Choose file", "./", "All Files (*)")
            self.label_test4_inputDataFile.setText(filename)
        else:
            self.label_test4_inputDataFile.setText("")

    def disable_buttonbox(self):
        """disable button box -- signal"""
        self.buttonBox.setEnabled(True)
        line_edits: list = [le for le in self.findChildren(QLineEdit)]
        for line_edit in line_edits:
            if line_edit.isEnabled():
                if not len(line_edit.text()) > 0:
                    self.buttonBox.setEnabled(False)
                    return

    def update_total_marks(self):
        """update total marks -- signal"""
        total_marks: int = self.get_total_marks()
        self.label_totalMarks.setText(str(total_marks))

    def disable_groupbox(self):
        """disable group box -- signal,"""
        if not self.groupBox_customTest2.isChecked():
            self.groupBox_customTest3.setChecked(False)
            self.groupBox_customTest4.setChecked(False)
        if not self.groupBox_customTest3.isChecked():
            self.groupBox_customTest4.setChecked(False)

    def get_total_marks(self) -> int:
        attendance = int(self.lineEdit_attendance_marks.text()) if len(self.lineEdit_attendance_marks.text()) > 0 and self.groupBox_attendance.isChecked() else 0
        compilation = int(self.lineEdit_compilation_marks.text()) if len(self.lineEdit_compilation_marks.text()) > 0 and self.groupBox_compilation.isChecked() else 0
        test1 = int(self.lineEdit_test1_marks.text()) if len(self.lineEdit_test1_marks.text()) > 0 else 0
        test2 = int(self.lineEdit_test2_marks.text()) if len(self.lineEdit_test2_marks.text()) > 0 and self.groupBox_customTest2.isChecked() else 0
        test3 = int(self.lineEdit_test3_marks.text()) if len(self.lineEdit_test3_marks.text()) > 0 and self.groupBox_customTest3.isChecked() else 0
        test4 = int(self.lineEdit_test4_marks.text()) if len(self.lineEdit_test4_marks.text()) > 0 and self.groupBox_customTest4.isChecked() else 0
        return attendance + compilation + test1 + test2 + test3 + test4

    def create_weekly_assignment(self):
        module_code = self.comboBox_moduleCode.currentText().strip()
        week_number = self.comboBox_weekNumber.currentText().strip()
        start_day = self.dateTimeEdit_startDay.text().strip()
        end_day = self.dateTimeEdit_startDay.text().strip()
        cutoff_day = self.dateTimeEdit_cutoffDay.text().strip()
        penalty_per_day = int(self.lineEdit_penaltyPerDay.text().strip())
        total_attempts = int(self.lineEdit_totalAttempts.text().strip())
        collection_filename = self.lineEdit_collectFilename.text().strip()
        tests = {}
        if self.groupBox_attendance.isChecked():
            tag = self.lineEdit_attendance_tag.text().strip()
            marks = int(self.lineEdit_attendance_marks.text().strip())
            tests["attendance"] = {"tag": tag, "marks": marks}
        if self.groupBox_compilation.isChecked():
            tag = self.lineEdit_compilation_tag.text().strip()
            marks = int(self.lineEdit_compilation_marks.text().strip())
            command = self.lineEdit_compilation_command.text().strip()
            tests["compilation"] = {"tag": tag, "marks": marks, "command": command}
        tag = self.lineEdit_test1_tag.text().strip()
        marks = int(self.lineEdit_test1_marks.text().strip())
        command = self.lineEdit_test1_command.text().strip()
        inputDataFile = self.label_test1_inputDataFile.text().strip()
        tests["test1"] = {"tag": tag, "marks": marks, "command": command, "inputDataFile": inputDataFile}
        if self.groupBox_customTest2.isChecked():
            tag = self.lineEdit_test2_tag.text().strip()
            marks = int(self.lineEdit_test2_marks.text().strip())
            command = self.lineEdit_test2_command.text().strip()
            inputDataFile = self.label_test2_inputDataFile.text().strip()
            tests["test2"] = {"tag": tag, "marks": marks, "command": command, "inputDataFile": inputDataFile}
        if self.groupBox_customTest3.isChecked():
            tag = self.lineEdit_test3_tag.text().strip()
            marks = int(self.lineEdit_test3_marks.text().strip())
            command = self.lineEdit_test3_command.text().strip()
            inputDataFile = self.label_test3_inputDataFile.text().strip()
            tests["test3"] = {"tag": tag, "marks": marks, "command": command, "inputDataFile": inputDataFile}
        if self.groupBox_customTest4.isChecked():
            tag = self.lineEdit_test4_tag.text().strip()
            marks = int(self.lineEdit_test4_marks.text().strip())
            command = self.lineEdit_test4_command.text().strip()
            inputDataFile = self.label_test4_inputDataFile.text().strip()
            tests["test4"] = {"tag": tag, "marks": marks, "command": command, "inputDataFile": inputDataFile}

        if not check_if_week_exists(module_code=module_code, week_number=week_number):
            path = "/module/" + module_code + "/"
            module_dir = DIR_ROOT + path
            self.create_week_directory(module_dir, week_number)
            self.update_params_file(
                moduleCode=module_code, weekNumber=week_number, startDay=start_day,
                endDay=end_day, cutoffDay=cutoff_day, penaltyPerDay=penalty_per_day,
                totalAttempts=total_attempts, collectionFilename=collection_filename, tests=tests)
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
