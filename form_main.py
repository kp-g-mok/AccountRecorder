# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1600, 900)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("White_Background_Annuity.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.FileList = QtWidgets.QTabWidget(self.centralwidget)
        self.FileList.setAutoFillBackground(False)
        self.FileList.setTabsClosable(False)
        self.FileList.setMovable(True)
        self.FileList.setObjectName("FileList")
        self.gridLayout.addWidget(self.FileList, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1600, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuTab_Functions = QtWidgets.QMenu(self.menubar)
        self.menuTab_Functions.setObjectName("menuTab_Functions")
        self.menuAdd = QtWidgets.QMenu(self.menuTab_Functions)
        self.menuAdd.setObjectName("menuAdd")
        self.menuRemove = QtWidgets.QMenu(self.menuTab_Functions)
        self.menuRemove.setObjectName("menuRemove")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.act_New = QtWidgets.QAction(MainWindow)
        self.act_New.setObjectName("act_New")
        self.act_Open = QtWidgets.QAction(MainWindow)
        self.act_Open.setObjectName("act_Open")
        self.act_Close_Tab = QtWidgets.QAction(MainWindow)
        self.act_Close_Tab.setObjectName("act_Close_Tab")
        self.act_Exit = QtWidgets.QAction(MainWindow)
        self.act_Exit.setObjectName("act_Exit")
        self.act_Refresh = QtWidgets.QAction(MainWindow)
        self.act_Refresh.setObjectName("act_Refresh")
        self.actionClear_History = QtWidgets.QAction(MainWindow)
        self.actionClear_History.setObjectName("actionClear_History")
        self.act_Move_Link = QtWidgets.QAction(MainWindow)
        self.act_Move_Link.setObjectName("act_Move_Link")
        self.act_Import = QtWidgets.QAction(MainWindow)
        self.act_Import.setObjectName("act_Import")
        self.act_Open_Multiple = QtWidgets.QAction(MainWindow)
        self.act_Open_Multiple.setObjectName("act_Open_Multiple")
        self.act_Refresh_Accounts = QtWidgets.QAction(MainWindow)
        self.act_Refresh_Accounts.setObjectName("act_Refresh_Accounts")
        self.act_Add_Account = QtWidgets.QAction(MainWindow)
        self.act_Add_Account.setObjectName("act_Add_Account")
        self.act_Add_Entry = QtWidgets.QAction(MainWindow)
        self.act_Add_Entry.setObjectName("act_Add_Entry")
        self.act_Remove_Account = QtWidgets.QAction(MainWindow)
        self.act_Remove_Account.setObjectName("act_Remove_Account")
        self.act_Remove_Entry = QtWidgets.QAction(MainWindow)
        self.act_Remove_Entry.setObjectName("act_Remove_Entry")
        self.actiton_Change_Default_Directory = QtWidgets.QAction(MainWindow)
        self.actiton_Change_Default_Directory.setObjectName("actiton_Change_Default_Directory")
        self.act_Change_Default_Directory = QtWidgets.QAction(MainWindow)
        self.act_Change_Default_Directory.setObjectName("act_Change_Default_Directory")
        self.act_Change_Start_Date = QtWidgets.QAction(MainWindow)
        self.act_Change_Start_Date.setObjectName("act_Change_Start_Date")
        self.act_Change_Database_Type = QtWidgets.QAction(MainWindow)
        self.act_Change_Database_Type.setObjectName("act_Change_Database_Type")
        self.menuFile.addAction(self.act_New)
        self.menuFile.addAction(self.act_Open)
        self.menuFile.addAction(self.act_Close_Tab)
        self.menuFile.addAction(self.act_Change_Default_Directory)
        self.menuFile.addAction(self.act_Exit)
        self.menuAdd.addAction(self.act_Add_Account)
        self.menuAdd.addAction(self.act_Add_Entry)
        self.menuRemove.addAction(self.act_Remove_Account)
        self.menuRemove.addAction(self.act_Remove_Entry)
        self.menuTab_Functions.addAction(self.act_Refresh_Accounts)
        self.menuTab_Functions.addAction(self.act_Change_Start_Date)
        self.menuTab_Functions.addAction(self.menuAdd.menuAction())
        self.menuTab_Functions.addAction(self.menuRemove.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTab_Functions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuTab_Functions.setTitle(_translate("MainWindow", "Account Functions"))
        self.menuAdd.setTitle(_translate("MainWindow", "Add"))
        self.menuRemove.setTitle(_translate("MainWindow", "Remove"))
        self.act_New.setText(_translate("MainWindow", "New Account Database"))
        self.act_New.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.act_Open.setText(_translate("MainWindow", "Open Account Database"))
        self.act_Open.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.act_Close_Tab.setText(_translate("MainWindow", "Close Account Database"))
        self.act_Close_Tab.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.act_Exit.setText(_translate("MainWindow", "Exit"))
        self.act_Exit.setShortcut(_translate("MainWindow", "Ctrl+Shift+Q"))
        self.act_Refresh.setText(_translate("MainWindow", "Refresh"))
        self.act_Refresh.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.actionClear_History.setText(_translate("MainWindow", "Clear History"))
        self.actionClear_History.setShortcut(_translate("MainWindow", "Ctrl+Shift+H"))
        self.act_Move_Link.setText(_translate("MainWindow", "Move Item"))
        self.act_Move_Link.setShortcut(_translate("MainWindow", "Ctrl+X"))
        self.act_Import.setText(_translate("MainWindow", "Import"))
        self.act_Open_Multiple.setText(_translate("MainWindow", "Open Multiple"))
        self.act_Open_Multiple.setShortcut(_translate("MainWindow", "Ctrl+Shift+O, Ctrl+S"))
        self.act_Refresh_Accounts.setText(_translate("MainWindow", "Refresh Accounts"))
        self.act_Refresh_Accounts.setShortcut(_translate("MainWindow", "Ctrl+R, F5"))
        self.act_Add_Account.setText(_translate("MainWindow", "Add Account"))
        self.act_Add_Account.setShortcut(_translate("MainWindow", "Ctrl+Shift+A"))
        self.act_Add_Entry.setText(_translate("MainWindow", "Add Entry"))
        self.act_Add_Entry.setShortcut(_translate("MainWindow", "Ctrl+Shift+E"))
        self.act_Remove_Account.setText(_translate("MainWindow", "Remove Account"))
        self.act_Remove_Entry.setText(_translate("MainWindow", "Remove Entry"))
        self.actiton_Change_Default_Directory.setText(_translate("MainWindow", "Change Default Directory"))
        self.act_Change_Default_Directory.setText(_translate("MainWindow", "Change Default Directory"))
        self.act_Change_Start_Date.setText(_translate("MainWindow", "Change Account Database Start Date"))
        self.act_Change_Database_Type.setText(_translate("MainWindow", "Change Database Type"))

