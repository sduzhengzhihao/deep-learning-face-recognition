from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import cv2
import pprint
import time
from collections import OrderedDict
import os
import glob
import numpy as np
import csv

import face_recognition

import reg_ui
import reg_ss_event

class Communicate(QtCore.QObject):
    signal = QtCore.pyqtSignal(str) # str是标识的意思吗

# QThread新线程播放视频
class VideoThread(QtCore.QThread):
    def __init__(self, sleep_time=1/8.):
        QtCore.QThread.__init__(self)
        self.sleep_time = sleep_time
        self.timeSignal = Communicate()
    
    def run(self):
        while True:
            self.timeSignal.signal.emit("1")  #-------???
            time.sleep(self.sleep_time)  #调小一点视频更流畅


class RegEvent(reg_ui.Ui_Dialog):
    def __init__(self):
        ## 初始化多线程
        self.video_thread = VideoThread()
        self.video_thread.timeSignal.signal[str].connect(self.show_video_images)

        self.btn_start = None # 初始化开始按钮
        self.btn_reg = None # 初始化注册按钮
        self.btn_see = None # 初始化查看按钮
        self.btn_end = None # 初始化结束按钮
        self.label_reg = None
        self.enable_reg_end_flag = False
        self.enable_start_flag = True
        
    def setupUi(self, Dialog):
        super().setupUi(Dialog)
        # self.btn_reg.setEnabled(False)
        self.btn_end.setEnabled(self.enable_reg_end_flag )
        self.btn_reg.setEnabled(self.enable_reg_end_flag )
        self.btn_start.setEnabled(self.enable_start_flag )
        
        pic = './res/timg.jpg'
        qmap = QtGui.QPixmap(pic).scaled(self.label_reg.width(), self.label_reg.height())
        self.label_reg.setPixmap(qmap) #需要删除setText才能显示图像

        ## 槽函数
        self.btn_start.clicked.connect(self.btn_start_click)
        self.btn_reg.clicked.connect(self.btn_reg_click)
        self.btn_see.clicked.connect(self.btn_see_click)
        self.btn_end.clicked.connect(self.btn_end_click)

    # 点击开始按钮,开启视频
    def btn_start_click(self):
        self.enable_start_flag = not self.enable_start_flag
        self.btn_start.setEnabled(self.enable_start_flag )
        self.video_capture = cv2.VideoCapture(0) # 启动摄像头
        if not self.video_capture.isOpened(): 
            QMessageBox.warning(self.btn_show_unsigned, '警告', '摄像头未开启', QMessageBox.Ok)
            return
        self.video_thread.start() #开启摄像头显示
        self.enable_reg_end_flag = True
        self.btn_end.setEnabled(self.enable_reg_end_flag )
        self.btn_reg.setEnabled(self.enable_reg_end_flag )

    # 查看已注册人员
    def btn_see_click(self):
        os.startfile('data')

    # 点击注册按钮，启动截屏注册界面
    def btn_reg_click(self):
        success, frame_bgr = self.video_capture.read() #frame-bgr
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB) ##frame-rgb
        # print(type(frame_rgb))
        self.widget=QtWidgets.QWidget()  
        self.dlgUI=reg_ss_event.Reg_ss_Event(frame_rgb, self.widget)
        self.dlgUI.setupUi(self.widget)
        self.widget.show()
    
    # 结束注册
    def btn_end_click(self):
        self.enable_start_flag = True
        self.btn_start.setEnabled(self.enable_start_flag )
        if 'video_capture' in self.__dir__():
            self.video_capture.release() #释放摄像头
        pic = './res/timg.jpg'
        qmap = QtGui.QPixmap(pic).scaled(self.label_reg.width(), self.label_reg.height())
        self.label_reg.setPixmap(qmap) #需要删除setText才能显示图像
    
    def show_video_images(self):
        '''
        多线程调用
        '''
        success, frame_bgr = self.video_capture.read() #frame-bgr
        if not success:
            return
        height, width, _ = frame_bgr.shape
        frame_bgr = cv2.resize(frame_bgr, (width//2, height//2))
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB) ##frame-rgb
        max_side = max(width//2, height//2)
        ratio = max_side/391.
        height_ratio = int(height/2*ratio)
        width_ratio = int(width/2*ratio)
       
        face_locations = face_recognition.face_locations(frame_rgb)  # list[box,...]
        for (top, right, bottom, left) in face_locations:
            # bbox
            cv2.rectangle(frame_rgb, (left, top), (right, bottom), (0, 0, 255), 2)
       
        qimg = QtGui.QImage(frame_rgb.data, width//2, height//2, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap(qimg).scaled(int(2.4*width_ratio), int(2.4*height_ratio))
        self.label_reg.setPixmap(pixmap) #需要删除setText才能显示图像


if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)  
    widget=QtWidgets.QWidget()  
    dlgUI=RegEvent()
    dlgUI.setupUi(widget)
    widget.show()  
    sys.exit(app.exec_())