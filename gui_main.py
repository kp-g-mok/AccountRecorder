import os
import sys

from PyQt5 import QtCore, QtWidgets, QtGui

from config_file_api import Config
from account_database_api import Database
from static_functions import error_message

from gui_frame import Frame
from gui_add_remove_account_group import AddRemoveAccountGroup
from gui_get_start_date import GetStartDate
from gui_add_remove_account import AddRemoveAccount

__author__ = 'Gareth Mok'


class Main():
    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        
        self.last_session = Config('last_open.json')
        if getattr(sys, 'frozen', False):  # frozen
            self.directory = os.path.dirname(os.path.realpath(sys.executable))
        else:  # unfrozen
            self.directory = os.path.dirname(os.path.realpath(__file__))
        
        filename = self.last_session.get_prev_database()
        if not filename or not os.path.isfile(filename):
            filename = QtGui.QFileDialog.getSaveFileName(QtGui.QFileDialog(), 'New database file', self.directory, '*.fs')[0]
        if not filename:
            sys.exit()
        
        self.database = Database(filename)
        self.last_session.set_prev_database(filename)

    def start_app(self):
        try:
            with self.database as db:      
                my_window = MainWindow(self.directory, self.last_session, db, None)
                my_window.show()
                my_window.act_refresh_accounts_triggered()
                sys.exit(self.app.exec_())
        except SystemExit:
            pass


