import sys
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
import sqlFunctions #library of my sql things which I need, in the future I should move this to a whole file
#It is important to know I plan to move this file in to a main file as another separate library/module

#Initialise my first windows here and then initialise each one inside of the class function as my program branches off
#in more than one direction
win1 = uic.loadUiType("coursework.ui")[0]
win2 = uic.loadUiType("labourerHire.ui")[0]
win3 = uic.loadUiType("labourerReg.ui")[0]
win4 = uic.loadUiType("viewOrder.ui")[0]

class RegScreen(QtWidgets.QMainWindow, win1): #I could make one super big class and stuff everything in there, but 
    def __init__(self, parent=None): #that way I need to be super careful about what I name my objects.
        QtWidgets.QMainWindow.__init__(self, parent) #Making a separate class which is initialized by this first class
        self.setupUi(self) #makes it slightly easier for me to switch screens
        self.pushButton.clicked.connect(self.labourerHire) 
        self.pushButton_2.clicked.connect(self.labourerRegistration)
        self.pushButton_3.clicked.connect(self.viewOrders)
    def labourerHire(self):
        print("hire")
        win1.hide()
        win2.show()
        
    def labourerRegistration(self):
        print("reg")
        win1.hide()
        win3.show()
      
    def viewOrders(self):
        print("order")
        win1.hide()
        win3.show()

class LabourerHire(QtWidgets.QMainWindow,win2):
    def __init__(self, parent=None): #I don't need any methods from other classes, so this is OK probably
        QtWidgets.QMainWindow.__init__(self, parent=None)
        self.setupUi(self)
        self.comboBox.addItem("Electrician")
        self.comboBox.addItem("Plumber")
        self.pushButton.clicked.connect(self.searchDatabase)
    def searchDatabase(self):
        jobType = self.comboBox.currentText()
        labourerID = sqlFunctions.getLabourersWithJob(jobType,sqlFunctions.database)

        
        
        

        
class LabourerReg(QtWidgets.QMainWindow,win3):
    def __init__(self,parent=None):
        QtWidgets.QMainWindow.__init__(self,parent=None)
        self.setupUi(self)
        self.comboBox.addItem("Electrician")
        self.comboBox.addItem("Plumber")
        self.pushButton.clicked.connect(self.newLabourer)
    def newLabourer(self):
        name = self.textEditName.toPlainText()
        wage = self.textEditWage.toPlainText()
        number = self.textEditNumber.toPlainText()
        number = number.replace(" ","")
        jobType = sef.comboBox.currentText()
        
        


class ViewOrder(QtWidgets.QMainWindow,win4):
    def __init__(self,parent=None):
        QtWidgets.QMainWindow.__init__(self,parent=None)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.updateTable)
    def updateTable(self):
        contents = self.textEdit.toPlainText()
        command = "SELECT OrderStart FROM Orders WHERE CustomerID ="+"'"+contents+"'" #come back to this later, it isn't essential for now
        pass
        
        



app = QtWidgets.QApplication(sys.argv)
win1 = RegScreen(None) #all windows are hidden by default
win2 = LabourerHire(None)
win3 = LabourerReg(None)
win4 = ViewOrder(None)

win3.show()
app.exec_()
