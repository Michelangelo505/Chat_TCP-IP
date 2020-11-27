# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainChatRoom.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(823, 690)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ListUsers = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.ListUsers.setGeometry(QtCore.QRect(643, 10, 171, 541))
        self.ListUsers.setObjectName("ListUsers")
        self.ChatRoom = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.ChatRoom.setGeometry(QtCore.QRect(10, 10, 621, 541))
        self.ChatRoom.setObjectName("ChatRoom")
        self.MessageWindow = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.MessageWindow.setGeometry(QtCore.QRect(10, 570, 621, 70))
        self.MessageWindow.setObjectName("MessageWindow")
        self.pushButtonSend = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSend.setGeometry(QtCore.QRect(640, 570, 171, 71))
        self.pushButtonSend.setObjectName("pushButtonSend")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 823, 22))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuMenu.addAction(self.actionExit)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButtonSend.setText(_translate("MainWindow", "Send"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
