from unittest import TestCase
from file_database_api import Files
from account_database_api import Account
import os
from datetime import date

__author__ = 'Gareth Mok'


class TestFiles(TestCase):
    def test_new(self):
        filepath = "lastopen.json"
        self.data = Files(filepath)

        self.assertTrue(os.path.isfile(filepath))
        os.remove(filepath)

    def test_add_update(self):
        filepath = "lastopen.json"
        data = Files(filepath)

        accountpath1 = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test1.json')
        test1_account = Account(accountpath1, "M", date(2015, 3, 1))

        accountpath2 = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test2.json')
        test2_account = Account(accountpath2, "M", date(2015, 3, 1))

        name = "Test File"
        data.add_update(name, accountpath1)
        self.assertEqual(data.data, {name: accountpath1})

        data.add_update(name, accountpath2)
        self.assertEqual(data.data, {name: accountpath2})

        data.add_update(name+"1", accountpath1)
        self.assertEqual(data.data, {name: accountpath2, name+"1": accountpath1})

        os.remove(filepath)
        os.remove(accountpath1)
        os.remove(accountpath2)

    def test_remove(self):
        filepath = "lastopen.json"
        data = Files(filepath)

        accountpath = os.path.join(os.path.dirname(os.path.realpath(__file__)),'test.json')
        test_account = Account(accountpath, "M", date(2015, 3, 1))

        name = "Test File"
        data.add_update(name, accountpath)
        data.remove(name)

        self.assertEqual(data.data, {})

        os.remove(filepath)
        os.remove(accountpath)

    def test_grab(self):
        filepath = "lastopen.json"
        data = Files(filepath)

        accountpath1 = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test1.json')
        test1_account = Account(accountpath1, "M", date(2015, 3, 1))

        accountpath2 = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test2.json')
        test2_account = Account(accountpath2, "M", date(2015, 3, 1))

        name = "Test File"
        data.add_update(name+"1", accountpath1)
        data.add_update(name+"2", accountpath2)
        self.assertEqual(data.grab(), {name+"2": accountpath2, name+"1": accountpath1})

        os.remove(filepath)
        os.remove(accountpath1)
        os.remove(accountpath2)

    def test_empty(self):
        filepath = "lastopen.json"
        data = Files(filepath)

        self.assertTrue(data.empty())

        accountpath = os.path.join(os.path.dirname(os.path.realpath(__file__)),'test.json')
        test_account = Account(accountpath, "M", date(2015, 3, 1))

        data.add_update("Test File", accountpath)

        self.assertFalse(data.empty())

        os.remove(filepath)
        os.remove(accountpath)
