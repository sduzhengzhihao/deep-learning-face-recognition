# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

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
        self.btn_start = QtWidgets.QPushButton(Dialog)
        self.btn_start.setGeometry(QtCore.QRect(600, 50, 181, 61))
        self.btn_start.setObjectName("btn_start")
        self.btn_reg = QtWidgets.QPushButton(Dialog)
        self.btn_reg.setGeometry(QtCore.QRect(600, 180, 181, 61))
        self.btn_reg.setObjectName("btn_reg")
        self.btn_see = QtWidgets.QPushButton(Dialog)
        self.btn_see.setGeometry(QtCore.QRect(600, 310, 181, 61))
        self.btn_see.setObjectName("btn_see")
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
        self.btn_end = QtWidgets.QPushButton(Dialog)
        self.btn_end.setGeometry(QtCore.QRect(600, 440, 181, 61))
        self.btn_end.setObjectName("btn_end")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "学生注册"))
        # self.label_reg.setText(_translate("Dialog", "TextLabel"))
        self.btn_start.setText(_translate("Dialog", "开始"))
        self.btn_reg.setText(_translate("Dialog", "注册"))
        self.btn_see.setText(_translate("Dialog", "查看已注册人员"))
        self.btn_end.setText(_translate("Dialog", "结束"))

if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)  
    widget=QtWidgets.QWidget()  
    dlgUI=Ui_Dialog()
    dlgUI.setupUi(widget)
    widget.show()  
    sys.exit(app.exec_())