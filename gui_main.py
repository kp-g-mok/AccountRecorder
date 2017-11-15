import os
import sys

from PyQt5 import QtCore, QtGui, uic

from file_database_api import Files
from gui_frame import Frame
from gui_get_database_type import GetDatabaseType
from gui_get_start_date import GetStartDate
from gui_add_remove_account import AddRemoveAccount
from gui_add_remove_entry import AddRemoveEntry
from static_functions import date_serializer, date_placeholder_text, error_message

__author__ = 'Gareth Mok'

form_main = uic.loadUiType('main.ui')[0]


class MainWindow(QtGui.QMainWindow, form_main):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.last_session = Files('last_open.json')
        if not self.last_session.empty() or self.last_session.get_directory():
            if os.path.isdir(self.last_session.get_directory()):
                self.directory = self.last_session.get_directory()
            else:
                if getattr(sys, 'frozen', False):  # frozen
                    self.directory = os.path.dirname(os.path.realpath(sys.executable))
                else:  # unfrozen
                    self.directory = os.path.dirname(os.path.realpath(__file__))
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
