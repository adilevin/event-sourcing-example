"""
Bank API, based on an event store
"""

import pymongo
from event_store import EventStore
from account_events import MONEY_DEPOSITED, MONEY_TRANSFERED
from account_events import MONEY_WITHDRAWN, ACCOUNT_CREATED, ACCOUNT_DELETED
from account_statement_builder import AccountStatementBuilder


class AccountDoesNotExistException(Exception):
    "Exception in case account does not exist"


class NotEnoughMoneyForWithdrawalException(Exception):
    "Exception in caes account does not have enough money for a withdrawal"


class TransactionFailedTryAgainLater(Exception):
    "Exception in case withdraw failed due to too much contention"


class Bank(object):

    "API for Bank deposits and withdrawals"

    def __init__(self, host="localhost", port=27017, db_name="bank_event_store"):
        self.event_store = EventStore(host=host, port=port, db_name=db_name)

    def get_statement(self, account):
        "Get current account statement including transactions and balance"
        account_statement, _ = self._build_account_statement(account)
        return account_statement

    def get_balance(self, account):
        "Get balance of given account"
        account_statement = self.get_statement(account)
        return account_statement.get_balance()

    def create_account(self, account):
        "create an account"
        self.event_store.add_event(
            {"event_type": ACCOUNT_CREATED, "aggregate_id": account})

    def delete_account(self, account):
        "delete an account"
        self.event_store.add_event(
            {"event_type": ACCOUNT_DELETED, "aggregate_id": account})

    def deposit(self, account, amount):
        "deposit money to an account"
        self.event_store.add_event({
            "event_type": MONEY_DEPOSITED,
            "aggregate_id": account,
            "amount": amount})

    def _transfer_optimistic_locking(self, from_account, to_account, amount):
        """Attempt to trasnfer money. May fail if there is not enough money or if
        another withdraw is happenning in parallel"""
        withdrawn_account_statement, last_withdrawal_number = self._build_account_statement(
            from_account)
        if withdrawn_account_statement.get_balance() < amount:
            raise NotEnoughMoneyForWithdrawalException
        self.event_store.add_event({
            "event_type": MONEY_TRANSFERED,
            "aggregate_id": [from_account, to_account],
            "account_withdrawn": from_account,
            "account_credited": to_account,
            "amount": amount,
            "withdrawal_number": last_withdrawal_number + 1})

    def transfer(self, from_account, to_account, amount):
        "transfer money fro one account to another"
        for _ in range(3):
            try:
                self._transfer_optimistic_locking(
                    from_account=from_account, to_account=to_account, amount=amount)
                break
            except pymongo.errors.DuplicateKeyError:
                raise TransactionFailedTryAgainLater()

    def _withdraw_optimistic_locking(self, account, amount):
        """Attempt to withdraw. May fail if there is not enough money or if
        another withdraw is happenning in parallel"""
        account_statement, last_withdrawal_number = self._build_account_statement(
            account)
        if account_statement.get_balance() < amount:
            raise NotEnoughMoneyForWithdrawalException
        self.event_store.add_event({
            "event_type": MONEY_WITHDRAWN, "aggregate_id": account,
            "account_withdrawn": account, "amount": amount,
            "withdrawal_number": last_withdrawal_number + 1})

    def withdraw(self, account, amount):
        "withdraw money to an account"
        for _ in range(3):
            try:
                self._withdraw_optimistic_locking(account, amount)
                break
            except pymongo.errors.DuplicateKeyError:
                raise TransactionFailedTryAgainLater()

    def _build_account_statement(self, account):
        "Build account state from event store"
        account_events = self.event_store.get_events_for_aggregate(
            aggregate_id=account)
        builder = AccountStatementBuilder(account)
        for event in account_events:
            builder.update_account_statement(event)
        if not builder.account_exists:
            raise AccountDoesNotExistException
        return builder.account_statement, builder.last_withdrawal_number

    @staticmethod
    def reset(host="localhost", port=27017, db_name="bank_event_store"):
        "reset bank events store, including indexes"
        events_collection = EventStore.reset(
            host=host, port=port, db_name=db_name)
        events_collection.create_index(
            keys=[("account_withdrawn", pymongo.ASCENDING),
                  ("withdrawal_number", pymongo.ASCENDING)],
            name="widthdrawal_compound_index",
            unique=True,
            partialFilterExpression={"account_withdrawn": {"$exists": True}})
