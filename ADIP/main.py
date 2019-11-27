from windows import *
# from second import *
from PyQt5.QtWidgets import QApplication,QMainWindow,QDialog
import sys

class parentWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)
    # def GetValue(self):
    #     return self.main_ui.GetEvaluate()

# class childWindow(QDialog):
#     def __init__(self):
#         QDialog.__init__(self)
#         self.child = Ui_Dialog()
#         self.child.setupUi(self)
        # self.child.test()
    # def showWindows(self, p, r, f, m, t):
    #     self.child.showResult(p, r, f, m, t)

if __name__=='__main__':

    app=QApplication(sys.argv)
    window=parentWindow()
    # childW=childWindow()

    # btn=window.main_ui.pushButton_2
    # btn.clicked.connect(childW.show)

    # p,r,f,mae, time = window.GetValue()
    # childW.showWindows(p,r,f,mae, time)

    window.show()
    sys.exit(app.exec_())
