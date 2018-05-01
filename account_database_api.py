import os
import datetime

import ZODB
import ZODB.FileStorage
from persistent import Persistent
from BTrees import OOBTree, OIBTree
import transaction

__author__ = 'Gareth Mok'

class Database(Persistent):
    def __init__(self, filepath: str):
        setup_db = not os.path.isfile(filepath)
        self.db = ZODB.DB(filepath)
        if setup_db:
            self.connection = self.db.open()
            self.root = self.connection.root()
            self.root.account_groups = OOBTree.BTree()
            transaction.commit()
            self.connection.close()
            
        self.connection = None
        self.root = None

    def __enter__(self):
        self.connection = self.db.open()
        self.root = self.connection.root()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        transaction.commit()
        self.connection.close()
        self.connection = None
        self.root = None

    def refresh(self):
        self.__exit__(None, None, None)
        self.__enter__()

    def get_account_group(self, group_name: str):
        """Gets the account group data from the datbase
            If the account group doesn't exist, create it first
        
        Arguments:
            group_name {str} -- monetary account name to create/retrieve
        
        Raises:
            ConnectionError -- Raised if the database hasn't been connected to yet
        
        Returns:
            Account -- the Account data tied to the given account name
        """

        if not self.connection and not self.root:
            raise ConnectionError('Database connection not setup yet. Use the database with a context manager.')
        if group_name not in self.root.account_groups:
            self.root.account_groups[group_name] = AccountGroup()
        return self.root.account_groups[group_name]
    
    def remove_account_group(self, group_name: str):
        if not self.connection and not self.root:
            raise ConnectionError('Database connection not setup yet. Use the database with a context manager.')
        if group_name in self.root.account_groups:
            del self.root.account_groups[group_name]
        else:
            raise KeyError("Account doesn't exist in database")

    def grab_account_group_names(self):
        return self.root.account_groups.keys()
        

