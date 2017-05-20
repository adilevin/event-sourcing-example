"""
Unittests for Event Sourcing example code
"""

import unittest

TEST_HOST = "localhost"
TEST_PORT = 27017
TEST_DB = "test_db"

from bank import Bank
from bank import AccountDoesNotExistException, NotEnoughMoneyForWithdrawalException


class TestBank(unittest.TestCase):
    "Tests for Bank class"

    def setUp(self):
        "Reset the event store"
        Bank.reset(host=TEST_HOST, port=TEST_PORT, db_name=TEST_DB)
        self.bank = Bank(host=TEST_HOST, port=TEST_PORT, db_name=TEST_DB)

    def test_empty_bank(self):
        "The empty event store should have no account"
        with self.assertRaises(AccountDoesNotExistException):
            self.bank.get_balance("captain america")

    def test_empty_account(self):
        "An empty account has zero balance"
        self.bank.create_account("captain america")
        self.assertEquals(0, self.bank.get_balance("captain america"))

    def test_deleted_account(self):
        "A deleted accont does not exist"
        self.bank.create_account("captain america")
        self.bank.delete_account("captain america")
        with self.assertRaises(AccountDoesNotExistException):
            self.bank.get_balance("captain america")

    def test_single_deposit(self):
        "An empty account has zero balance"
        self.bank.create_account("captain america")
        self.bank.deposit("captain america", 50)
        self.assertEquals(50, self.bank.get_balance("captain america"))

    def test_deposits_and_withdrawals(self):
        "Multiple deposits and withdrawals should sum up correctly"
        self.bank.create_account("captain america")
        self.bank.deposit("captain america", 50)
        self.bank.deposit("captain america", 70)
        self.bank.withdraw("captain america", 80)
        self.assertEquals(40, self.bank.get_balance("captain america"))

    def test_two_withdrawals(self):
        "Enable two withdrawals if there is enough money in the account"
        self.bank.create_account("captain america")
        self.bank.deposit("captain america", 50)
        self.bank.withdraw("captain america", 20)
        self.bank.withdraw("captain america", 10)
        self.assertEquals(20, self.bank.get_balance("captain america"))

    def test_forbidden_withdrawal(self):
        "Enable two withdrawals if there is enough money in the account"
        self.bank.create_account("captain america")
        self.bank.deposit("captain america", 50)
        self.bank.withdraw("captain america", 20)
        with self.assertRaises(NotEnoughMoneyForWithdrawalException):
            self.bank.withdraw("captain america", 60)

    def test_transfer_money(self):
        "Transfer money between two accounts with sufficient funds"
        self.bank.create_account("captain america")
        self.bank.create_account("iron man")
        self.bank.deposit("captain america", 1000)
        self.bank.deposit("iron man", 500)
        self.bank.transfer(from_account="iron man",
                           to_account="captain america",
                           amount=200)
        self.assertEquals(1200, self.bank.get_balance("captain america"))
        self.assertEquals(300, self.bank.get_balance("iron man"))


if __name__ == '__main__':
    unittest.main()
