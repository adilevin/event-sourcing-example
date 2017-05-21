from account_events import MONEY_DEPOSITED, MONEY_TRANSFERED
from account_events import MONEY_WITHDRAWN, ACCOUNT_CREATED, ACCOUNT_DELETED
from account_statement import AccountStatement


class AccountStatementBuilder(object):

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
        event_type = event["event_type"]
        self.updaters[event_type].__call__(event)

    def _on_creation(self, _):
        self.account_exists = True

    def _on_deletion(self, _):
        self.account_statement.reset()
        self.account_exists = False
        self.last_withdrawal_number = -1

    def _on_transfer(self, event):
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
        self.account_statement.add_transaction(
            title="Withdraw",
            timestamp=event["timestamp"],
            balance_diff=-event["amount"]
        )
        self.last_withdrawal_number = event["withdrawal_number"]

    def _on_deposit(self, event):
        self.account_statement.add_transaction(
            title="Deposit",
            timestamp=event["timestamp"],
            balance_diff=event["amount"]
        )
