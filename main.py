import sys
from time import sleep
import threading 
import inspect
import ctypes
import random

from PyQt5.QtCore import * # Qt, QTimer, pyqtSlot
from PyQt5.QtGui import * # QFont, QFontMetrics, QPainter,QPixmap, QMouseEvent
from PyQt5.QtWidgets import * #QApplication, QLabel, QWidget

ori = ""
trans = ""

class ScrollTextWindow(QWidget):
    """ 滚动字幕 """

    def __init__(self, songName, songerName, parent=None):
        super().__init__(parent)
        self.songName = songName
        self.songerName = songerName
        # 实例化定时器
        self.timer = QTimer(self)
        # 设置刷新时间和移动距离
        self.timeStep = 1
        self.moveStep = 5
        self.songCurrentIndex = 0
        self.songerCurrentIndex = 0
        # 设置字符串溢出标志位
        self.isSongNameAllOut = False
        self.isSongerNameAllOut = False
        # 设置两段字符串之间留白的宽度
        self.spacing = 25
        # 初始化界面
        self.initWidget()
        # 背景设为透明
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.timer.start(self.timeStep*1000)
        self.counter = 0
        self.ori = ori

    def initWidget(self):
        """ 初始化界面 """
        self.setFixedHeight(115)
        self.setAttribute(Qt.WA_StyledBackground)
        # 调整窗口宽度
        self.adjustWindowWidth()
        # 初始化定时器
        self.timer.setInterval(self.timeStep)
        self.timer.timeout.connect(self.updateIndex)
        # 只要有一个字符串宽度大于窗口宽度就开启滚动：
        if self.isSongerNameTooLong or self.isSongNameTooLong:
            self.timer.start()

    def getTextWidth(self):
        """ 计算文本的总宽度 """
        songFontMetrics = QFontMetrics(QFont('Microsoft YaHei', 14, 400))
        self.songNameWidth = sum([songFontMetrics.width(i)
                                  for i in self.songName])
        songerFontMetrics = QFontMetrics(QFont('Microsoft YaHei', 12, 500))
        self.songerNameWidth = sum(
            [songerFontMetrics.width(i) for i in self.songerName])

    def adjustWindowWidth(self):
        """ 根据字符串长度调整窗口宽度 """
        self.getTextWidth()
        maxWidth = max(self.songNameWidth*3, self.songerNameWidth*3)
        # 判断是否有字符串宽度超过窗口的最大宽度
        self.isSongNameTooLong = self.songNameWidth > 250
        self.isSongerNameTooLong = self.songerNameWidth > 250
        # 设置窗口的宽度
        self.setFixedWidth(min(maxWidth, 1200))

    def updateIndex(self):
        """ 更新下标 """
        self.repaint()
        self.songCurrentIndex += 1
        self.songerCurrentIndex += 1
        # 设置下标重置条件
        resetSongIndexCond = self.songCurrentIndex * \
            self.moveStep >= self.songNameWidth + self.spacing * self.isSongNameAllOut
        resetSongerIndexCond = self.songerCurrentIndex * \
            self.moveStep >= self.songerNameWidth + self.spacing * self.isSongerNameAllOut
        # 只要条件满足就要重置下标并将字符串溢出置位，保证在字符串溢出后不会因为留出的空白而发生跳变
        if resetSongIndexCond:
            self.songCurrentIndex = 0
            self.isSongNameAllOut = True
        if resetSongerIndexCond:
            self.songerCurrentIndex = 0
            self.isSongerNameAllOut = True

    def paintEvent(self, e):
        """ 绘制文本 """
        global ori
        # super().paintEvent(e)
        painter = QPainter(self)
        painter.setPen(Qt.white)
        # 绘制歌名
        painter.setFont(QFont('Microsoft YaHei', 14))
        # if self.isSongNameTooLong and self.counter<100:
            # # 实际上绘制了两段完整的字符串
            # # 从负的横坐标开始绘制第一段字符串
            # painter.drawText(self.spacing * self.isSongNameAllOut - self.moveStep *
                             # self.songCurrentIndex, 54, self.songName)
            # # 绘制第二段字符串
            # painter.drawText(self.songNameWidth - self.moveStep * self.songCurrentIndex +
                             # self.spacing * (1 + self.isSongNameAllOut), 54, self.songName)
            # self.counter += 1
        # else:
            # painter.drawText(0, 54, self.songName)
        if self.ori == "":
            self.ori = ori
            painter.drawText(0, 54, self.ori)
        else:
            painter.drawText(0, 54, ori)
        # if self.counter < 30:
            # if self.counter == 10:
                # self.songName = "Fuck You"
            # else:
                # self.songName = str(self.counter)
            # painter.drawText(0, 54, self.songName)
            # sleep(0.001)
            # self.counter += 1
        # else:
            # painter.drawText(0, 54, "hello")
            

        # 绘制歌手名  
        painter.setFont(QFont('Microsoft YaHei', 12, 500))
        painter.begin(self)
        if self.isSongerNameTooLong:
            painter.drawText(self.spacing * self.isSongerNameAllOut - self.moveStep *
                             self.songerCurrentIndex, 82, self.songerName)
            painter.drawText(self.songerNameWidth - self.moveStep * self.songerCurrentIndex +
                             self.spacing * (1 + self.isSongerNameAllOut), 82, self.songerName)
        else:
            painter.drawText(0, 82, self.songerName)
        painter.end()
        #painter.CompositionMode_Clear()
        #painter.drawText(0, 100, "mamamamama")
        

