#### 產生第二個視窗

### 但最後沒有使用到，結果數字出不來 = =

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'second.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QFormLayout
import cv2
import sys
from four import *
class Ui_Dialog(object):

###############視窗############################
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(307, 222)
        self.precision = QtWidgets.QLabel(Dialog)
        self.precision.setGeometry(QtCore.QRect(20, 20, 81, 31))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.precision.setFont(font)
        self.precision.setObjectName("precision")
        self.Recall = QtWidgets.QLabel(Dialog)
        self.Recall.setGeometry(QtCore.QRect(20, 60, 81, 31))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.Recall.setFont(font)
        self.Recall.setObjectName("Recall")
        self.f__measure = QtWidgets.QLabel(Dialog)
        self.f__measure.setGeometry(QtCore.QRect(20, 100, 81, 31))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.f__measure.setFont(font)
        self.f__measure.setObjectName("f__measure")
        self.MAE = QtWidgets.QLabel(Dialog)
        self.MAE.setGeometry(QtCore.QRect(20, 140, 81, 31))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.MAE.setFont(font)
        self.MAE.setObjectName("MAE")
        self.time = QtWidgets.QLabel(Dialog)
        self.time.setGeometry(QtCore.QRect(20, 180, 81, 31))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.time.setFont(font)
        self.time.setObjectName("time")
        self.precision_out = QtWidgets.QLineEdit(Dialog)
        self.precision_out.setGeometry(QtCore.QRect(120, 20, 161, 31))
        self.precision_out.setObjectName("precision_out")
        self.recall_out = QtWidgets.QLineEdit(Dialog)
        self.recall_out.setGeometry(QtCore.QRect(120, 60, 161, 31))
        self.recall_out.setObjectName("recall_out")
        self.f_measure_out = QtWidgets.QLineEdit(Dialog)
        self.f_measure_out.setGeometry(QtCore.QRect(120, 100, 161, 31))
        self.f_measure_out.setObjectName("f_measure_out")
        self.MAE_out = QtWidgets.QLineEdit(Dialog)
        self.MAE_out.setGeometry(QtCore.QRect(120, 140, 161, 31))
        self.MAE_out.setObjectName("MAE_out")
        self.time_out = QtWidgets.QLineEdit(Dialog)
        self.time_out.setGeometry(QtCore.QRect(120, 180, 161, 31))
        self.time_out.setObjectName("time_out")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.precision.setText(_translate("Dialog", "Precision"))
        self.Recall.setText(_translate("Dialog", "Recall"))
        self.f__measure.setText(_translate("Dialog", "F-measure"))
        self.MAE.setText(_translate("Dialog", "MAE"))
        self.time.setText(_translate("Dialog", "Time"))

##################功能################################
    def showResult(self, p, r, f, m, t):
        self.precision_out.setText('%.2f' % p)
        self.recall_out.setText('%.2f' % r)
        self.f_measure_out.setText('%.2f' % f)
        self.MAE_out.setText('%.2f' % m)
        self.time_out.setText('%.2f' % t)


# if __name__ == "__main__":
#    app = QtWidgets.QApplication(sys.argv)
#    ex = Ui_Dialog()
#    w = QtWidgets.QMainWindow()
#    ex.setupUi(w)
#    w.show()
#    sys.exit(app.exec_())   