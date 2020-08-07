from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image,ImageQt
import requests
import base64


class Ui_Form(QWidget):

    def __init__(self,api,keys,parent = None):
        super(Ui_Form,self).__init__(parent =None)
        self.api = api
        self.keys =keys
        self.setObjectName("Form")
        self.resize(606, 394)
        self.pushButton = QtWidgets.QPushButton("Open",self)
        self.pushButton.setGeometry(QtCore.QRect(30, 330, 60, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.open_file)

        self.pushButton_2 = QtWidgets.QPushButton("Convert",self)
        self.pushButton_2.setGeometry(QtCore.QRect(100, 330, 60, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.clicked.connect(self.get_date)

        self.pushButton_3 = QtWidgets.QPushButton("Save as.", self)
        self.pushButton_3.setGeometry(QtCore.QRect(180, 330, 60, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.clicked.connect(self.save_file)


        #两个图片标签；pic
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(30, 30, 231, 271))
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet("background-color:black;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel("",self)
        self.label_2.setGeometry(QtCore.QRect(360, 60, 171, 161))
        self.label_2.setStyleSheet("background-color:black;")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")


        self.widget = QtWidgets.QWidget(self)
        self.widget.setGeometry(QtCore.QRect(330, 270, 191, 111))
        self.widget.setObjectName("widget")
        self.formLayout = QtWidgets.QFormLayout(self.widget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")

        self.label_3 = QtWidgets.QLabel("年龄",self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setFont(font)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)

        self.label_4 = QtWidgets.QLabel("性别",self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setFont(font)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)


        self.label_5 = QtWidgets.QLabel("颜值",self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setFont(font)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_3)


        self.label_6 = QtWidgets.QLabel("脸型",self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_4)


    def open_file(self):
        file_name = QFileDialog.getOpenFileName(self,"Open file..","/",'all files:(*.png);;(*.jpg)')
        if file_name[0]:#File exits
            #clear the contend of label;
           self.label.clear()
           self.label_2.clear()
           self.file_name = file_name[0]
           print("file name: {}".format(str(self.file_name)))
           img = Image.open(self.file_name)
           pixmap = ImageQt.toqpixmap(img)
           self.label.setPixmap(pixmap)
           self.label.setScaledContents(True)
           self.pushButton_2.setEnabled(True)

        else:
            QMessageBox.warning(self,"waring","文件为空无法转换")

    def save_file(self):
        self.pushButton_3.setEnabled(True)
        name = QFileDialog.getSaveFileName(self,'Save file','/','png:(*.png);;jpg:(*.jpg)')
        if name[0]:
            img = ImageQt.fromqpixmap(self.crop_pixmap)
            img.save(str(name[0]))
            QMessageBox.information(self,'info','{} saved successfully'.format(str(name[0])))
        else:
            QMessageBox.warning(self,'error','{} saved failed'.format(str(name[0])))

    def get_token(self):
        get_token_url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(
            self.api, self.keys)
        try:
            res = requests.get(get_token_url).json()['access_token']
            return str(res)
        except:
            return 0

    def get_date(self):
        if self.file_name:
            params = {
                'image': str(base64.b64encode(open(self.file_name, 'rb').read()), 'utf-8'),
                'image_type': 'BASE64',
                'face_field': 'age,beauty,expression,face_shape,location,gender'
            }
            headers = {'content-type': 'application/json'}
            # 构造百度人脸检测请求url,获取token;,
            token = self.get_token()
            res_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect?access_token={}".format(str(token))
            res = requests.post(res_url, data=params, headers=headers)
            try:
                total_list = res.json()['result']['face_list']
                loacation = total_list[0]['location']
                left = int(loacation['left']) - 10
                upper = int(loacation['top']) - 10
                right = int(loacation['left']) + int(loacation['width']) + 10
                bottom = int(loacation['top'] + int(loacation['height'])) + 10
                img = Image.open(self.file_name).crop((left, upper, right, bottom))
                print(res.json())
                self.crop_pixmap = ImageQt.toqpixmap(img)
                self.label_2.setPixmap(self.crop_pixmap)
                self.label_2.setScaledContents(True)

                age = total_list[0]['age']
                print(age)
                self.lineEdit.setText(str(age))

                self.lineEdit.setAlignment(Qt.AlignCenter)
                gender = total_list[0]['gender']['type']
                print(gender)
                self.lineEdit_2.setText(str(gender))
                self.lineEdit_2.setAlignment(Qt.AlignCenter)
                beauty = total_list[0]['beauty']
                self.lineEdit_3.setText(str(beauty))
                self.lineEdit_3.setAlignment(Qt.AlignCenter)
                face_shape = total_list[0]['face_shape']['type']
                self.lineEdit_4.setText(str(face_shape))
                self.lineEdit_4.setAlignment(Qt.AlignCenter)



                # Save pushbutton 保存一致；
                self.pushButton_3.setEnabled(True)

            except:
                QMessageBox.warning(self,'error','Face recognise failed!')
        else:
            QMessageBox.information(self,'info','The file path of pic is not exist!')


if __name__ =='__main__':
    import sys
    api ='FklIzzed77H5RuqHYUcufYdg'
    keys ='TRf4Es2rRuL2riVfo5RgXYi5FctXmOxB'
    app =QtWidgets.QApplication(sys.argv)
    window = Ui_Form(api,keys)
    window.show()
    sys.exit(app.exec_())