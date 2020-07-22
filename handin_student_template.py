# -*- coding: utf-8 -*-
import socket
import sys
from datetime import datetime

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QMainWindow

# ****** DYNAMIC CONFIGS ****** #
HOST = "{}"
PORT = "{}"
STUDENT_NAME = "{}"
STUDENT_ID = "{}"
MODULE_CODE = "{}"
MODULE_NAME = "{}"
# ****** DYNAMIC CONFIGS ****** #


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 700)
        MainWindow.setMinimumSize(QtCore.QSize(800, 700))
        MainWindow.setMaximumSize(QtCore.QSize(800, 700))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 40, 100, 25))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 100, 25))
        self.label_2.setObjectName("label_2")
        self.lineEdit_moduleCode = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_moduleCode.setGeometry(QtCore.QRect(140, 40, 120, 25))
        self.lineEdit_moduleCode.setObjectName("lineEdit_moduleCode")
        self.lineEdit_moduleName = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_moduleName.setGeometry(QtCore.QRect(140, 80, 220, 25))
        self.lineEdit_moduleName.setObjectName("lineEdit_moduleName")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(400, 40, 100, 25))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(400, 80, 110, 25))
        self.label_4.setObjectName("label_4")
        self.lineEdit_studentID = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_studentID.setGeometry(QtCore.QRect(520, 40, 120, 25))
        self.lineEdit_studentID.setObjectName("lineEdit_studentID")
        self.lineEdit_studentName = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_studentName.setGeometry(QtCore.QRect(520, 80, 220, 25))
        self.lineEdit_studentName.setText("")
        self.lineEdit_studentName.setObjectName("lineEdit_studentName")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(20, 120, 750, 270))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.textEdit_showFileContent = QtWidgets.QTextEdit(self.frame)
        self.textEdit_showFileContent.setGeometry(QtCore.QRect(20, 50, 700, 210))
        self.textEdit_showFileContent.setObjectName("textEdit_showFileContent")
        self.layoutWidget = QtWidgets.QWidget(self.frame)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 10, 701, 31))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(16)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.lineEdit_chooseFile = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_chooseFile.setObjectName("lineEdit_chooseFile")
        self.horizontalLayout.addWidget(self.lineEdit_chooseFile)
        self.pushButton_browse = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_browse.setObjectName("pushButton_browse")
        self.horizontalLayout.addWidget(self.pushButton_browse)
        self.pushButton_handin = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_handin.setGeometry(QtCore.QRect(640, 420, 93, 28))
        self.pushButton_handin.setObjectName("pushButton_handin")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(20, 430, 81, 21))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(402, 420, 111, 28))
        self.label_7.setObjectName("label_7")
        self.comboBox_weekNumber = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_weekNumber.setGeometry(QtCore.QRect(520, 420, 93, 28))
        self.comboBox_weekNumber.setObjectName("comboBox_weekNumber")
        self.textEdit_Output = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_Output.setGeometry(QtCore.QRect(20, 470, 750, 200))
        self.textEdit_Output.setStyleSheet("color: rgb(102, 102, 255)")
        self.textEdit_Output.setObjectName("textEdit_Output")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Handin System (Student)"))
        self.label.setText(_translate("MainWindow", "Module Code:"))
        self.label_2.setText(_translate("MainWindow", "Module Name:"))
        self.label_3.setText(_translate("MainWindow", "Student ID:"))
        self.label_4.setText(_translate("MainWindow", "Student Name:"))
        self.label_5.setText(_translate("MainWindow", "File Name:"))
        self.pushButton_browse.setText(_translate("MainWindow", "Browse"))
        self.pushButton_handin.setText(_translate("MainWindow", "Handin"))
        self.label_6.setText(_translate("MainWindow", "Output"))
        self.label_7.setText(_translate("MainWindow", "Week Number:"))
        self.textEdit_Output.setHtml(_translate("MainWindow",
                                                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                "<html><head><meta name=\"qrichtext\" content=\"1\" />"
                                                "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))


class HandinMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(HandinMainWindow, self).__init__()
        self.setupUi(self)
        self.pushButton_browse.clicked.connect(self.browse)
        self.pushButton_handin.clicked.connect(self.check_handin)
        self.lineEdit_moduleCode.setText(MODULE_CODE)
        self.lineEdit_moduleCode.setEnabled(False)
        self.lineEdit_moduleName.setText(MODULE_NAME)
        self.lineEdit_moduleName.setEnabled(False)
        self.lineEdit_studentID.setText(STUDENT_ID)
        self.lineEdit_studentID.setEnabled(False)
        self.lineEdit_studentName.setText(STUDENT_NAME)
        self.lineEdit_studentName.setEnabled(False)
        self.comboBox_weekNumber.addItems(["w01", "w02", "w03", "w04", "w05", "w06", "w07",
                                           "w08", "w09", "w10", "w11", "w12", "w13"])
        self.textEdit_Output.setReadOnly(True)
        self.textEdit_showFileContent.setReadOnly(True)
        self.lineEdit_chooseFile.setReadOnly(True)
        self.lineEdit_chooseFile.textChanged.connect(self.disable_handin)
        self.pushButton_handin.setEnabled(False)

    def disable_handin(self):
        if len(self.lineEdit_chooseFile.text()) > 0:
            self.pushButton_handin.setEnabled(True)
        else:
            self.pushButton_handin.setEnabled(False)

    def browse(self):
        filename, file_type = QtWidgets.QFileDialog.getOpenFileName(
            self, "Choose file", "./", "All Files (*);;C File (*.c);;Cpp File (*.cpp);;"
                                       "Java File (*.java);;Python File (*.py);;Text File (*.txt)")
        self.lineEdit_chooseFile.setText(filename)
        try:
            with open(filename, 'rb') as f:
                content = f.read().decode('utf-8')
        except Exception as e:
            content = ""
            print(e)
        self.textEdit_showFileContent.setText(content)
        self.submit_filepath = filename

    def check_handin(self):
        global initVars
        try:
            s = socket.socket()
            s.connect((HOST, int(PORT)))
            # check if module exists
            if module_exists(MODULE_CODE, s):
                # check if week number valid
                week_number = self.comboBox_weekNumber.currentText()
                if week_number_valid(MODULE_CODE, week_number, s):
                    self.output("Submitting code to %s::%s" % (MODULE_CODE, week_number))
                    # check student id authentication
                    if check_student_authentication(MODULE_CODE, STUDENT_ID, s):
                        self.output("Student ID: %s has been authenticated" % STUDENT_ID)
                        # create a vars.yaml file to store info of a specific student
                        result = create_vars_file(MODULE_CODE, STUDENT_ID, week_number, s)
                        if result == "Success":
                            print("Vars file has been created ...")
                            initVars = True
                        elif result == "Failed":
                            print("Vars file already exists")
                            initVars = False
                        self.run_handin(week_number, s, initVars)
                    else:
                        self.output("Student ID: %s not authenticated" % STUDENT_ID, flag="ERROR")
                else:
                    self.output("%s not valid for %s" % (week_number, MODULE_CODE), flag="ERROR")
            else:
                self.output("%s not exist!" % MODULE_CODE, flag="ERROR")
        except Exception as e:
            self.output(str(e), flag="ERROR")

    def run_handin(self, week_number, s: socket.socket, init_vars: bool):
        # initialize vars.yaml file
        if init_vars:
            init_vars_file(MODULE_CODE, STUDENT_ID, week_number, s)
        # get attempts left
        attempts_left: int = check_attempts_left(MODULE_CODE, STUDENT_ID, week_number, s)
        late_penalty_msg = check_late_penalty(MODULE_CODE, week_number, s)
        penalty: int = -1
        if isinstance(late_penalty_msg, str):
            self.output(late_penalty_msg, flag="ERROR")
        if isinstance(late_penalty_msg, int):
            self.output("Penalty applied : " + str(late_penalty_msg))
            penalty = late_penalty_msg
        if penalty != -1:
            # check if the filename matches required filename
            filename = QFileInfo(self.submit_filepath).fileName()
            file_suffix = QFileInfo(self.submit_filepath).suffix()
            msg = check_collection_filename(filename, MODULE_CODE, week_number, s)
            if msg == "True":
                # copy file to server side
                send_file_to_server(self.submit_filepath, MODULE_CODE, week_number, STUDENT_ID, s)
                # get exec result output
                print('send file to server finished ...')
                result = get_exec_result(MODULE_CODE, week_number, STUDENT_ID, s, file_suffix, str(penalty))
                self.output(result)
            else:
                self.output(msg, "ERROR")

    def output(self, text: str, flag: str = "INFO"):
        df = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self.textEdit_Output.append("---" + df + "---")
        if flag.upper() == "INFO":
            blackText = "<span style=\"color:#000000;\" >"
            blackText += text
            blackText += "</span>"
            self.textEdit_Output.append(blackText)
        elif flag.upper() == "ERROR":
            redText = "<span style=\"color:#ff0000;\" >"
            redText += "ERROR: "
            redText += text
            redText += "</span>"
            self.textEdit_Output.append(redText)


def module_exists(module_code, s: socket.socket):
    s.sendall(b"Check module exists")
    if s.recv(1024).decode() == "OK":
        s.sendall(module_code.encode())
        result = s.recv(1024).decode()
        if result == "True":
            return True
    return False


def week_number_valid(module_code, week_number, s: socket.socket):
    s.sendall(b"Checking Assignment Week")
    if s.recv(1024).decode() == "OK":
        s.sendall(module_code.encode())
        s.sendall(week_number.encode())
        result = s.recv(1024).decode()
        if result == "True":
            return True
    return False


def check_student_authentication(module_code, student_id, s: socket.socket):
    s.sendall(b"Authentication")
    if s.recv(1024).decode() == "OK":
        s.sendall(module_code.encode())
        s.sendall(student_id.encode())
        is_auth = s.recv(1024).decode()
        if is_auth == "True":
            return True
    return False


def check_collection_filename(filename, module_code, week_number, s: socket.socket):
    """check if the submitted filename matches required filename"""
    s.sendall(b"Check collection filename")
    if s.recv(1024).decode() == "OK":
        s.sendall(filename.encode())
        s.sendall(module_code.encode())
        s.sendall(week_number.encode())
        is_collected_filename = s.recv(1024).decode()
        return is_collected_filename


def create_vars_file(module_code, student_id, week_number, s: socket.socket) -> str:
    """create a vars.yaml file to store info of a specific student"""
    s.sendall(b"Create vars file")
    if s.recv(1024).decode() == "OK":
        s.sendall(module_code.encode())
        s.sendall(student_id.encode())
        s.sendall(week_number.encode())
        # Success or Failed
        result = s.recv(1024).decode()
        return result


def init_vars_file(module_code, student_id, week_number, s: socket.socket):
    s.sendall(b"Init vars file")
    if s.recv(1024).decode() == "OK":
        s.sendall(module_code.encode())
        s.sendall(student_id.encode())
        s.sendall(week_number.encode())


def check_attempts_left(module_code, student_id, week_number, s: socket.socket) -> int:
    s.sendall(b"Check attempts left")
    if s.recv(1024).decode() == "OK":
        s.sendall(module_code.encode())
        s.sendall(student_id.encode())
        s.sendall(week_number.encode())
        attempts_left = s.recv(1024).decode()
        if attempts_left != "False":
            if 1 <= int(attempts_left) <= 10:
                return int(attempts_left)
            else:
                print("you have no attempts left")
                print(attempts_left)
                return 0
        else:
            print("Error when acquiring attemptsLeft value")
            return -1
    return -1


def check_late_penalty(module_code, week_number, s):
    s.sendall(b"Check late penalty")
    if s.recv(1024).decode() == "OK":
        s.sendall(module_code.encode())
        s.sendall(week_number.encode())
        late_penalty = s.recv(1024).decode()
        try:
            late_penalty = int(late_penalty)
        except:
            late_penalty = str(late_penalty)
        return late_penalty


def send_file_to_server(submit_filepath, module_code, week_number, student_id, s: socket.socket):
    s.sendall(b"Send file to server")
    if s.recv(1024).decode() == "OK":
        s.sendall(module_code.encode())
        s.sendall(week_number.encode())
        s.sendall(student_id.encode())
        s.sendall(str(submit_filepath).encode())
        msg = s.recv(1024).decode()
        print(msg)
        with open(submit_filepath, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    s.sendall(b"DONE")
                    break
                s.sendall(data)
        msg = s.recv(1024).decode()
        print(msg)


def get_exec_result(module_code, week_number, student_id, s: socket.socket, file_suffix, penalty: str) -> str:
    s.sendall(b"Get exec result")
    if s.recv(1024).decode() == "OK":
        s.sendall(module_code.encode())
        s.sendall(week_number.encode())
        s.sendall(student_id.encode())
        s.sendall(file_suffix.encode())
        s.sendall(penalty.encode())

        result = s.recv(1024).decode()
        return result


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = HandinMainWindow()
    window.show()
    sys.exit(app.exec_())
