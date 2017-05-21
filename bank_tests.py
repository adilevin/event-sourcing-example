import unittest

from bank import AccountDoesNotExistException, NotEnoughMoneyForWithdrawalException
import factory


class TestBank(unittest.TestCase):

    def setUp(self):
        self.bank = factory.create_bank_with_mongodb_event_store(
            host="localhost", port=27017, db_name="test_bank", reset=True)

    def test_empty_bank(self):
        with self.assertRaises(AccountDoesNotExistException):
            self.bank.get_balance("captain america")

    def test_empty_account(self):
        self.bank.create_account("captain america")
        self.assertEquals(0, self.bank.get_balance("captain america"))

    def test_deleted_account(self):
        self.bank.create_account("captain america")
        self.bank.delete_account("captain america")
        with self.assertRaises(AccountDoesNotExistException):
            self.bank.get_balance("captain america")

    def test_single_deposit(self):
        self.bank.create_account("captain america")
        self.bank.deposit("captain america", 50)
        account_statement = self.bank.get_statement("captain america")
        self.assertEquals(50, self.bank.get_balance("captain america"))
        self.assertEquals(1, account_statement.get_num_of_transactions())

    def test_deposits_and_withdrawals(self):
        self.bank.create_account("captain america")
        self.bank.deposit("captain america", 50)
        self.bank.deposit("captain america", 70)
        self.bank.withdraw("captain america", 80)
        self.assertEquals(40, self.bank.get_balance("captain america"))

    def test_two_withdrawals(self):
        self.bank.create_account("captain america")
        self.bank.deposit("captain america", 50)
        self.bank.withdraw("captain america", 20)
        self.bank.withdraw("captain america", 10)
        self.assertEquals(20, self.bank.get_balance("captain america"))

    def test_forbidden_withdrawal(self):
        self.bank.create_account("captain america")
        self.bank.deposit("captain america", 50)
        self.bank.withdraw("captain america", 20)
        with self.assertRaises(NotEnoughMoneyForWithdrawalException):
            self.bank.withdraw("captain america", 60)

    def test_transfer_money(self):
        self.bank.create_account("captain america")
        self.bank.create_account("iron man")
        self.bank.deposit("captain america", 1000)
        self.bank.deposit("iron man", 500)
        self.bank.transfer(from_account="iron man",
                           to_account="captain america", amount=200)
        self.assertEquals(1200, self.bank.get_balance("captain america"))
        self.assertEquals(300, self.bank.get_balance("iron man"))


if __name__ == '__main__':
    unittest.main()
