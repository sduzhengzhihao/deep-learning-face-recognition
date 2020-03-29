# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register_screenShot.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(627, 426)
        self.label_screenShot = QtWidgets.QLabel(Dialog)
        self.label_screenShot.setGeometry(QtCore.QRect(20, 20, 381, 381))
        self.label_screenShot.setObjectName("label_screenShot")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(10, 0, 401, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(Dialog)
        self.line_2.setGeometry(QtCore.QRect(0, 10, 20, 401))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(Dialog)
        self.line_3.setGeometry(QtCore.QRect(10, 400, 401, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(Dialog)
        self.line_4.setGeometry(QtCore.QRect(400, 10, 20, 401))
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(420, 50, 111, 16))
        self.label_2.setObjectName("label_2")
        self.txt_stuNum = QtWidgets.QLineEdit(Dialog)
        self.txt_stuNum.setGeometry(QtCore.QRect(420, 70, 191, 31))
        self.txt_stuNum.setObjectName("txt_stuNum")
        self.btn_ok = QtWidgets.QPushButton(Dialog)
        self.btn_ok.setGeometry(QtCore.QRect(420, 140, 191, 41))
        self.btn_ok.setObjectName("btn_ok")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "保存截图"))
        self.label_screenShot.setText(_translate("Dialog", "TextLabel"))
        self.label_2.setText(_translate("Dialog", "请输入学号："))
        self.btn_ok.setText(_translate("Dialog", "确定"))

if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)  
    widget=QtWidgets.QWidget()  
    dlgUI=Ui_Dialog()
    dlgUI.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())