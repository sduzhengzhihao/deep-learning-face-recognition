import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QFileDialog
import cv2
import pprint
import time
from collections import OrderedDict
import os
import glob
import numpy as np
import csv
import threading
import pdb
import face_recognition
import time
# 自定义包
import ui
# import reg_ui
import reg_event
import pickle
# 全局变量
SIGN_FORM_FILE = 'data/sign_form.csv'  # 签到表
course = {1:'计算机组成原理-17计算机.txt',
          2:'计算机组成原理-17计算机澳1-3.txt',
          3:'深度学习-17软件1-2班-17数媒.txt',
          4:'深度学习概论-17计算机澳1-3班-17计算机.txt'}
STUDENT_IDS_NAME_FILE = 'data/roster/{0}'.format(course[1]) # 学号姓名信息

class Recog_Thread(threading.Thread):
    def __init__(self, func):
        threading.Thread.__init__(self)
        self.func = func
    def run(self):
        self.func()

class Stored_faces:
    def __init__(self):
        self.num_students = 0
        self.all_id_embedding = OrderedDict() # 所有的学号-Embedding
        self.stored_embeddings()
        self.init_sign_form()
        
    def stored_embeddings(self, stored_faces_path = 'emb_list_all.pkl', data_flag='pkl'):
        '''
        @ stored_faces_path: 存储人脸的路径
        @ data_flag: 'pic' or 'pkl'
        '''
        if data_flag == 'pic':
            pattern = os.path.join(stored_faces_path, '*.jpg') 
            all_face_pics = glob.glob(pattern) # 数据库的所有图像, 相对路径,不是图像名称.jpg
            all_id_list = [x.split('\\')[-1].split('.')[0] for x in all_face_pics] # 所有学号str
            
            for id_str, pic_path in zip(all_id_list, all_face_pics):
                print('Loading {0}'.format(id_str))
                im_bgr = cv2.imread(pic_path)
                im_rgb = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(im_rgb)  # list[box,...]
                face_encodings = face_recognition.face_encodings(im_rgb, face_locations)  #list
                self.all_id_embedding[id_str] = face_encodings[0]
                print(self.all_id_embedding)
            self.num_students = len(all_face_pics)

        if data_flag == 'pkl':
            with open('emb_list_all.pkl', 'rb') as f:
                emb_list = pickle.load(f)
            self.all_id_embedding = OrderedDict([(x[0],x[2]) for x in emb_list])
            self.num_students = len(self.all_id_embedding)
            print(self.num_students)

    def init_sign_form(self, sign_form=SIGN_FORM_FILE, student_ids_name = STUDENT_IDS_NAME_FILE):
        '''
        读取student_ids.txt,写入sign_form.csv
        '''
        if not os.path.exists(sign_form):
            with open(sign_form, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, ['stu_id', 'stu_name', 'sign_status'])
                # writer.writerow({'stu_id': '2018001', 'stu_name': 'Baked', 'sign_status': ''})
                # pdb.set_trace()
                with open(student_ids_name, 'r', encoding='utf-8-sig') as txtfile:
                    num_name = txtfile.readlines()
                    for id_num_name_str in [x.split()[0] for x in num_name]:
                        stu_id, stu_name = id_num_name_str.split('-')
                        writer.writerow({'stu_id':stu_id, 'stu_name':stu_name, 'sign_status':'0'})


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



