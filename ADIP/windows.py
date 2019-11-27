# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'four.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
import cv2
import sys
from keras.models import Model, load_model
from Evaluation import *
import time
from model import *
from Remove import *


class Ui_MainWindow(object):

    ##########初始化圖片###########

    def __init__(self):
        self.start = 0.0
        self.end = 0.0
        self.oriImage = None
        self.predImage = None
        self.background = None
        self.mergeImg = None
        self.labelImg = None
        self.width = None
        self.height = None
        self.channel = None
        self.widthBg = None
        self.heightBg = None
        self.channelBg = None
        self.recall = 0.0
        self.precision = 0.0
        self.f1 = 0.0
        self.mae = 0.0
        
    def setupUi(self, MainWindow):
        print("loading Model ~~~~")
        # self.model = load_model('./Weight/model-person_seg.h5', custom_objects={'mean_iou': mean_iou})
        self.model = load_model('./Weight/modelModify-person_testSeg.h5', custom_objects={'mean_iou': mean_iou})    #### 權重讀取
        print("loading end!!")
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1193, 996)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.slect_image = QtWidgets.QPushButton(self.centralwidget)
        self.slect_image.setGeometry(QtCore.QRect(10, 10, 131, 41))
        font = QtGui.QFont()
        font.setFamily("標楷體")
        font.setPointSize(14)
        self.slect_image.setFont(font)
        self.slect_image.setObjectName("slect_image")
        self.image = QtWidgets.QLabel(self.centralwidget)
        self.image.setGeometry(QtCore.QRect(10, 50, 581, 361))
        self.image.setFrameShape(QtWidgets.QFrame.Box)
        self.image.setFrameShadow(QtWidgets.QFrame.Plain)
        self.image.setText("")
        self.image.setObjectName("image")
        self.remove = QtWidgets.QPushButton(self.centralwidget)
        self.remove.setGeometry(QtCore.QRect(10, 420, 131, 41))
        font = QtGui.QFont()
        font.setFamily("標楷體")
        font.setPointSize(14)
        self.remove.setFont(font)
        self.remove.setObjectName("remove")
        self.image_3 = QtWidgets.QLabel(self.centralwidget)
        self.image_3.setGeometry(QtCore.QRect(10, 460, 581, 361))
        self.image_3.setFrameShape(QtWidgets.QFrame.Box)
        self.image_3.setText("")
        self.image_3.setObjectName("image_3")
        self.compose = QtWidgets.QPushButton(self.centralwidget)
        self.compose.setGeometry(QtCore.QRect(600, 420, 131, 41))
        font = QtGui.QFont()
        font.setFamily("標楷體")
        font.setPointSize(14)
        self.compose.setFont(font)
        self.compose.setObjectName("compose")
        self.image_2 = QtWidgets.QLabel(self.centralwidget)
        self.image_2.setGeometry(QtCore.QRect(600, 50, 581, 361))
        self.image_2.setFrameShape(QtWidgets.QFrame.Box)
        self.image_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.image_2.setText("")
        self.image_2.setObjectName("image_2")
        self.slect_scape = QtWidgets.QPushButton(self.centralwidget)
        self.slect_scape.setGeometry(QtCore.QRect(600, 10, 131, 41))
        font = QtGui.QFont()
        font.setFamily("標楷體")
        font.setPointSize(14)
        self.slect_scape.setFont(font)
        self.slect_scape.setObjectName("slect_scape")
        self.image_4 = QtWidgets.QLabel(self.centralwidget)
        self.image_4.setGeometry(QtCore.QRect(600, 460, 581, 361))
        self.image_4.setFrameShape(QtWidgets.QFrame.Box)
        self.image_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.image_4.setText("")
        self.image_4.setObjectName("image_4")
        #self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        #self.pushButton.setGeometry(QtCore.QRect(740, 420, 121, 41))
        #font = QtGui.QFont()
        #font.setFamily("標楷體")
        #font.setPointSize(14)
        #self.pushButton.setFont(font)
        #self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 420, 131, 41))
        #font = QtGui.QFont()
        #font.setFamily("標楷體")
        #font.setPointSize(14)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.slect_label = QtWidgets.QPushButton(self.centralwidget)
        self.slect_label.setGeometry(QtCore.QRect(150, 10, 131, 41))
        font = QtGui.QFont()
        font.setFamily("標楷體")
        font.setPointSize(14)
        self.slect_label.setFont(font)
        self.slect_label.setObjectName("slect_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1193, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.precision = QtWidgets.QLabel(self.centralwidget)
        self.precision.setGeometry(QtCore.QRect(10, 840, 81, 31))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.precision.setFont(font)
        self.precision.setObjectName("precision")
        self.precision_out = QtWidgets.QLineEdit(self.centralwidget)
        self.precision_out.setGeometry(QtCore.QRect(100, 840, 161, 31))
        self.precision_out.setObjectName("precision_out")
        self.Recall = QtWidgets.QLabel(self.centralwidget)
        self.Recall.setGeometry(QtCore.QRect(10, 880, 81, 31))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.Recall.setFont(font)
        self.Recall.setObjectName("Recall")
        self.recall_out = QtWidgets.QLineEdit(self.centralwidget)
        self.recall_out.setGeometry(QtCore.QRect(100, 880, 161, 31))
        self.recall_out.setObjectName("recall_out")
        self.f__measure = QtWidgets.QLabel(self.centralwidget)
        self.f__measure.setGeometry(QtCore.QRect(280, 840, 81, 31))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.f__measure.setFont(font)
        self.f__measure.setObjectName("f__measure")
        self.f_measure_out = QtWidgets.QLineEdit(self.centralwidget)
        self.f_measure_out.setGeometry(QtCore.QRect(370, 840, 161, 31))
        self.f_measure_out.setObjectName("f_measure_out")
        self.MAE = QtWidgets.QLabel(self.centralwidget)
        self.MAE.setGeometry(QtCore.QRect(280, 880, 81, 31))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.MAE.setFont(font)
        self.MAE.setObjectName("MAE")
        self.time = QtWidgets.QLabel(self.centralwidget)
        self.time.setGeometry(QtCore.QRect(10, 920, 81, 31))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.time.setFont(font)
        self.time.setObjectName("time")
        self.f_measure_out_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.f_measure_out_2.setGeometry(QtCore.QRect(370, 880, 161, 31))
        self.f_measure_out_2.setObjectName("f_measure_out_2")
        self.time_out = QtWidgets.QLineEdit(self.centralwidget)
        self.time_out.setGeometry(QtCore.QRect(100, 920, 161, 31))
        self.time_out.setObjectName("time_out")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1193, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)     

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

