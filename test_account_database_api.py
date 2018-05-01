from unittest import TestCase

from account_database_api import Database
import os
from datetime import date

__author__ = 'Gareth Mok'


class TestAccountDatabaseAPI(TestCase):
    def test_new(self):
        filepath = 'test.json'
        database_type = 'Monthly'
        start_date = '2015-02'
        data = Account(filepath, database_type, start_date)

        self.assertTrue(os.path.isfile(filepath))
        self.assertEqual(data.data['Type'], database_type)
        self.assertEqual(data.data['Start Date'], start_date)
        self.assertEqual(data.data['Accounts'], {})
        os.remove(filepath)

    def test_add_remove_account(self):
        filepath = 'test.json'
        database_type = 'Monthly'
        start_date = '2015-02'
        data = Account(filepath, database_type, start_date)

        account_names = ['Test Account', 'Blah Account']

        [data.add_account(account_name) for account_name in account_names]
        self.assertEqual(sorted([key for key in data.data['Accounts'].keys()]), sorted(account_names))

        data.remove_account('Blah Account')
        account_names.remove('Blah Account')
        self.assertEqual([key for key in data.data['Accounts'].keys()], account_names)

        os.remove(filepath)

    def test_add_remove_entry(self):
        filepath = 'test.json'
        database_type = 'Monthly'
        start_date = '2015-02'
        data = Account(filepath, database_type, start_date)

        account_name = 'Test Account'
        account_data = {'2015-03': '132.21', '2015-04': '143.22'}
        test_data = {str(key): int(value.replace('.', '')) for key, value in account_data.items()}

        [data.add_entry(account_name, record_date, amount) for record_date, amount in account_data.items()]
        self.assertEqual(data.data['Accounts'][account_name], test_data)

        data.remove_entry(account_name, '2015-04')
        test_data.pop('2015-04')
        self.assertEqual(data.data['Accounts'][account_name], test_data)

        os.remove(filepath)

    def test_grab_dates(self):
        filepath = 'test.json'
        database_type = 'Monthly'
        start_date = '2015-02'
        data = Account(filepath, database_type, start_date)

        data.set_end_date('2016-02')
        self.assertEqual(data.grab_dates(), ['02/2015', '03/2015', '04/2015', '05/2015', '06/2015', '07/2015',
                                             '08/2015', '09/2015', '10/2015', '11/2015', '12/2015', '01/2016',
                                             '02/2016','03/2016'])

        data.set_end_date('2016-04')
        data.data['Type'] = 'Quarterly'
        data.write()
        self.assertEqual(data.grab_dates(), ['Q1 2015', 'Q2 2015', 'Q3 2015', 'Q4 2015',
                                             'Q1 2016', 'Q2 2016', 'Q3 2016'])

        data.set_end_date('2020-02')
        data.data['Type'] = 'Yearly'
        data.write()
        self.assertEqual(data.grab_dates(), ['2015', '2016', '2017', '2018', '2019', '2020', '2021'])

        os.remove(filepath)

    def test_grab_names(self):
        filepath = 'test.json'
        database_type = 'Monthly'
        start_date = '2015-02'
        data = Account(filepath, database_type, start_date)

        account_names = sorted(['Test Account', 'Test 2 Account'])
        record_date = '2015-03'
        amount = '13221'

        [data.add_entry(account_name, record_date, amount) for account_name in account_names]

        self.assertEqual(data.grab_account_names(), account_names)
        os.remove(filepath)

    def test_grab_account_data(self):
        filepath = 'test.json'
        database_type = 'Monthly'
        start_date = '2015-02'
        data = Account(filepath, database_type, start_date)

        account_name = 'Test Account'
        account_data = {'2015-03': '132.21', '2015-04': '143.22'}
        test_data = {data.date_parser(key): int(value.replace('.', '')) for key, value in account_data.items()}

        [data.add_entry(account_name, recordDate, amount) for recordDate, amount in account_data.items()]

        self.assertEqual(data.grab_account_data(account_name), test_data)
        os.remove(filepath)
