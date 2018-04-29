from PyQt5 import QtCore, QtGui,uic

from account_database_api import Account
from static_functions import date_serializer

import pyqtgraph

__author__ = 'Gareth Mok'
form_frame = uic.loadUiType('frame.ui')[0]

minimum_column_width = 125


class Frame(QtGui.QWidget, form_frame):
    def __init__(self, filename, database_type=None, start_date=None, parent=None):
        self.data = Account(filename, database_type, start_date)

        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.tableAccountData = QtGui.QTableWidget()

        self.total_string_axis = pyqtgraph.AxisItem(orientation='bottom')
        self.total_graph = pyqtgraph.PlotWidget(title='Total Monetary Value',
                                                axisItems={'bottom': self.total_string_axis})
        self.total_graph.getPlotItem().getViewBox().setMouseEnabled(False, False)
        self.total_graph.getPlotItem().getViewBox().setMenuEnabled(False)
        self.total_graph.getPlotItem().showGrid(y=True)
        self.total_graph.setLabel('left', 'Monetary Value')
        self.total_graph.setLabel('bottom', 'Date')

        self.total_plot = self.total_graph.plot(symbolSize=0.25, pxMode=False)

        self.IndividualGraphs = QtGui.QTabWidget()
        self.tabs = {}

        self.gridLayout.addWidget(self.tableAccountData, 0, 0, 2, 1)
        self.gridLayout.addWidget(self.total_graph, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.IndividualGraphs, 1, 1, 1, 1)

        self.connect_components()
        self.initialize_shortcuts()
        self.initialize_components()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(964, 677)
        self.gridLayout_6 = QtWidgets.QGridLayout(Form)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_6.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

    def connect_components(self):
        self.tableAccountData.cellChanged.connect(self.cell_changed)

    def initialize_shortcuts(self):
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete), self, self.remove_entries)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Z),
                        self, self.previous_graph_tab)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_X),
                        self, self.next_graph_tab)

    def initialize_components(self):
        self.display_accounts()
        self.tableAccountData.scrollToBottom()

    def next_graph_tab(self):
        new_index = (self.IndividualGraphs.currentIndex() + 1) % self.IndividualGraphs.count()
        self.IndividualGraphs.setCurrentIndex(new_index)

    def previous_graph_tab(self):
        new_index = self.IndividualGraphs.currentIndex() - 1
        if new_index == -1:
            new_index = self.IndividualGraphs.count() - 1
        self.IndividualGraphs.setCurrentIndex(new_index)

    def display_accounts(self):
        self.tableAccountData.blockSignals(True)

        dates = self.data.grab_dates()
        needed_rows = len(dates)
        accounts = self.data.grab_account_names()
        accounts.insert(0, 'Total')
        needed_cols = len(accounts)

        # Fill or remove columns as needed
        current_cols = self.tableAccountData.columnCount()
        if current_cols != needed_cols:
            if current_cols < needed_cols:
                for i in range(needed_cols - current_cols):
                    if self.tableAccountData.columnCount() == 0:
                        self.tableAccountData.insertColumn(self.tableAccountData.columnCount())
                    else:
                        self.tableAccountData.insertColumn(self.tableAccountData.columnCount() - 1)
            else:
                for i in range(current_cols - needed_cols):
                    self.tableAccountData.removeColumn(0)

        # Fill or remove rows as needed
        current_rows = self.tableAccountData.rowCount()
        if current_rows != needed_rows:
            if current_rows < needed_rows:
                for i in range(needed_rows - current_rows):
                    if self.tableAccountData.rowCount() == 0:
                        self.tableAccountData.insertRow(self.tableAccountData.rowCount())
                    else:
                        self.tableAccountData.insertRow(self.tableAccountData.rowCount() - 1)
            else:
                for i in range(current_rows - needed_rows):
                    self.tableAccountData.removeRow(0)

        accounts_data = {name: self.data.grab_account_data(name) for name in accounts}
        total = [value * 100 for value in self.get_total()]
        accounts_data['Total'] = {dates[i]: total[i] for i in range(len(total))}
        accounts_data['Total'][dates[-1]] = 0
        # Fill out the table
        for row, date in enumerate(dates):
            for col, name in enumerate(accounts):
                self.tableAccountData.setColumnWidth(col, minimum_column_width)
                if date in accounts_data[name].keys():
                    value = accounts_data[name][date] / 100
                    new_item = QtGui.QTableWidgetItem('{: ,.2f}'.format(value))
                    new_item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                    if value < 0:
                        new_item.setForeground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
                    if name == 'Total':
                        if value < 0:
                            new_item.setForeground(QtGui.QBrush(QtGui.QColor(255, 0, 0, 125)))
                        new_item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableAccountData.setItem(row, col, new_item)
                else:
                    new_item = QtGui.QTableWidgetItem("")
                    self.tableAccountData.setItem(row, col, new_item)

        self.tableAccountData.setHorizontalHeaderLabels(accounts)
        self.tableAccountData.setVerticalHeaderLabels(dates)
        self.tableAccountData.blockSignals(False)

        # Update Graphs
        self.display_total_graph()
        self.display_individual_graph()

        self.tableAccountData.setFocus()

    def remove_entries(self):
        for index in self.tableAccountData.selectedIndexes():
            column = index.column()
            row = index.row()

            account_name = str(self.tableAccountData.horizontalHeaderItem(column).text())
            date = date_serializer(self.data.get_type(), str(self.tableAccountData.verticalHeaderItem(row).text()))

            self.data.remove_entry(account_name, date)
            self.display_accounts()
            self.IndividualGraphs.setCurrentIndex(column - 1)

    def display_total_graph(self):
        dates = self.data.grab_dates()[-17:-1]

        date_indices = [i for i in range(len(dates))]
        money_values = self.get_total()[-16:]

        if money_values[-1] < 0:
            self.total_plot.setPen((255, 0, 0), width=2)
        else:
            self.total_plot.setPen((0, 255, 0), width=2)
        self.total_plot.setData(x=date_indices, y=money_values)

    def get_total(self):
        dates = self.data.grab_dates()
        accounts = self.data.grab_account_names()
        accounts_data = {name: self.data.grab_account_data(name) for name in accounts}
        money_values = [0.00 for i in range(len(dates) - 1)]

        dates_dictionary = dict(enumerate(self.data.grab_dates()[-17:-1]))
        self.total_string_axis.setTicks([dates_dictionary.items()])

        for name in accounts:
            if 'Skip' in accounts_data[name].keys():
                continue
            for date in accounts_data[name].keys():
                money_values[dates.index(date)] += int(accounts_data[name][date])/100
        return money_values

    def display_individual_graph(self):
        self.IndividualGraphs.clear()
        for name in [key for key in self.tabs.keys()]:
            del self.tabs[name]

        dates = self.data.grab_dates()[-17: -1]
        accounts = self.data.grab_account_names()
        accounts_data = {name: self.data.grab_account_data(name) for name in accounts}

        date_indices = [i for i in range(len(dates))]

        for name in accounts:
            money_values = [0.00 for i in range(len(dates))]
            for date in dates:
                if date in accounts_data[name].keys():
                    money_values[dates.index(date)] += int(accounts_data[name][date])/100

            if name not in self.tabs.keys():
                self.create_individual_graph(name)
            if money_values[-1] < 0:
                self.tabs[name].setPen((255, 0, 0), width=2)
            else:
                self.tabs[name].setPen((0, 255, 0), width=2)
            self.tabs[name].setData(x=date_indices, y=money_values)

    def create_individual_graph(self, name):
        dates_dictionary = dict(enumerate(self.data.grab_dates()[-17:-1]))

        widget = QtGui.QWidget()
        layout = QtGui.QGridLayout(widget)
        self.IndividualGraphs.addTab(widget, name)
        tab_string_axis = pyqtgraph.AxisItem(orientation='bottom')
        tab_string_axis.setTicks([dates_dictionary.items()])
        tab_plot = pyqtgraph.PlotWidget(title='{} Monetary Value'.format(name), axisItems={'bottom': tab_string_axis})
        tab_plot.getPlotItem().getViewBox().setMouseEnabled(False, False)
        tab_plot.getPlotItem().getViewBox().setMenuEnabled(False)
        tab_plot.getPlotItem().showGrid(y=True)
        tab_plot.setLabel('left', 'Monetary Value')
        tab_plot.setLabel('bottom', 'Date')
        layout.addWidget(tab_plot)
        self.tabs[name] = tab_plot.plot(symbolSize=0.25, pxMode=False)

    def cell_changed(self, row, column):
        account_name = str(self.tableAccountData.horizontalHeaderItem(column).text())
        date = date_serializer(self.data.get_type(), str(self.tableAccountData.verticalHeaderItem(row).text()))
        money = str(self.tableAccountData.item(row, column).text())

        try:
            self.data.add_entry(account_name, date, money)
        except ValueError:
            self.tableAccountData.item(row, column).setText = ''
        self.display_accounts()
        self.IndividualGraphs.setCurrentIndex(column - 1)

def main():
    from gui_main import MainWindow
    import sys

    app = QtGui.QApplication(sys.argv)
    my_window = MainWindow(None)
    my_window.show()
    my_window.act_refresh_accounts_triggered()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