##########################功能#############################################

        self.slect_image.clicked.connect(self.setImage) ##放置圖片(主)

        self.slect_scape.clicked.connect(self.setscape) ##放置風景

        self.remove.clicked.connect(self.Remove)    ##去背

        self.compose.clicked.connect(self.Merge)   ## 合成背景

        self.pushButton_2.clicked.connect(self.Evaluate)    ## 評估

        self.slect_label.clicked.connect(self.setLabel)   ## 選擇 Label


################------------功能定義-------------------------------#################
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ADIP期末專案"))
        self.slect_image.setText(_translate("MainWindow", "選擇圖片"))
        self.remove.setText(_translate("MainWindow", "人物去背"))
        self.compose.setText(_translate("MainWindow", "合成圖片"))
        self.slect_scape.setText(_translate("MainWindow", "選擇風景"))
        #self.pushButton.setText(_translate("MainWindow", "保存合成圖"))
        self.pushButton_2.setText(_translate("MainWindow", "評估"))
        self.slect_label.setText(_translate("MainWindow", "選擇Label"))
        self.precision.setText(_translate("MainWindow", "Precision"))
        self.Recall.setText(_translate("MainWindow", "Recall"))
        self.f__measure.setText(_translate("MainWindow", "F-measure"))
        self.MAE.setText(_translate("MainWindow", "MAE"))
        self.time.setText(_translate("MainWindow", "Time"))

    def setImage(self):
        self.oriImage = 0
        fileName, _= QtWidgets.QFileDialog.getOpenFileName(None,"選擇圖片", "","Image Files (*.png *.jpg *jpeg *.bmp)")
        if fileName:
            print(fileName)
            img = cv2.imread(fileName)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # img = imageDetection(img)
            # print(img.shape[0], img.shape[1])
            self.height, self.width, self.channel = img.shape
            self.oriImage = img
            Qimg = QtGui.QImage(img.data, self.width, self.height, self.channel*self.width, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(Qimg)
            pixmap = pixmap.scaled(self.image.width(), self.image.height(), QtCore.Qt.KeepAspectRatio)
            self.image.setPixmap(pixmap)
            self.image.setAlignment(QtCore.Qt.AlignCenter)    
    
    def setscape(self):
        fileName, _= QtWidgets.QFileDialog.getOpenFileName(None,"選擇圖片", "","Image Files (*.png *.jpg *jpeg *.bmp)")
        if fileName:
            img = cv2.imread(fileName)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.background = img
            self.heightBg, self.widthBg, self.channelBg = self.background.shape
            Qimg = QtGui.QImage(img.data, self.widthBg, self.heightBg, self.channelBg*self.widthBg, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(Qimg)
            pixmap = pixmap.scaled(self.image_2.width(), self.image_2.height(), QtCore.Qt.KeepAspectRatio)
            self.image_2.setPixmap(pixmap)
            self.image_2.setAlignment(QtCore.Qt.AlignCenter)    

    def setLabel(self):
        fileName, _= QtWidgets.QFileDialog.getOpenFileName(None,"選擇圖片", "","Image Files (*.png *.jpg *jpeg *.bmp)")
        if fileName:
            img = cv2.imread(fileName)
            self.labelImg = img
    
    def Remove(self):
        self.start = time.time()
        pmap = removeBackground(self.oriImage, self.model)
        self.end = time.time()
        self.predImage = pmap
        Qimg = QtGui.QImage(pmap.data, self.width, self.height, self.channel*self.width, QImage.Format_RGB888)
        pmap = QPixmap.fromImage(Qimg)
        pmap = pmap.scaled(self.image.width(), self.image.height(), QtCore.Qt.KeepAspectRatio)           
        self.image_3.setPixmap(pmap)
        self.image_3.setAlignment(QtCore.Qt.AlignCenter)

    def Merge(self):
        self.mergeImg = MergeBackground(self.oriImage, self.background, self.predImage)
        Qimg = QtGui.QImage(self.mergeImg.data, self.width, self.height, self.channel*self.width, QImage.Format_RGB888)
        pmap = QPixmap.fromImage(Qimg)
        pmap = pmap.scaled(self.image.width(), self.image.height(), QtCore.Qt.KeepAspectRatio)           
        self.image_4.setPixmap(pmap)
        self.image_4.setAlignment(QtCore.Qt.AlignCenter)
     
    def Evaluate(self):
        self.precision, self.recall, self.f1 = Precision_Recall(self.labelImg, self.predImage, self.height, self.width, self.channel)
        self.mae = MAE(self.labelImg, self.predImage, self.height, self.width, self.channel)
        self.precision_out.setText('%.4f' % self.precision)
        self.recall_out.setText('%.4f' % self.recall)
        self.f_measure_out.setText('%.4f' % self.f1)
        self.f_measure_out_2.setText('%.4f' % self.mae)
        self.time_out.setText('%.4f' % (self.end - self.start))

    # def GetEvaluate(self):
    #     total_time = self.end - self.start
    #     print(self.precision, self.recall, self.f1, self.mae)
    #     return self.precision, self.recall, self.f1, self.mae, total_time
    
    # def showResult(self, p, r, f, m, t):
    #     self.precision_out.setText('%.2f' % self.precision)
    #     self.recall_out.setText('%.2f' % self.recall)
    #     self.f_measure_out.setText('%.2f' % self.f1)
    #     self.MAE_out.setText('%.2f' % self.mae)
    #     self.time_out.setText('%.2f' % t)


    # def save(self):
    #     filename = QFileDialog.getSaveFileName(self,'save file',"Image Files (*.png *.jpg *jpeg *.bmp)")
    #     self.predImage
    