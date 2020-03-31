from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtCore import *
import math


class chart_widget(QWidget):
    def __init__(self,parent =None):
        super(chart_widget,self).__init__(parent)
        self.resize(200,60)
        self.layout = QGridLayout(self)
        #背景填充灰色
        self.setAutoFillBackground(True)
        p  = QPalette()
        p.setColor(QPalette.Background,Qt.gray)
        self.setPalette(p)
        #设置进度条颜色
        self.bg_color = QColor(255, 0, 0)
        #设置界面刷新时间
        self.startTimer(80)
        self.m_waterOffset = 0.05
        self.m_offset = 50
        self.m_borderwidth = 10
        self.per_num = 0


    def paintEvent(self, event):
        # 锯齿状绘画板；
        painter = QPainter()
        painter.setRenderHint(QPainter.Antialiasing)
        painter.begin(self)
        #获取窗口的宽度和高度
        width,height = self.width(),self.height()
        percentage = 1 - self.per_num/100
        # 水波走向：正弦函数 y = A(wx+l) + k
        # w 表示 周期，值越大密度越大
        w = 2 * math.pi / (width)
        # A 表示振幅 ，理解为水波的上下振幅
        A = height * self.m_waterOffset
        # k 表示 y 的偏移量，可理解为进度
        k = height *percentage


        water1 = QPainterPath()
        water2 = QPainterPath()
        #起始点
        water1.moveTo(5,height)
        water2.moveTo(5,height)
        self.m_offset += 0.6

        if(self.m_offset >(width/2)):
            self.m_offset = 0
        i = 5
        while(i < width-5):
            waterY1 = A*math.sin(w*i +self.m_offset ) + k
            waterY2 = A*math.sin(w*i + self.m_offset + width/2*w) + k

            water1.lineTo(i, waterY1)
            water2.lineTo(i, waterY2)
            i += 1

        water1.lineTo(width-5,height)
        water2.lineTo(width-5,height)
        totalpath = QPainterPath()
        totalpath.addRect(QRectF(5, 5, self.width() - 10, self.height() - 10))
        painter.setBrush(Qt.gray)
        painter.drawRect(self.rect())
        painter.save()


        painter.setPen(Qt.NoPen)

        #设置水波的透明度
        watercolor1 =QColor(self.bg_color)
        watercolor1.setAlpha(100)
        watercolor2 = QColor(self.bg_color)
        watercolor2.setAlpha(150)

        path = totalpath.intersected(water1)
        painter.setBrush(watercolor1)
        painter.drawPath(path)


        path = totalpath.intersected(water2)
        painter.setBrush(watercolor2)
        painter.drawPath(path)
        painter.restore()

        '''绘制字体'''
        m_font = QFont()
        m_font.setFamily('Microsoft YaHei')
        m_font.setPixelSize(int(self.width()/10))
        painter.setPen(Qt.white)
        painter.setFont(m_font)
        painter.drawText(self.rect(),Qt.AlignCenter,"{}%".format(self.per_num))
        painter.end()


    def timerEvent(self, event):

        self.per_num +=1
        if self.per_num ==101:
            self.per_num = 0
        self.update()



if __name__ =='__main__':
    import sys
    app =QApplication(sys.argv)
    win = chart_widget()
    win.show()
    sys.exit(app.exec())