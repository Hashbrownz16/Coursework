import sys
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
import sqlFunctions #library of my sql things which I need, in the future I should move this to a whole file
#It is important to know I plan to move this file in to a main file as another separate library/module

win1 = uic.loadUiType("coursework.ui")[0]

class WindowClass(QtWidgets.QMainWindow, win1):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.labourerHire)
        self.pushButton_2.clicked.connect(self.labourerRegistration)
        self.pushButton_3.clicked.connect(self.viewOrders)
    def labourerHire(self):
        print("hire")
        
        
    def labourerRegistration(self):
        print("reg")
        
    def viewOrders(self):
        print("order")
    


app = QtWidgets.QApplication(sys.argv)
win1 = WindowClass(None)

win1.show()
app.exec_()
