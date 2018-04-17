from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDockWidget, QListWidget
from PyQt5.QtGui import *
import sys
import time
import serial
from wind import *
class CampVID(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tr = 1
        self.recod = 0
        self.cap_1 = cv2.VideoCapture(0)
        self.cap_2 = cv2.VideoCapture(1)
        self.cap_3 = cv2.VideoCapture(2)
    def run(self):
        cap1_out, cap2_out, cap3_out = self.initVIDfile()
        ui.testWay.clicked.connect(self.qt)
        ui.closecam.clicked.connect(self.quit)
        ui.camdev.clicked.connect(self.reopen)
        ui.startVID.clicked.connect(self.recordVID)
        ui.stopVID.clicked.connect(self.stopVID)
        while True:
            if self.tr == 1:
                if int(time.strftime("%S")) == 0:
                    if int(time.strftime("%M")) == 0:
                        cap1_out, cap2_out, cap3_out = self.renameVIDflie()
                ret1,img_1 = self.cap_1.read()
                if ret1:
                    if self.recod:
                        cap1_out.write(img_1)
                        print("正在存储视频...")
                    cap_1_img = self.opencv2qtpic(img_1)
                    ui.cam1.setPixmap(cap_1_img)
                    time.sleep(0.05)
                if ret1 !=1:
                    self.cap_1 = cv2.VideoCapture(0)
                ret2,img_2 = self.cap_2.read()
                if ret2:
                    if self.recod:
                        cap2_out.write(img_2)
                    cap_2_img = self.opencv2qtpic(img_2)
                    ui.cam2.setPixmap(cap_2_img)
                    time.sleep(0.05)
                if ret2 !=1:
                    self.cap_2 = cv2.VideoCapture(1)
                ret3,img_3 = self.cap_3.read()
                if ret3:
                    if self.recod:
                        cap3_out.write(img_3)
                    cap_3_img = self.opencv2qtpic(img_3)
                    ui.cam3.setPixmap(cap_3_img)
                    time.sleep(0.05)
                if ret3 !=1:
                    self.cap_3 = cv2.VideoCapture(2)
                self.disptime()
            else:
                self.disptime()
                time.sleep(0.8)
    def opencv2qtpic(self,img):
        height, width, bytesPerComponent = img.shape
        bytesPerLine = 3 * width
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
        QImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(QImg)
        return pixmap
    def quit(self):
        self.tr=0
        time.sleep(0.1)
        self.cap_1.release()
        self.cap_2.release()
        self.cap_3.release()
        ui.cam1.setText("关闭摄像头A")
        ui.cam2.setText( "关闭摄像头B")
        ui.cam3.setText( "关闭摄像头C")
    def reopen(self):
        self.quit()
        time.sleep(0.5)
        self.cap_1 = cv2.VideoCapture(0)
        self.cap_2 = cv2.VideoCapture(1)
        self.cap_3 = cv2.VideoCapture(2)
        self.tr = 1
    def recordVID(self):
        self.recod = 1
    def stopVID(self):
        self.recod = 0
    def renameVIDflie(self):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        VID_1 = 'D:\camp\AA\AA_' + time.strftime( '%m%d%H%M') + '.avi'
        VID_2 = 'D:\camp\BB\BB_' + time.strftime( '%m%d%H%M') + '.avi'
        VID_3 = 'D:\camp\CC\CC_' + time.strftime( '%m%d%H%M') + '.avi'
        cap1_out = cv2.VideoWriter( VID_1,fourcc, 20.0, (640,480))
        cap2_out = cv2.VideoWriter( VID_2,fourcc, 20.0, (640,480))
        cap3_out = cv2.VideoWriter( VID_3,fourcc, 20.0, (640,480))
        return cap1_out, cap2_out, cap3_out
    def initVIDfile(self):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        VID_1  = 'D:\camall\AA\AA_' + time.strftime("%m%d%H%M")+'.avi'
        VID_2 = 'D:\camall\BB\BB_' + time.strftime( '%m%d%H%M') + '.avi'
        VID_3 = 'D:\camall\CC\CC_' + time.strftime( '%m%d%H%M') + '.avi'
        cap1_out = cv2.VideoWriter( VID_1,fourcc, 20.0, (640,480))
        cap2_out = cv2.VideoWriter( VID_2,fourcc, 20.0, (640,480))
        cap3_out = cv2.VideoWriter( VID_3,fourcc, 20.0, (640,480))
        return cap1_out, cap2_out, cap3_out
    def disptime(self):
        ui.timelable.setText( str(time.strftime("%Y-%m-%d %H:%M:%S")))
    def qt(self):
        try:
            NowCom = ui.comboBox.currentText()
            self.ser = serial.Serial(NowCom, 115200)
            self.ser.write(b'$00022123&')
            time.sleep(3)
            try:
                testdate = self.ser.inWaiting()
                testReslt = int(str(self.ser.read(testdate))[-10:-2]) / 100
                print(testReslt)
                self.ser.flushInput()
                ui.testWay_2.display(str(testReslt))
                self.ser.close()
            except:
                self.ser.flushInput()
                self.ser.close()
                pass
        except:
            pass
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    thread = CampVID()
    thread.start()
    sys.exit(app.exec_())
