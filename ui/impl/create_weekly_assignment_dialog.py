# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'create_weekly_assignment_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 20, 111, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        font.setKerning(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.comboBox_moduleCode = QtWidgets.QComboBox(Dialog)
        self.comboBox_moduleCode.setGeometry(QtCore.QRect(130, 20, 87, 22))
        self.comboBox_moduleCode.setObjectName("comboBox_moduleCode")
        self.dateTimeEdit_startDay = QtWidgets.QDateTimeEdit(Dialog)
        self.dateTimeEdit_startDay.setGeometry(QtCore.QRect(170, 70, 194, 22))
        self.dateTimeEdit_startDay.setObjectName("dateTimeEdit_startDay")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 70, 121, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 110, 72, 15))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(30, 150, 101, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(30, 190, 141, 16))
        self.label_5.setObjectName("label_5")
        self.dateTimeEdit_endDay = QtWidgets.QDateTimeEdit(Dialog)
        self.dateTimeEdit_endDay.setGeometry(QtCore.QRect(170, 110, 194, 22))
        self.dateTimeEdit_endDay.setObjectName("dateTimeEdit_endDay")
        self.dateTimeEdit_cutoffDay = QtWidgets.QDateTimeEdit(Dialog)
        self.dateTimeEdit_cutoffDay.setGeometry(QtCore.QRect(170, 150, 194, 22))
        self.dateTimeEdit_cutoffDay.setObjectName("dateTimeEdit_cutoffDay")
        self.lineEdit_penaltyPerDay = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_penaltyPerDay.setGeometry(QtCore.QRect(170, 190, 113, 21))
        self.lineEdit_penaltyPerDay.setObjectName("lineEdit_penaltyPerDay")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(240, 20, 41, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.comboBox_weekNumber = QtWidgets.QComboBox(Dialog)
        self.comboBox_weekNumber.setGeometry(QtCore.QRect(290, 20, 81, 22))
        self.comboBox_weekNumber.setObjectName("comboBox_weekNumber")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Create Weekly Assignment"))
        self.label.setText(_translate("Dialog", "Module Code:"))
        self.label_2.setText(_translate("Dialog", "Start Day:"))
        self.label_3.setText(_translate("Dialog", "End Day:"))
        self.label_4.setText(_translate("Dialog", "Cutoff Day:"))
        self.label_5.setText(_translate("Dialog", "Penalty per day:"))
        self.label_6.setText(_translate("Dialog", "Week:"))
