from PyQt5 import QtGui, uic
__author__ = 'Gareth Mok'

form_import = uic.loadUiType('get_database_type.ui')[0]


class GetDatabaseType(QtGui.QDialog, form_import):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.database_type = ''

        self.clearFocus()
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.btn_accepted_clicked)

    def btn_accepted_clicked(self):
        if self.radio_Monthly.isChecked():
            self.database_type = 'Monthly'
        elif self.radio_Quarterly.isChecked():
            self.database_type = 'Quarterly'
        elif self.radio_Yearly.isChecked():
            self.database_type = 'Yearly'

    @staticmethod
    def get_database_type(parent=None):
        """
        ok, name, link, last = Select.select_result()
        :param parent:
        :return:
        """
        dialog = GetDatabaseType(parent)
        result = dialog.exec_()

        return dialog.database_type, result == QtGui.QDialog.Accepted
