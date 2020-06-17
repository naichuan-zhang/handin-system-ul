# -*- coding: utf-8 -*-
import sys

from PyQt5 import QtCore, QtWidgets
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
        self.textBrowser_showResult = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_showResult.setGeometry(QtCore.QRect(20, 470, 750, 200))
        self.textBrowser_showResult.setObjectName("textBrowser_showResult")
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


class HandinMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(HandinMainWindow, self).__init__()
        self.setupUi(self)
        self.pushButton_browse.clicked.connect(self.browse)
        self.pushButton_handin.clicked.connect(self.handin)
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

    def handin(self):
        # TODO: Check if week number valid?
        week_number = self.comboBox_weekNumber.currentText()
        print(week_number)
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = HandinMainWindow()
    window.show()
    sys.exit(app.exec_())
