"""
Module for building account statements from account events
"""

from account_events import MONEY_DEPOSITED, MONEY_TRANSFERED
from account_events import MONEY_WITHDRAWN, ACCOUNT_CREATED, ACCOUNT_DELETED
from account_statement import AccountStatement


class AccountStatementBuilder(object):

    "A class for building account statement from account events"

    def __init__(self, account):
        self.last_withdrawal_number = -1
        self.account_exists = False
        self.account = account
        self.account_statement = AccountStatement(account)
        self.updaters = {
            MONEY_DEPOSITED: self._on_deposit,
            MONEY_WITHDRAWN: self._on_withdrawal,
            MONEY_TRANSFERED: self._on_transfer,
            ACCOUNT_CREATED: self._on_creation,
            ACCOUNT_DELETED: self._on_deletion
        }

    def update_account_statement(self, event):
        "Update an account statement by an event"
        event_type = event["event_type"]
        self.updaters[event_type].__call__(event)

    def _on_creation(self, _):
        "Update account statement by an account creation event"
        self.account_exists = True

    def _on_deletion(self, _):
        "Update account statement by an account deletion event"
        self.account_statement.reset()
        self.account_exists = False
        self.last_withdrawal_number = -1

    def _on_transfer(self, event):
        "Update account statement by a withdrawal event and return last withdrawal number"
        if self.account == event["account_withdrawn"]:
            self.account_statement.add_transaction(
                title="Transfer to another account",
                timestamp=event["timestamp"],
                balance_diff=-event["amount"]
            )
            self.last_withdrawal_number = event["withdrawal_number"]
        elif self.account == event["account_credited"]:
            self.account_statement.add_transaction(
                title="Transfer from another account",
                timestamp=event["timestamp"],
                balance_diff=event["amount"]
            )

    def _on_withdrawal(self, event):
        "Update account statement by a withdrawal event"
        self.account_statement.add_transaction(
            title="Withdraw",
            timestamp=event["timestamp"],
            balance_diff=-event["amount"]
        )
        self.last_withdrawal_number = event["withdrawal_number"]

    def _on_deposit(self, event):
        "Update account statement by a deposit event"
        self.account_statement.add_transaction(
            title="Deposit",
            timestamp=event["timestamp"],
            balance_diff=event["amount"]
        )