class MainWindow(QtGui.QMainWindow):
    def __init__(self, directory: str, last_session: Config, database: Database, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.directory = directory
        self.last_session = last_session
        self.database = database
        
        self.clear_and_fill_tabs()
        self.connect_components()
        self.initialize_shortcuts()

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
        
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.act_New = QtWidgets.QAction(MainWindow)
        self.act_New.setObjectName("act_New")
        self.act_Open = QtWidgets.QAction(MainWindow)
        self.act_Open.setObjectName("act_Open")
        self.act_Add_Account_Group = QtWidgets.QAction(MainWindow)
        self.act_Add_Account_Group.setObjectName("act_Add_Account_Group")
        self.act_Remove_Account_Group = QtWidgets.QAction(MainWindow)
        self.act_Remove_Account_Group.setObjectName("act_Remove_Account_Group")
        self.act_Exit = QtWidgets.QAction(MainWindow)
        self.act_Exit.setObjectName("act_Exit")
        self.act_Refresh_Accounts = QtWidgets.QAction(MainWindow)
        self.act_Refresh_Accounts.setObjectName("act_Refresh_Accounts")
        self.act_Add_Account = QtWidgets.QAction(MainWindow)
        self.act_Add_Account.setObjectName("act_Add_Account")
        self.act_Remove_Account = QtWidgets.QAction(MainWindow)
        self.act_Remove_Account.setObjectName("act_Remove_Account")
        self.act_Change_Start_Date = QtWidgets.QAction(MainWindow)
        self.act_Change_Start_Date.setObjectName("act_Change_Start_Date")
        self.menuFile.addAction(self.act_New)
        self.menuFile.addAction(self.act_Open)
        self.menuFile.addAction(self.act_Add_Account_Group)
        self.menuFile.addAction(self.act_Remove_Account_Group)
        self.menuFile.addAction(self.act_Exit)
        self.menuTab_Functions.addAction(self.act_Refresh_Accounts)
        self.menuTab_Functions.addAction(self.act_Change_Start_Date)
        self.menuTab_Functions.addAction(self.act_Add_Account)
        self.menuTab_Functions.addAction(self.act_Remove_Account)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTab_Functions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuTab_Functions.setTitle(_translate("MainWindow", "Account Functions"))
        self.act_New.setText(_translate("MainWindow", "New Account Database"))
        self.act_New.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.act_Open.setText(_translate("MainWindow", "Open Account Database"))
        self.act_Open.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.act_Add_Account_Group.setText(_translate("MainWindow", "Add Account Group"))
        self.act_Add_Account_Group.setShortcut(_translate("MainWindow", "Ctrl+Shift+N"))
        self.act_Remove_Account_Group.setText(_translate("MainWindow", "Remove Account Group"))
        self.act_Exit.setText(_translate("MainWindow", "Exit"))
        self.act_Exit.setShortcut(_translate("MainWindow", "Ctrl+Shift+X"))
        self.act_Refresh_Accounts.setText(_translate("MainWindow", "Refresh Accounts"))
        self.act_Refresh_Accounts.setShortcut(_translate("MainWindow", "Ctrl+R, F5"))
        self.act_Add_Account.setText(_translate("MainWindow", "Add account"))
        self.act_Add_Account.setShortcut(_translate("MainWindow", "Ctrl+Shift+A"))
        self.act_Remove_Account.setText(_translate("MainWindow", "Remove account"))
        self.act_Change_Start_Date.setText(_translate("MainWindow", "Change Account Start Date"))

    def clear_and_fill_tabs(self):
        self.FileList.clear()
        account_list = sorted(self.database.grab_account_group_names())
        for name in account_list:
            new_tab = Frame(self.database.get_account_group(name), self)
            self.FileList.addTab(new_tab, name)
            self.act_refresh_accounts_triggered()

        if self.FileList.currentWidget():
            self.FileList.currentWidget().tableAccountData.setFocus()

    def connect_components(self):
        self.act_New.triggered.connect(self.act_new_triggered)
        self.act_Open.triggered.connect(self.act_open_triggered)
        self.act_Add_Account_Group.triggered.connect(self.act_add_account_group_triggered)
        self.act_Remove_Account_Group.triggered.connect(self.act_remove_account_group_triggered)
        self.act_Change_Start_Date.triggered.connect(self.act_change_start_date_triggered)
        self.act_Exit.triggered.connect(self.act_exit_triggered)
        self.act_Refresh_Accounts.triggered.connect(self.act_refresh_accounts_triggered)
        self.act_Add_Account.triggered.connect(self.act_add_account_triggered)
        self.act_Remove_Account.triggered.connect(self.act_remove_account_triggered)
        self.FileList.currentChanged.connect(self.act_refresh_accounts_triggered)

    def initialize_shortcuts(self):
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Tab),
                        self, self.next_tab)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.SHIFT + QtCore.Qt.Key_Tab),
                        self, self.previous_tab)

    def next_tab(self):
        new_index = (self.FileList.currentIndex() + 1) % self.FileList.count()
        self.FileList.setCurrentIndex(new_index)

    def previous_tab(self):
        new_index = self.FileList.currentIndex() - 1
        if new_index == -1:
            new_index = self.FileList.count() - 1
        self.FileList.setCurrentIndex(new_index)

    def act_exit_triggered(self):
        self.close()

    def act_new_triggered(self):
        """ Create a new account database file and set it as the current database
        """
        filename = QtGui.QFileDialog.getSaveFileName(QtGui.QFileDialog(), 'New database file', self.directory, '*.fs')[0]
        if filename != '':
            self.database.__exit__(None, None, None)
            self.database = Database(filename).__enter__()
            self.clear_and_fill_tabs()
            self.last_session.set_prev_database(filename)        

    def act_open_triggered(self):
        """ Select a account database file and set it as the current database
        """
        filename = QtGui.QFileDialog.getOpenFileName(QtGui.QFileDialog(), 'Open database file', self.directory, '*.fs')[0]
        if filename != '':
            self.database.__exit__(None, None, None)
            self.database = Database(filename).__enter__()
            self.clear_and_fill_tabs()
            self.last_session.set_prev_database(filename)

    def act_add_account_group_triggered(self):
        current_account_groups = self.database.grab_account_group_names()
        name, start_date, account_group_type, ok = AddRemoveAccountGroup.get_account_group_details(
            current_account_groups, False, self)
        if ok and name and start_date:            
            if name not in current_account_groups:
                try:
                    # if the entered group is new, add it to the database
                    new_account_group = self.database.get_account_group(name)
                    new_account_group.set_type(account_group_type)
                    new_account_group.set_start_date(start_date)

                    new_tab = Frame(new_account_group, self)

                    self.FileList.addTab(new_tab, name)
                    self.FileList.setCurrentIndex(self.FileList.count() - 1)
                    self.FileList.currentWidget().display_accounts()
                except ValueError as ve:
                    self.database.remove_account_group(name)
                    error_message(ve)
            else:
                # if the entered group already exists, go to that tab
                for i in range(self.FileList.count()):
                    text = str(self.FileList.tabText(i))
                    if text == name:
                        self.FileList.setCurrentIndex(i)
                        self.FileList.currentWidget().display_accounts()
                        break            

    def act_remove_account_group_triggered(self):
        name, _, _, ok = AddRemoveAccountGroup.get_account_group_details(
            self.database.grab_account_group_names(), True, self)
        if ok and name:
            self.database.remove_account_group(name)
            for i in range(self.FileList.count()):
                text = str(self.FileList.tabText(i))
                if text == name:
                    self.FileList.setCurrentIndex(i)
                    self.FileList.removeTab( self.FileList.currentIndex())
                    break

    def act_add_account_triggered(self):
        if self.FileList.currentWidget():
            self.FileList.currentWidget().display_accounts()
            name, skip, ok = AddRemoveAccount.get_account_details(
                self.FileList.currentWidget().data.grab_account_names(), False, self)
            if ok and name:
                self.FileList.currentWidget().data.get_account(name, not skip)
            self.FileList.currentWidget().display_accounts()

    def act_remove_account_triggered(self):
        if self.FileList.currentWidget():
            self.FileList.currentWidget().display_accounts()
            name, _, ok = AddRemoveAccount.get_account_details(
                self.FileList.currentWidget().data.grab_account_names(), True, self)
            if ok and name:
                self.FileList.currentWidget().data.remove_account(name)
            self.FileList.currentWidget().display_accounts()

    def act_change_start_date_triggered(self):
        if self.FileList.currentWidget():
            self.FileList.currentWidget().display_accounts()

            start_date, ok = GetStartDate.get_start_date(self.FileList.currentWidget().data.date_placeholder_text(), self)
            if ok and start_date:
                try:
                    self.FileList.currentWidget().data.set_start_date(self.FileList.currentWidget().data.date_serializer(start_date))
                except ValueError as ve:
                    error_message(ve)
            self.FileList.currentWidget().display_accounts()

    def act_refresh_accounts_triggered(self):
        if self.FileList.currentWidget():
            self.FileList.currentWidget().display_accounts()


if __name__ == '__main__':
    app = Main()
    app.start_app()
