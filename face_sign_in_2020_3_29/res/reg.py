# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(810, 591)
        self.label_reg = QtWidgets.QLabel(Dialog)
        self.label_reg.setGeometry(QtCore.QRect(20, 20, 551, 541))
        self.label_reg.setObjectName("label_reg")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(10, 0, 571, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_6 = QtWidgets.QFrame(Dialog)
        self.line_6.setGeometry(QtCore.QRect(560, 10, 40, 571))
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.btn_start1 = QtWidgets.QPushButton(Dialog)
        self.btn_start1.setGeometry(QtCore.QRect(600, 50, 181, 61))
        self.btn_start1.setObjectName("btn_start1")
        self.btn_reg = QtWidgets.QPushButton(Dialog)
        self.btn_reg.setGeometry(QtCore.QRect(600, 180, 181, 61))
        self.btn_reg.setObjectName("btn_reg")
        self.btn_end1 = QtWidgets.QPushButton(Dialog)
        self.btn_end1.setGeometry(QtCore.QRect(600, 310, 181, 61))
        self.btn_end1.setObjectName("btn_end1")
        self.line_2 = QtWidgets.QFrame(Dialog)
        self.line_2.setGeometry(QtCore.QRect(10, 570, 571, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_7 = QtWidgets.QFrame(Dialog)
        self.line_7.setGeometry(QtCore.QRect(-10, 10, 40, 571))
        self.line_7.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.btn_end1_2 = QtWidgets.QPushButton(Dialog)
        self.btn_end1_2.setGeometry(QtCore.QRect(600, 440, 181, 61))
        self.btn_end1_2.setObjectName("btn_end1_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_reg.setText(_translate("Dialog", "TextLabel"))
        self.btn_start1.setText(_translate("Dialog", "开始"))
        self.btn_reg.setText(_translate("Dialog", "注册"))
        self.btn_end1.setText(_translate("Dialog", "查看已注册人员"))
        self.btn_end1_2.setText(_translate("Dialog", "结束"))

