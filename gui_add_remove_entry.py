from PyQt5 import QtCore, QtGui, uic
__author__ = 'Gareth Mok'

form_import = uic.loadUiType('add_remove_entry.ui')[0]


class AddRemoveEntry(QtGui.QDialog, form_import):
    def __init__(self, names, remove, date_placeholder_text, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.name = ''
        self.date = ''
        self.money = ''

        self.lin_Money_Value.setDisabled(remove)
        for name in names:
            self.combo_Account_Names.addItem(name)
        self.lin_Entry_Date.setPlaceholderText(date_placeholder_text)
        self.clearFocus()
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.btn_accepted_clicked)

    def btn_accepted_clicked(self):
        self.name = self.combo_Account_Names.currentText()
        self.date = self.lin_Entry_Date.text()
        self.money = self.lin_Money_Value.text()

    @staticmethod
    def get_entry_details(names, remove, date_placeholder_text, parent=None):
        """
        ok, name, link, last = Select.select_result()
        :param parent:
        :return:
        """
        dialog = AddRemoveEntry(names, remove, date_placeholder_text, parent)
        result = dialog.exec_()
        return dialog.name, dialog.date, dialog.money, result == QtGui.QDialog.Accepted
