from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QCompleter
import sys
import cv2
import pprint
import time
from collections import OrderedDict
import os
import glob
import numpy as np
import csv

import reg_ss_ui

# txt_stuNum提示列表
def getAllStuNum(stunumtxt):
    src = 'data/roster'
    roster_list = glob.glob(os.path.join(src, '*.txt'))
    stu_list = []
    for roster in roster_list:
        with open(roster, 'r', encoding='utf-8') as f:
            num_name_list = [x.split()[0] for x in f.readlines()]
            stu_list.extend(num_name_list)
    return stu_list

class Reg_ss_Event(reg_ss_ui.Ui_Dialog):
    def __init__(self, screen_shot, widget):
        self.btn_ok = None # 初始化OK按钮
        self.label_screenShot = None
        self.txt_stuNum = None
        self.screenShot = screen_shot
        self.widget = widget
        self.stu_list = getAllStuNum(0)

    def setupUi(self, Dialog):
        super().setupUi(Dialog)
        height, width, _ = self.screenShot.shape
        # print(height, width)
        # print(self.label_screenShot.width(), self.label_screenShot.height())
        qimg = QtGui.QImage( self.screenShot.data, width, height, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap(qimg).scaled(int(self.label_screenShot.width()), self.label_screenShot.height()*0.85)
        self.label_screenShot.setPixmap(pixmap) #需要删除setText才能显示图像

        # 初始化代码补全
        self.txt_stuNum_completer()
        # 槽函数
        self.btn_ok.clicked.connect(self.btn_ok_click)

    # txt_stuNum自动补全
    def txt_stuNum_completer(self):
        self.completer = QCompleter(self.stu_list)
        self.txt_stuNum.setCompleter(self.completer)

    def btn_ok_click(self):
        stu_num_txt = self.txt_stuNum.text()  #文本框中的内容
        stu_num_str = stu_num_txt.split('-')[0] # 获得学号str
        if not stu_num_str.isnumeric():
            QMessageBox.warning(QtWidgets.QWidget(), "警告", "请输入正确的学号！")
            return
        # dst = os.path.join(os.getcwd(),'data','reg_pics',stu_num_txt+'.jpg')
        dst = 'data/'+'reg_pics/'+stu_num_str+'.jpg'
        print(dst)
        cv2.imwrite(dst, self.screenShot[:,:,::-1])
        QMessageBox.information(QtWidgets.QWidget(), "提示", "学生注册信息已保存！")
        # 自动关闭
        self.widget.close()
        
        
        

if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)  
    widget=QtWidgets.QWidget()  
    dlgUI=Reg_ss_Event(None)
    dlgUI.setupUi(widget)
    widget.show()  
    sys.exit(app.exec_())