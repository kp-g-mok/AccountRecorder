from PyQt5 import QtCore, QtWidgets, QtGui

from account_database_api import AccountGroup
from static_functions import error_message

import pyqtgraph

__author__ = 'Gareth Mok'

minimum_column_width = 125


class Frame(QtGui.QWidget):
    def __init__(self, account_group: AccountGroup, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.data = account_group

        self.tableAccountData.itemSelectionChanged.connect(self.item_selected)
        self.initialize_shortcuts()
        self.initialize_components()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(964, 677)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        
        self.frameTable = QtWidgets.QFrame(Form)
        self.frameTable.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameTable.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameTable.setObjectName("frameTable")
        self.gridLayoutTable = QtWidgets.QGridLayout(self.frameTable)
        self.gridLayoutTable.setObjectName("gridLayoutTable")
        
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("recordEntryBox")
        self.gridLayoutGroupBox = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayoutGroupBox.setObjectName("gridLayoutGroupBox")
        self.dateSelectionDropdown = QtWidgets.QComboBox(self.groupBox)
        self.dateSelectionDropdown.setObjectName("dateSelection")
        self.dateSelectionDropdown.setEditable(True)
        self.dateSelectionDropdown.lineEdit().setMaxLength(10)
        self.gridLayoutGroupBox.addWidget(self.dateSelectionDropdown, 0, 0, 1, 1, QtCore.Qt.AlignLeft)
        self.accountSelectionDropdown = QtWidgets.QComboBox(self.groupBox)
        self.accountSelectionDropdown.setObjectName("accountSelectionDropdown")
        self.accountSelectionDropdown.setFixedWidth(350)
        self.gridLayoutGroupBox.addWidget(self.accountSelectionDropdown, 0, 1, 1, 1, QtCore.Qt.AlignLeft)
        self.amountEntry = QtWidgets.QLineEdit(self.groupBox)
        self.amountEntry.setObjectName("amountEntry")
        self.amountEntry.setMaxLength(10)
        self.amountEntry.setFixedWidth(150)
        self.gridLayoutGroupBox.addWidget(self.amountEntry, 0, 2, 1, 1, QtCore.Qt.AlignRight)
        self.entryDialogChoice = QtWidgets.QDialogButtonBox(self.groupBox)
        self.entryDialogChoice.setStandardButtons(QtWidgets.QDialogButtonBox.Discard|QtWidgets.QDialogButtonBox.Ok)
        self.entryDialogChoice.setObjectName("entryDialogChoice")
        self.gridLayoutGroupBox.addWidget(self.entryDialogChoice, 0, 3, 1, 1, QtCore.Qt.AlignRight)
    
        self.tableAccountData = QtGui.QTableWidget()
        self.tableAccountData.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.gridLayoutTable.addWidget(self.groupBox, 0, 0, 1, 1, QtCore.Qt.AlignTop)
        self.gridLayoutTable.addWidget(self.tableAccountData, 1, 0, 1, 1)

        self.frameGraph = QtWidgets.QFrame(Form)
        self.frameGraph.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameGraph.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameGraph.setObjectName("frameGraph")
        self.gridLayoutGraph = QtWidgets.QGridLayout(self.frameGraph)
        self.gridLayoutGraph.setObjectName("gridLayoutGraph")

        self.total_string_axis = pyqtgraph.AxisItem(orientation='bottom')
        self.total_graph = pyqtgraph.PlotWidget(title='Total Monetary Value',
                                                axisItems={'bottom': self.total_string_axis})
        self.total_graph.getPlotItem().getViewBox().setMouseEnabled(False, False)
        self.total_graph.getPlotItem().getViewBox().setMenuEnabled(False)
        self.total_graph.getPlotItem().showGrid(y=True)

        self.total_plot = self.total_graph.plot(symbolSize=0, pxMode=False)

        self.IndividualGraphs = QtGui.QTabWidget()
        self.tabs = {}
        
        self.gridLayoutGraph.addWidget(self.total_graph, 0, 0, 1, 1)
        self.gridLayoutGraph.addWidget(self.IndividualGraphs, 1, 0, 1, 1)

        self.gridLayout.addWidget(self.frameTable, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frameGraph, 0, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Record Entry"))
        self.total_graph.setLabel('left', 'Monetary Value')
        self.total_graph.setLabel('bottom', 'Date')

    def initialize_shortcuts(self):
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Return), self, self.new_entry_accepted)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Enter), self, self.new_entry_accepted)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete), self, self.remove_entries)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Z),
                        self, self.previous_graph_tab)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_X),
                        self, self.next_graph_tab)

    def initialize_components(self):
        self.entryDialogChoice.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.new_entry_accepted)
        self.entryDialogChoice.button(QtGui.QDialogButtonBox.Discard).clicked.connect(self.new_entry_discarded)

    def next_graph_tab(self):
        new_index = (self.IndividualGraphs.currentIndex() + 1) % self.IndividualGraphs.count()
        self.IndividualGraphs.setCurrentIndex(new_index)

    def previous_graph_tab(self):
        new_index = self.IndividualGraphs.currentIndex() - 1
        if new_index == -1:
            new_index = self.IndividualGraphs.count() - 1
        self.IndividualGraphs.setCurrentIndex(new_index)

    def new_entry_accepted(self):
        record_date = self.data.date_serializer(self.dateSelectionDropdown.currentText())
        record_account = self.accountSelectionDropdown.currentText()
        record_amount = self.amountEntry.text()
        if not record_amount:
            return
        try:
            self.data.add_account_entry(record_account, record_date, record_amount)
        except ValueError as ve:
            error_message(ve)
        except OverflowError as oe:
            error_message(oe)
        
        self.amountEntry.clear()
        self.display_accounts()

    def new_entry_discarded(self):
        dates = sorted(self.data.grab_dates(), reverse = True)
        # Update date dropdown list
        self.dateSelectionDropdown.clear()
        for date in dates:
            self.dateSelectionDropdown.addItem(self.data.date_parser(date))
        self.dateSelectionDropdown.setCurrentIndex(1)
        self.accountSelectionDropdown.setCurrentIndex(0)
        self.amountEntry.clear()

    def remove_entries(self):
        for index in self.tableAccountData.selectedIndexes():
            column = index.column()
            row = index.row()

            account_name = str(self.tableAccountData.horizontalHeaderItem(column).text())
            if account_name == 'Total':
                continue
            
            date = self.data.date_serializer(str(self.tableAccountData.verticalHeaderItem(row).text()))

            self.data.remove_account_entry(account_name, date)
            self.display_accounts()
            self.IndividualGraphs.setCurrentIndex(column - 1)

    def display_accounts(self):
        dates = sorted(self.data.grab_dates(), reverse = True)
        # Update date dropdown list
        self.dateSelectionDropdown.clear()
        for date in dates:
            self.dateSelectionDropdown.addItem(self.data.date_parser(date))
        self.dateSelectionDropdown.setCurrentIndex(1)
        dates.pop(0)
        
        needed_rows = len(dates)
        accounts = list(self.data.grab_account_names())
        # Update account dropdown list
        self.accountSelectionDropdown.clear()
        for account in accounts:
            self.accountSelectionDropdown.addItem(account)

        accounts.insert(0, 'Total')
        needed_cols = len(accounts)
        
        # Add or remove columns as needed
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

        # Add or remove rows as needed
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
        total = self.get_total()[::-1]
        accounts_data['Total'] = {dates[i]: total[i] for i in range(len(total))}
        
        # Fill out the table
        for row, date in enumerate(dates):
            for col, name in enumerate(accounts):
                self.tableAccountData.setColumnWidth(col, minimum_column_width)
                new_item = QtGui.QTableWidgetItem("")
                if date in accounts_data[name].keys():                    
                    value = str(accounts_data[name][date])
                    if value == '0':
                        # Pad value with two zeros to make sure the decimal comes out correctly
                        value += '00'
                    new_item = QtGui.QTableWidgetItem('{: ,}'.format(int(value[:-2])) + '.' + value[-2:])
                    new_item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                    if float(value) < 0:
                        new_item.setForeground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
                    if name == 'Total':
                        if float(value) < 0:
                            new_item.setForeground(QtGui.QBrush(QtGui.QColor(255, 0, 0, 125)))
                self.tableAccountData.setItem(row, col, new_item)

        self.tableAccountData.setHorizontalHeaderLabels(accounts)
        self.tableAccountData.setVerticalHeaderLabels([self.data.date_parser(date) for date in dates])

        # Update Graphs
        self.display_total_graph()
        self.display_individual_graph()

        self.tableAccountData.setFocus()

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
        money_values = [0 for i in range(len(dates) - 1)]

        dates_dictionary = dict(enumerate(dates[-17:-1]))
        self.total_string_axis.setTicks([dates_dictionary.items()])

        for name in accounts:
            if not self.data.grab_account_skip_data(name):
                continue
            for date in accounts_data[name].keys():
                money_values[dates.index(date)] += int(accounts_data[name][date])
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
        self.tabs[name] = tab_plot.plot(symbolSize=0, pxMode=False)

    def item_selected(self):
        for index in self.tableAccountData.selectedIndexes():
            column = index.column()
            row = index.row()

            account_name = str(self.tableAccountData.horizontalHeaderItem(column).text())
            if account_name == 'Total':
                continue
            
            dates = sorted(self.data.grab_dates(), reverse = True)
            date = self.data.date_serializer(str(self.tableAccountData.verticalHeaderItem(row).text()))
            self.dateSelectionDropdown.setCurrentIndex(dates.index(date))
            
            accounts = list(self.data.grab_account_names())
            self.accountSelectionDropdown.setCurrentIndex(accounts.index(account_name))


if __name__ == '__main__':
    from gui_main import Main
    app = Main()
    app.start_app()
