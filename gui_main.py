import os
import sys

from PyQt5 import QtCore, QtWidgets, QtGui, uic

from config_file_api import Config
from account_database_api import Database
from static_functions import date_serializer, date_placeholder_text, error_message

from gui_frame import Frame
from gui_get_database_type import GetDatabaseType
from gui_get_start_date import GetStartDate
from gui_add_remove_account import AddRemoveAccount
from gui_add_remove_entry import AddRemoveEntry

__author__ = 'Gareth Mok'


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.last_session = Config('last_open.json')
        self.database = ''
        if getattr(sys, 'frozen', False):  # frozen
            self.directory = os.path.dirname(os.path.realpath(sys.executable))
        else:  # unfrozen
            self.directory = os.path.dirname(os.path.realpath(__file__))
        if self.last_session.get_prev_database():
            filename = ''
            while not filename:
                filename = QtGui.QFileDialog.getSaveFileName(QtGui.QFileDialog(), 'New database file', self.directory, '*.fs')[0]
            self.database = Database(filename)

        if not self.last_session.empty() or self.last_session.get_directory():
            if os.path.isdir(self.last_session.get_directory()):
                self.directory = self.last_session.get_directory()
            else:
                
                self.last_session.add_update("Directory", self.directory)

            file_list = self.last_session.grab()
            sorted_names = sorted(file_list)
            for i, name in enumerate(sorted_names):
                if os.path.isfile(file_list[name]):
                    new_tab = Frame(file_list[name], self)
                    self.FileList.addTab(new_tab, name)
                    self.act_refresh_accounts_triggered()
                else:
                    self.last_session.remove(name)
        else:
            if getattr(sys, 'frozen', False):  # frozen
                    self.directory = os.path.dirname(os.path.realpath(sys.executable))
            else:  # unfrozen
                self.directory = os.path.dirname(os.path.realpath(__file__))
            self.last_session.add_update("Directory", self.directory)

        if self.FileList.currentWidget():
            self.FileList.currentWidget().tableAccountData.setFocus()

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

    def connect_components(self):
        self.act_New.triggered.connect(self.act_new_triggered)
        self.act_Open.triggered.connect(self.act_open_triggered)
        self.act_Close_Tab.triggered.connect(self.act_close_tab_triggered)
        self.act_Change_Default_Directory.triggered.connect(self.act_change_default_account_directory_triggered)
        self.act_Change_Start_Date.triggered.connect(self.act_change_start_date_triggered)
        self.act_Exit.triggered.connect(self.act_exit_triggered)
        self.act_Refresh_Accounts.triggered.connect(self.act_refresh_accounts_triggered)
        self.act_Add_Account.triggered.connect(self.act_add_account_triggered)
        self.act_Add_Entry.triggered.connect(self.act_add_entry_triggered)
        self.act_Remove_Account.triggered.connect(self.act_remove_account_triggered)
        self.act_Remove_Entry.triggered.connect(self.act_remove_entry_triggered)
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

    def act_new_triggered(self):
        """
        Creates a new account database and opens it in a new tab
        :return:
        """
        filename = QtGui.QFileDialog.getSaveFileName(QtGui.QFileDialog(), 'New file', self.directory, '*.json')[0]
        if filename != '':
            database_type, ok = GetDatabaseType.get_database_type(self)
            if ok and database_type != '':
                start_date, ok = GetStartDate.get_start_date(date_placeholder_text(database_type),self)
                if ok and start_date != '':
                    base_filename = os.path.basename(filename)

                    try:
                        new_tab = Frame(filename, database_type, date_serializer(database_type, start_date), self)

                        self.FileList.addTab(new_tab, base_filename)
                        self.FileList.setCurrentIndex(self.FileList.count() - 1)
                        self.FileList.currentWidget().display_accounts()
                        self.last_session.add_update(base_filename, filename)
                    except ValueError as ve:
                        error_message(ve)

    def act_open_triggered(self):
        """
        Opens a file in current tab or new tab
        :return:
        """
        filename = QtGui.QFileDialog.getOpenFileName(QtGui.QFileDialog(), 'Open file', self.directory, '*.json')[0]
        if filename != '':
            base_filename = os.path.splitext(os.path.basename(filename))[0]

            for i in range(self.FileList.count()):
                text = str(self.FileList.tabText(i))
                if text == base_filename:
                    self.FileList.setCurrentIndex(i)
                    self.FileList.currentWidget().display_accounts()
                    break
            else:
                new_tab = Frame(filename, self)
                self.FileList.addTab(new_tab, base_filename)
                self.FileList.setCurrentIndex(self.FileList.count() - 1)
                self.FileList.currentWidget().display_accounts()
                self.last_session.add_update(base_filename, filename)

    def act_close_tab_triggered(self):
        current = self.FileList.currentIndex()
        self.last_session.remove(str(self.FileList.tabText(current)))
        self.FileList.removeTab(current)

    def act_change_default_account_directory_triggered(self):
        self.directory = QtGui.QFileDialog.getExistingDirectory(QtGui.QFileDialog(), None,
                                                                'Choose Account Database Directory')
        self.last_session.add_update("Directory", self.directory)

    def act_change_start_date_triggered(self):
        if self.FileList.currentWidget():
            self.FileList.currentWidget().display_accounts()

            database_type = self.FileList.currentWidget().data.get_type()
            start_date, ok = GetStartDate.get_start_date(date_placeholder_text(database_type), self)
            if ok and start_date:
                try:
                    self.FileList.currentWidget().data.set_start_date(date_serializer(database_type, start_date))
                except ValueError as ve:
                    error_message(ve)
            self.FileList.currentWidget().display_accounts()

    def act_exit_triggered(self):
        self.close()

    def act_refresh_accounts_triggered(self):
        if self.FileList.currentWidget():
            self.FileList.currentWidget().display_accounts()

    def act_add_account_triggered(self):
        if self.FileList.currentWidget():
            self.FileList.currentWidget().display_accounts()
            name, skip, ok = AddRemoveAccount.get_account_details(
                self.FileList.currentWidget().data.grab_account_names(), False, self)
            if ok and name:
                self.FileList.currentWidget().data.add_account(name, skip)
            self.FileList.currentWidget().display_accounts()

    def act_add_entry_triggered(self):
        if self.FileList.currentWidget():
            self.FileList.currentWidget().display_accounts()
            database_type = self.FileList.currentWidget().data.get_type()
            name, date, money, ok = AddRemoveEntry.get_entry_details(
                self.FileList.currentWidget().data.grab_account_names(), 0, date_placeholder_text(database_type), self)
            if ok and name and date and money:
                try:
                    self.FileList.currentWidget().data.add_entry(name, date_serializer(database_type, date), money)
                except ValueError as ve:
                    error_message(ve)

            self.FileList.currentWidget().display_accounts()

    def act_remove_account_triggered(self):
        if self.FileList.currentWidget():
            self.FileList.currentWidget().display_accounts()
            name, skip, ok = AddRemoveAccount.get_account_details(
                self.FileList.currentWidget().data.grab_account_names(), True, self)
            if ok and name:
                self.FileList.currentWidget().data.remove_account(name)
            self.FileList.currentWidget().display_accounts()

    def act_remove_entry_triggered(self):
        if self.FileList.currentWidget():
            self.FileList.currentWidget().display_accounts()
            database_type = self.FileList.currentWidget().data.get_type()
            name, date, money, ok = AddRemoveEntry.get_entry_details(
                self.FileList.currentWidget().data.grab_account_names(), 1, date_placeholder_text(database_type), self)
            if ok and name and date:
                try:
                    self.FileList.currentWidget().data.remove_entry(name, date_serializer(database_type, date))
                except ValueError as ve:
                    error_message(ve)

            self.FileList.currentWidget().display_accounts()


def main():
    app = QtGui.QApplication(sys.argv)
    my_window = MainWindow(None)
    my_window.show()
    my_window.act_refresh_accounts_triggered()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