class AccountGroup(Persistent):
    def __init__(self):
        self.type = ''
        self.start_date = ''
        self.end_date = ''
        self.accounts = OOBTree.BTree()        

    def get_start_date(self):
        return self.date_parser(self.start_date)

    def set_start_date(self, input_date: str):
        """ Setter for Start Date of Account Group. If there is no end date set, set it to the start date
        
        Arguments:
            input_date {str: '%Y-%m' format} -- New start date for account database
        """

        self.check_date_format(input_date)
        self.start_date = input_date
        if not self.end_date:
            self.end_date = input_date

    def get_end_date(self):
        return self.date_parser(self.end_date)
    
    def set_end_date(self, input_date: str):
        """ Setter for End Date of Account Group
        
        Arguments:
            input_date {str: '%Y-%m' format} -- New end date for account database
        """
        
        self.check_date_format(input_date)
        self.end_date = input_date

    def get_type(self):
        return self.type
    
    def set_type(self, type: str):
        database_types = ['Monthly', 'Quarterly', 'Yearly']
        if type not in database_types:
            raise ValueError('Value Error: Invalid type. Type must be "Monthly", "Quarterly", or "Yearly"')
        self.type = type
    
    def get_account(self, account_name: str, part_of_total=True):
        """ Get an account from the group, adds if it doesn't exist
        
        Arguments:
            account_name {str} -- account account name to add
        
        Keyword Arguments:
            part_of_total {bool} -- determines if the account should be part of the total account money calculations (default: {True})
        """
        if account_name not in self.accounts:
            self.accounts[account_name] = Account(part_of_total)
        return self.accounts[account_name]

    def add_account_entry(self, account_name: str, entry_date: str, money: str):
        """ Add a record entry to the account, rewrites if an entry exists
        
        Arguments:
            account_name {str} -- account account to add an entry to
            entry_date {str: '%Y-%m' format} -- date when the entry occurs
            money {str} -- money string that will be converted into a monetary int
        
        Raises:
            ValueError -- Raised if the given money value can't be converted into the int format
            KeyError -- Raised if the given account doesn't exist on the account
        """

        self.check_date_format(entry_date)

        if account_name not in self.accounts:
            raise KeyError("account doesn't exist in account")
        
        try:
            money = money.replace(',', '')
            if '.' in money:
                if len(money.split('.')[1]) == 0:  # There is nothing after the period
                    money = int(money.replace('.', '')) * 100
                elif len(money.split('.')[1]) == 1:  # There is 1 digit after the period
                    money = int(money.replace('.', '')) * 10
                elif len(money.split('.')[1]) == 2:  # There are 2 digits after the period
                    money = int(money.replace('.', ''))
                else:  # There are more than 2 digits after the period; truncate to 2 digits after the period
                    money = int(money[0:len(money.split('.')[0]) + 3].replace('.', ''))
            else:  # There is no period in the string
                if money == '':
                    money = 0
                money = int(money) * 100
        except ValueError:
            raise ValueError("ValueError: Invalid monetary value. "
                             "Value needs to be a number with only commas and periods")

        self.accounts[account_name].add_update_record(entry_date, money)

        if self.end_date < entry_date:
            # Current account database end date is lower than new entry date
            # Set the account database date to the new entry date
            self.set_end_date(entry_date)

    def remove_split(self, account_name: str):
        """ Remove an account from the account, does nothing if it doesn't exists
        
        Arguments:
            account_name {str} -- account account to add an entry to
        """

        if account_name in self.accounts:
            del self.accounts[account_name]

    def remove_account_entry(self, account_name: str, entry_date: str):
        """ Remove a record entry to the account, rewrites if an entry exists
        
        Arguments:
            account_name {str} -- account account to add an entry to
            entry_date {str: '%Y-%m' format} -- date when the entry occurs
        
        Raises:
            KeyError -- [description]
        """

        self.check_date_format(entry_date)

        if account_name not in self.accounts:
            raise KeyError("account doesn't exist in account")
        self.accounts[account_name].remove_record(entry_date)

        latest_dates = sorted([self.accounts[account].latest_date for account in self.accounts])
        if self.end_date > latest_dates[-1]:
            # Current account database end date is greater than latest dates for all accounts
            # Set the account database date to the new entry date
            self.set_end_date(latest_dates[-1])

    def grab_account_names(self):
        return self.accounts.keys()

    def grab_account_data(self, account_name: str):
        """ Grab all the account data
        
        Arguments:
            account_name {str} -- account account to retrieve data from
        
        Returns:
            tuple(bool, dict{str: int}) -- boolean holds whether the account should be counted towards the total, dict contains the account record entry data
        """

        if account_name in self.accounts:
            account = self.accounts[account_name]
            return (account.part_of_total, 
                {self.date_parser(key): value for key, value in account.records.items()}, )

    def get_iterations(self):
        """ Get the number of iterations this account database requires between the starting and ending date of the account
        
        Returns:
            int -- number of months, quarters, or years that are between the starting and ending dates depending on the account type
        """

        start_date = self.get_start_date()
        end_date = self.get_end_date()

        if self.get_type() == "Monthly":
            # Format: MM/YYYY
            start_month, start_year = [int(piece) for piece in start_date.split("/")]
            end_month, end_year = [int(piece) for piece in end_date.split("/")]
            return (end_year - start_year) * 12 + (end_month - start_month) + 1
        elif self.get_type() == "Quarterly":
            # Format: Q# YYYYY
            start_quarter = int(start_date.split(" ")[0][1])  # Get the number after the Q
            start_year = int(start_date.split(" ")[1])
            end_quarter = int(end_date.split(" ")[0][1])
            end_year = int(end_date.split(" ")[1])

            return (end_year - start_year) * 4 + (end_quarter - start_quarter) + 1
        elif self.get_type() == "Yearly":
            # Format: YYYY
            return int(end_date) - int(start_date) + 1

    def grab_dates(self):
        """
        Grab all the dates this database covers
        :return: a list of all available dates starting from earliest to latest + an extra date beyond the latest
                The extra date is so there is space to add a new entry in the table
        """
        start_date = self.start_date
        year, month = [int(piece) for piece in start_date.split("-")]
        iterations = self.get_iterations() + 1

        dates = []
        for _ in range(1, iterations + 1):
            dates.append(self.date_parser('{0}-{1:02d}'.format(year, month)))
            if self.type == "Monthly":
                month += 1
                if month == 13:
                    month = 1
                    year += 1
            elif self.type == "Quarterly":
                month += 3
                if month >= 13:
                    month = 1
                    year += 1
            elif self.type == "Yearly":
                year += 1
        return dates

    def date_parser(self, input_date):
        """
        Takes an ISO formatted date string and returns a date string based on database type
        :type input_date: str
        :param input_date: date formatted in %Y-%m
        :return: a string in the format below based on database type
                MM/YYYY format for 'Monthly' type
                QQ YYYY format for 'Quarterly' type
                YYYY format for 'Yearly' type
        """
        self.check_date_format(input_date)

        year, month = input_date.split("-")
        if self.get_type() == "Monthly":
            return '{0}/{1}'.format(month, year)
        elif self.get_type() == "Quarterly":
            quarter = (int(month) - 1) // 3 + 1
            return 'Q{0} {1}'.format(quarter, year)
        elif self.get_type() == "Yearly":
            return year
    
    @staticmethod
    def check_date_format(input_date):
        try:
            datetime.datetime.strptime(input_date, '%Y-%m')
        except ValueError:
            raise ValueError('Value Error: Invalid date format. Date must be in YYYY-MM format')


class Account(Persistent):
    def __init__(self, part_of_total: bool):
        self.records = OIBTree.BTree()
        self.part_of_total = part_of_total
        self.latest_date = ''

    def add_update_record(self, record_date: str, amount: int):
        self.records[record_date] = amount
        if not self.latest_date or self.latest_date < record_date:
            # Record date occurs after latest date, update latest date with new record date
            self.latest_date = record_date

    def remove_record(self, record_date: str):
        del self.records[record_date]
        if self.latest_date == record_date:
            # Record date being removed occurs at the latest date time, update latest date with the previous latest date
            self.latest_date = sorted(self.records.keys())[-1]