class SongInfoCard(QWidget):
    """ 播放栏左侧歌曲信息卡 """

    def __init__(self, parent=None):
        super().__init__(parent)
        # 保存信息
        #self.songInfo = songInfo
        self.songName = "hello world"
        self.songerName = "Vincent"
        # 实例化小部件
        self.albumPic = QLabel(self)
        self.scrollTextWindow = ScrollTextWindow(
            self.songName, self.songerName, self)
        # 初始化界面
        self.initWidget()
        # 背景设为透明
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.move(0, 0)

    def initWidget(self):
        """ 初始化小部件 """
        self.setFixedHeight(115)
        self.setFixedWidth(115 + 15 + self.scrollTextWindow.width() + 25)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.scrollTextWindow.move(130, 0)
        self.albumPic.setPixmap(QPixmap(r'./OIP2.jfif').scaled(
                                115, 115, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                                
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  #更改鼠标图标
            
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:  
            self.move(QMouseEvent.globalPos()-self.m_Position)#更改窗口位置
            QMouseEvent.accept()
            
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QCursor(Qt.ArrowCursor))

    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        关闭窗口
        """
        self.close()
    
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        最小化窗口
        """
        self.showMinimized()

class Subtitle:
    def __init__(self, content):
        self.app = QApplication(sys.argv)
        self.songInfo = content
            #{
            #'songName': 'ハッピーでバッドな眠りは浅い', 'songer': '鎖那',
            #'album': [r'resource\Album Cover\ハッピーでバッドな眠りは浅い\ハッピーでバッドな眠りは浅い.png']}
        self.demo = SongInfoCard(self.songInfo)
        self.demo.setStyleSheet('background:rgb(129,133,137)')
        self.demo.show()
        sys.exit(self.app.exec_())
        self.create_dict()
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        关闭窗口
        """
        self.close()
        
    
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        最小化窗口
        """
        self.showMinimized()
    
    def create_dict(self):
        for i in [1,2,3,4,5,6,7,8,9,0]:
            global global_dict
            ori = str(i)
            sleep(1)

def create_dict():
    global global_dict
    ori = "1"
    # for i in [1,2,3,4,5,6,7,8,9,0]:
        # ori = str(i)
        # sleep(1)

class WorkThread(QThread, QObject):
    update_date = pyqtSignal(str)
    
    # 初始化线程
    def __int__(self):
        super(WorkThread, self).__init__()
    
    #线程运行函数
    def run(self):
        while True:
            global ori
            global trans
            print(ori)
            ori = str(random.randint(200,225))
            trans = str(random.randint(150,200))
            self.update_date.emit(ori)
            self.update_date.emit(trans)
            sleep(1)

if __name__ == "__main__":
    workThread = WorkThread()
    workThread.start()
    # threading.Thread(target = create_dict(), args=()).start()
    app = QApplication(sys.argv)
    songInfo = {
        'songName': 'ハッピーでバッドな眠りは浅い', 'songer': '鎖那',
        'album': [r'./OIP2.jfif']}
    # demo = SongInfoCard(songInfo)
    demo = SongInfoCard()
    demo.setStyleSheet('background:rgb(129,133,137)')
    #threading.Thread(target = demo.show(), args=()).start()
    demo.show()
    # for i in range(10):
        # sleep(0.8)
        # print(ori)
        
    # while 1:
        # ori = input("Origin: ")
        # global_dict[ori] = input("Translate")
        # if tem_dict=={}:
            # tem_dict = global_dict
        # sleep(0.5)
    
    #demo.show()
    # dic_res = {
        # "Hi, how are you?": u"哈喽， 你最近过的怎么样?",
        # "Tommy, are you there? What happen today?": u"汤米，在吗？今天发生了什么？"
    # }
    
    # for i in ["Hi, how are you?", "Tommy, are you there? What happen today?"]:
        # new_data = {
                    # 'songName': i, 'songer': dic_res[i],
                    # 'album': [r'./OIP2.jfif']
                    # }
        # m = threading.Thread(target = Subtitle, args=(new_data,), daemon=True)
        # m.start()
        
        # print("prepare")
        # sleep(10)
        # print("changed")
    
    # sleep(30)