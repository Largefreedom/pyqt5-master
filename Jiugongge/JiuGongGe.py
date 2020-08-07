import numpy  as np
import cv2
import os
from PyQt5.QtWidgets import *

class GUI_mian(QWidget):
    def __init__(self,parent = None):
        super(GUI_mian,self).__init__(parent)
        self.parent = parent
        # 设置窗口大小
        self.resize(250,500)
        self.open_file_path =None
        self.save_file_path =None
        self.open_pushbutton = QPushButton(self)
        self.open_pushbutton.setText("打开图片")
        self.open_pushbutton.setGeometry(50,100,60,20)
        self.open_pushbutton.clicked.connect(self.open_origin_file)

        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText('图片地址')
        self.line_edit.setGeometry(50,140,150,20)

        self.save_pushbutton = QPushButton(self)
        self.save_pushbutton.setText("保存至")
        self.save_pushbutton.setGeometry(50, 250, 60, 20)
        self.save_pushbutton.clicked.connect(self.save_file)

        self.line_edit1 = QLineEdit(self)
        self.line_edit1.setPlaceholderText('变换后图片存储地址')
        self.line_edit1.setGeometry(50, 300, 150, 20)

        self.start_pushbutton = QPushButton(self)
        self.start_pushbutton.setText("开始转换")
        self.start_pushbutton.setGeometry(50,370,60,20)
        self.start_pushbutton.clicked.connect(self.start_convert)

    def open_origin_file(self):
        open_file = QFileDialog.getOpenFileName(None,"Open File","C:/","Image (*.png)")
        if open_file[0]:
            print(open_file[0])
            self.open_file_path = open_file[0]
            self.line_edit.setText(self.open_file_path)
        else:
            print('222222222')
            QMessageBox.warning(self,"info","Fail to open file, please try it again!")

    def save_file(self):

        open_file = QFileDialog.getExistingDirectory(None,'Open File','C:/')
        if open_file:
            print(open_file)
            self.save_file_path = open_file
            self.line_edit1.setText(str(self.save_file_path))
        else:
            QMessageBox.warning(self,'info','Fail to open file, Please try it again!')

    def start_convert(self):
        if self.open_file_path and self.save_file_path:
            print('11111111')
            try:
                img = cv2.imread(self.open_file_path)
                if len(img.shape) == 2: # 判断是否为灰度图
                    last_dim = 1
                else:
                    last_dim = 3
                if img.shape[0] != img.shape[1]:
                    # 长宽不一致
                    new_image = np.zeros([max(img.shape), max(img.shape), last_dim], dtype=np.uint8) + 255

                    # 图像填充
                    new_image[
                    int((new_image.shape[0] - img.shape[0]) / 2):img.shape[0] + int((new_image.shape[0] - img.shape[0]) / 2),
                    int((new_image.shape[1] - img.shape[1]) / 2):img.shape[1] + int((new_image.shape[1] - img.shape[1]) / 2),:] = img
                else:
                    new_image = img
                # 开始进行图像分割
                col_width = int(new_image.shape[0] / 3)

                # 得到九宫格图像
                image_list = [new_image[i * col_width:(i + 1) * col_width, j * (col_width):(j + 1) * col_width, :] for i in
                              range(3) for j in range(3)]
                for i in range(9):
                    image_name = str(i)
                    save_image_path = os.path.join(self.save_file_path, f'{image_name}.png')
                    cv2.imwrite(save_image_path, np.array(image_list[i]))
                    print(f'save {image_name} sucessfully!')
                QMessageBox.information(self,'info','转换完成！')
            except Exception as e:
                print(e)
                QMessageBox.warning(self,'error',f'转换失败{str(e)}')
        else:
            QMessageBox.information(self,'err','文件为空，请重新操作')


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    widget = GUI_mian()
    widget.show()
    sys.exit(app.exec())
