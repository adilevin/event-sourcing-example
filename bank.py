"""
Bank API, based on an event store
"""

import pymongo
from event_store import EventStore


class AccountDoesNotExistException(Exception):
    "Exception in case account does not exist"


class NotEnoughMoneyForWithdrawalException(Exception):
    "Exception in caes account does not have enough money for a withdrawal"


ACCOUNT_CREATED = "account_created"
ACCOUNT_DELETED = "account_deleted"
MONEY_DEPOSITED = "money_deposited"
MONEY_WITHDRAWN = "money_withdrawn"


class Bank(object):

    "API for Bank deposits and withdrawals"

    def __init__(self, host="localhost", port=27017, db_name="bank_event_store"):
        self.event_store = EventStore(host=host, port=port, db_name=db_name)

    def get_balance(self, account):
        "Get balance of given account"
        account_events = self.event_store.get_events({"account": account})
        account_balance, _ = self._calc_account_balance(
            account_events)
        if account_balance == None:
            raise AccountDoesNotExistException
        else:
            return account_balance

    def create_account(self, account):
        "create an account"
        self.event_store.add_event(
            {"event_type": ACCOUNT_CREATED, "account": account})

    def delete_account(self, account):
        "delete an account"
        self.event_store.add_event(
            {"event_type": ACCOUNT_DELETED, "account": account})

    def deposit(self, account, amount):
        "deposit money to an account"
        self.event_store.add_event(
            {"event_type": MONEY_DEPOSITED, "account": account, "amount": amount})

    def transfer(self, from_account, to_account, amount):
        "transfer money fro one account to another"
        self.withdraw(from_account, amount)
        self.deposit(to_account, amount)

    def withdraw(self, account, amount):
        "withdraw money to an account"
        account_events = self.event_store.get_events({"account": account})
        account_balance, last_withdrawal_number = self._calc_account_balance(
            account_events)
        if account_balance < amount:
            raise NotEnoughMoneyForWithdrawalException
        self.event_store.add_event({
            "event_type": MONEY_WITHDRAWN,
            "account": account,
            "account_withdrawn": account,
            "amount": amount,
            "withdrawal_number": last_withdrawal_number + 1})

    def _calc_account_balance(self, account_events):
        "Calculate balance of an account given its events"
        account_balance = None
        last_withdrawal_number = -1
        for event in account_events:
            event_type = event["event_type"]
            if event_type == ACCOUNT_CREATED:
                account_balance = 0
            elif event_type == ACCOUNT_DELETED:
                account_balance = None
                last_withdrawal_number = -1
            elif event_type == MONEY_DEPOSITED:
                account_balance += event["amount"]
            elif event_type == MONEY_WITHDRAWN:
                account_balance -= event["amount"]
                last_withdrawal_number = event["withdrawal_number"]
        return account_balance, last_withdrawal_number

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
        events_collection.create_index("account")
