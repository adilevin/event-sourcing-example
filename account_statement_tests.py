"""
Unittests for account statements
"""

import unittest

from account_statement import AccountStatement


class TestAccountStatement(unittest.TestCase):
    "Tests for AccountStatement class"

    def setUp(self):
        self.account_statement = AccountStatement(account_name="acc")

    def test_empty_account_statement(self):
        "The empty event statement should return a proper dictionary"
        self.assertDictEqual(
            {"account_name": "acc", "balance": 0, "lines": []}, self.account_statement.as_dict())

    def test_reset(self):
        "Test account reset"
        self.account_statement.add_transaction(
            title="deposit", balance_diff=50, timestamp='3/5/2018')
        self.assertEquals(50, self.account_statement.get_balance())
        self.account_statement.reset()
        self.assertDictEqual(
            {"account_name": "acc", "balance": 0, "lines": []}, self.account_statement.as_dict())

    def test_adding_transactions(self):
        "adding transactions results in balance and transactions update"
        self.account_statement.add_transaction(
            title="deposit", balance_diff=50, timestamp='3/5/2018')
        self.account_statement.add_transaction(
            title="withdraw", balance_diff=-20, timestamp='3/6/2018')
        self.assertEquals(30, self.account_statement.get_balance())
        self.assertDictEqual({
            "account_name": "acc",
            "balance": 30,
            "lines": [{
                "title": "deposit", "balance_diff": 50,
                "balance_after": 50, "timestamp": "3/5/2018"
            }, {
                "title": "withdraw", "balance_diff": -20,
                "balance_after": 30, "timestamp": "3/6/2018"
            }]
        }, self.account_statement.as_dict())
        self.assertEquals(2, self.account_statement.get_num_of_transactions())

