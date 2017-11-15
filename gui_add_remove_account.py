from PyQt5 import QtGui, uic
__author__ = 'Gareth Mok'

form_import = uic.loadUiType('add_remove_account.ui')[0]


class AddRemoveAccount(QtGui.QDialog, form_import):
    def __init__(self, names, remove, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.name = ''
        self.skip = False

        self.clearFocus()
        self.check_Skip_Total.setDisabled(remove)
        self.combo_Account_Names.setEditable(not remove)
        for name in names:
            self.combo_Account_Names.addItem(name)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.btn_accepted_clicked)

    def btn_accepted_clicked(self):
        self.name = self.combo_Account_Names.currentText()
        self.skip = self.check_Skip_Total.isChecked()

    @staticmethod
    def get_account_details(names, remove=False, parent=None):
        """
        ok, name, link, last = Select.select_result()
        :param parent:
        :return:
        """
        dialog = AddRemoveAccount(names, remove, parent)
        result = dialog.exec_()

        return dialog.name, dialog.skip, result == QtGui.QDialog.Accepted