# 继承ui,添加事件
class Event(ui.Ui_Dialog):
    '''---------------------------------------
    # TODO:窗口退出时结束线程
    ---------------------------------------'''
    def __init__(self, thre=0.35):
        ## 初始化多线程
        self.video_thread = VideoThread()
        self.video_thread.timeSignal.signal[str].connect(self.show_video_images)

        self.recognize_thread = Recog_Thread(self.recognize_video_images)
        
        self.thre = thre  # 是否为同一个人的阈值

        self.start_end_btn_flag = False # 控制start/end按钮是否可用
        self.btn_show_signed = None # 显示已签到人员 
        self.btn_start = None # 开始签到
        self.btn_show_unsigned = None # 显示未签到人员
        self.btn_screenshot = None # 签到人员截屏目录
        self.btn_sign_form = None # 签到表
        self.btn_end =None # 结束签到
        self.qlabel_video = None #视频显示标签
        self.qtxt_showname = None # 显示签到人员,QTextBrowser
        self.lcd_signedCount = None #LCD显示
        self.num_sign = 0
    def ctrl_start_end_btn(self, flag):
        self.btn_end.setEnabled(flag)

    
    def setupUi(self, Dialog):
        super().setupUi(Dialog)
        
        ## 初始化视频播放界面,qlabel_video
        pic = './res/timg.jpg'
        qmap = QtGui.QPixmap(pic).scaled(self.qlabel_video.width(), self.qlabel_video.height())
        self.qlabel_video.setPixmap(qmap) #需要删除setText才能显示图像

        ## 槽函数
        self.btn_show_signed.clicked.connect(self.btn_show_signed_click)
        self.btn_start.clicked.connect(self.btn_start_click)
        self.btn_show_unsigned.clicked.connect(self.btn_show_unsigned_click)
        self.btn_screenshot.clicked.connect(self.btn_screenshot_click)
        self.btn_sign_form.clicked.connect(self.btn_sign_form_click)
        self.btn_end.clicked.connect(self.btn_end_click)
        self.btn_end.setEnabled(False)
        
        # 初始LCD
        with open(SIGN_FORM_FILE, 'r') as f: # 文件对象
            reader = csv.DictReader(f, ['stu_id', 'stu_name', 'sign_status'])
            sign_form_from_file = {tuple(x.values())[0]:tuple(x.values())[1:]  for x in list(reader)} # 来自文件的签到表,dict
            unsigned_list_from_file = [(x[0], x[1][0]) for x in sign_form_from_file.items() if x[1][1]=='1'] # 来自文件签到人员
            self.num_sign = len(unsigned_list_from_file)
            self.lcd_signedCount.display(self.num_sign) # 初始LCD
        

    # 开始签到
    def btn_start_click(self):
        # 控制按钮可用
        self.btn_start.setEnabled(False)
        self.start_end_btn_flag = not self.start_end_btn_flag
        self.ctrl_start_end_btn(self.start_end_btn_flag)

        # 读取签到表
        with open(SIGN_FORM_FILE, 'r') as f: # 文件对象
            reader = csv.DictReader(f, ['stu_id', 'stu_name', 'sign_status'])
            self.sign_form_from_file = {tuple(x.values())[0]:tuple(x.values())[1:]  for x in list(reader)} # 来自文件的签到表,dict
            self.sign_form_realtime = self.sign_form_from_file.copy() # 实时签到表
            self.unsigned_set_realtime = {x[0] for x in self.sign_form_realtime.items() if x[1][1]=='0'} # 实时未签到人员,set

        ## 摄像头相关
        self.video_capture = cv2.VideoCapture(0,cv2.CAP_DSHOW) # 启动摄像头
        # 判断摄像头是否开启,调整按钮可用/不可用
        if not self.video_capture.isOpened(): 
            QMessageBox.warning(self.btn_show_unsigned, '警告', '摄像头未开启', QMessageBox.Ok)
            self.start_end_btn_flag = not self.start_end_btn_flag
            self.ctrl_start_end_btn(self.start_end_btn_flag)
            return
        self.video_thread.start() #开启摄像头显示
        self.recognize_thread = Recog_Thread(self.recognize_video_images)
        self.recognize_thread.start()
        

        
    # 显示未签到人员名单
    def btn_show_unsigned_click(self):
        self.qtxt_showname.setText('') # 清空txtbrowser
        if not os.path.exists(SIGN_FORM_FILE):
            QMessageBox.warning(self.btn_show_unsigned, '警告', '未找到签到表', QMessageBox.Ok)
        with open(SIGN_FORM_FILE, 'r') as f: # 文件对象
            reader = csv.DictReader(f, ['stu_id', 'stu_name', 'sign_status'])
            self.sign_form_from_file = {tuple(x.values())[0]:tuple(x.values())[1:]  for x in list(reader)} # 来自文件的签到表,dict
            self.unsigned_list_from_file = [(x[0], x[1][0]) for x in self.sign_form_from_file.items() if x[1][1]=='0'] # 实时未签到人员
            for id_name in self.unsigned_list_from_file:
                self.qtxt_showname.append(id_name[0]+' '+id_name[1])
        self.qtxt_showname.append('')
        self.qtxt_showname.append('-'*20)
        self.qtxt_showname.append('一共 {0} 人未签到!'.format(len(self.unsigned_list_from_file)))
    
    # 显示已签到人员
    def btn_show_signed_click(self):
        self.qtxt_showname.setText('') # 清空txtbrowser
        if not os.path.exists(SIGN_FORM_FILE):
            QMessageBox.warning(self.btn_show_signed, '警告', '未找到签到表', QMessageBox.Ok)
        with open(SIGN_FORM_FILE, 'r') as f: # 文件对象
            reader = csv.DictReader(f, ['stu_id', 'stu_name', 'sign_status'])
            self.sign_form_from_file = {tuple(x.values())[0]:tuple(x.values())[1:]  for x in list(reader)} # 来自文件的签到表,dict
            self.unsigned_list_from_file = [(x[0], x[1][0]) for x in self.sign_form_from_file.items() if x[1][1]=='1'] # 来自文件签到人员
            for id_name in self.unsigned_list_from_file:
                self.qtxt_showname.append(id_name[0]+' '+id_name[1])
        self.qtxt_showname.append('')
        self.qtxt_showname.append('-'*20)
        self.qtxt_showname.append('一共 {0} 人签到!'.format(len(self.unsigned_list_from_file)))
    
    # 打开截图文件夹
    def btn_screenshot_click(self):
        os.startfile('data')
    
    # 打开新界面,注册界面------------------------------------------------------------------
    def btn_sign_form_click(self):
        self.btn_end_click() #调用结束签到
        self.btn_start.setEnabled(True)
        ## 启动注册界面
        self.widget=QtWidgets.QWidget()  
        self.dlgUI=reg_event.RegEvent()
        self.dlgUI.setupUi(self.widget)
        self.widget.show()
        
     #--------------------------------------------------------------------------

    # 结束签到
    def btn_end_click(self):
        self.start_end_btn_flag = not self.start_end_btn_flag
        self.ctrl_start_end_btn(self.start_end_btn_flag)
        if 'video_capture' in self.__dir__():
            self.video_capture.release()        #释放摄像头
        else:
            print('failed to close')
        pic = './res/timg.jpg'
        qmap = QtGui.QPixmap(pic).scaled(self.qlabel_video.width(), self.qlabel_video.height())
        self.qlabel_video.setPixmap(qmap) #需要删除setText才能显示图像
        self.video_capture.release()
        cv2.destroyAllWindows()
        self.btn_start.setEnabled(True)

        # 视频显示在标签上
    def show_video_images(self):
        '''
        多线程调用
        '''
        success, frame_bgr = self.video_capture.read(0) #frame-bgr
        if not success:
            return
        height, width, _ = frame_bgr.shape
        # TODO: 请在视频前停留2s
        cv2.putText(frame_bgr, 'Please Stay 2-5s', (10,40), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0,255,0), 2)
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
        pixmap = QtGui.QPixmap(qimg).scaled(int(1.5*width_ratio), int(1.5*height_ratio))
        self.qlabel_video.setPixmap(pixmap) #需要删除setText才能显示图像

    def recognize_video_images(self):
        '''
        多线程调用
        '''
        while True:
            time.sleep(2)
            success, frame_bgr = self.video_capture.read() #frame-bgr
            if not success:
                return
            frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB) ##frame-rgb
            face_locations = face_recognition.face_locations(frame_rgb)  # list[box,...]
            face_encodings = face_recognition.face_encodings(frame_rgb, face_locations)

            for face_encoding in face_encodings:
                # bbox
                all_dists = np.linalg.norm(list(all_stored_embeddings.values()) - face_encoding, axis=1)  # 与存储人脸数据的所有距离
                min_dist_index = all_dists.argmin()  # 最小距离所在索引
                min_dist_value = all_dists[min_dist_index] # 最小距离
                id_num_str = list(all_stored_embeddings.keys())[min_dist_index]  # 最小距离/索引对应的学号

                ## 处理符合人脸
                if min_dist_value < self.thre:  # 如果人脸距离小于阈值
                    # 更新签到表
                    if id_num_str in self.unsigned_set_realtime: # 如果在未签到集合中
                        cv2.imwrite(os.path.join('data', 'signin_screenshoot', id_num_str+'screenshot.jpg'), cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR))
                        self.update_sign_form(id_num_str = id_num_str)  # 屏显

    def update_sign_form(self, id_num_str, sign_form_file=SIGN_FORM_FILE):
        self.qtxt_showname.append('{0} {1} 签到成功!'.format(id_num_str, self.sign_form_realtime[id_num_str][0]))
        self.unsigned_set_realtime.remove(id_num_str) # 从未签到人员中删除这个签到成功学生
        self.num_sign+=1
        self.lcd_signedCount.display(self.num_sign) # 更新LCD
        
        # 将这个签到成功学生写入到实时签到表中
        sign_success_stu = list(self.sign_form_realtime[id_num_str])
        sign_success_stu[1] = '1'
        sign_success_stu = tuple(sign_success_stu)
        self.sign_form_realtime[id_num_str] = sign_success_stu
        # 写入到磁盘
        with open(sign_form_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, ['stu_id', 'stu_name', 'sign_status'])
            for id_name_statue in self.sign_form_realtime.items():
                writer.writerow({'stu_id':id_name_statue[0], 'stu_name':id_name_statue[1][0], 'sign_status':id_name_statue[1][1]})


if __name__=='__main__':
    print("Loading Stored id...")
    st = Stored_faces()
    all_stored_embeddings = st.all_id_embedding  # 全局可用
    print("Loading Finished")
    app=QtWidgets.QApplication(sys.argv)  
    widget=QtWidgets.QWidget()  
    dlgUI=Event()
    dlgUI.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())