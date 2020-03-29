import sys
from PyQt5.QtWidgets import QApplication, QWidget,QToolTip,QPushButton
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import QCoreApplication
#demo_4:通过一个按钮关闭窗体
class Exception(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('添加关闭按钮')
        self.setFont(QFont('微软雅黑',20))
        self.resize(400,300)
        self.setWindowIcon(QIcon('1.png'))
        btn=QPushButton('关闭',self)
        #关闭应用
        btn.clicked.connect(QCoreApplication.instance().quit)
        self.show()
if __name__=='__main__':
    pp=QApplication(sys.argv)
    example=Exception()
    #example.show()
    sys.exit(pp.exec())