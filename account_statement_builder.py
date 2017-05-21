"""
Module for building account statements from account events
"""

from account_events import MONEY_DEPOSITED, MONEY_TRANSFERED
from account_events import MONEY_WITHDRAWN, ACCOUNT_CREATED, ACCOUNT_DELETED

def update_account_statement(event, account_statement, account,
                             account_exists, last_withdrawal_number):
    "Update an account statement by an event"
    event_type = event["event_type"]
    if event_type == ACCOUNT_CREATED:
        account_exists = True
    elif event_type == ACCOUNT_DELETED:
        account_statement.reset()
        account_exists = False
        last_withdrawal_number = -1
    elif event_type == MONEY_DEPOSITED:
        _update_by_deposit_event(account_statement, event)
    elif event_type == MONEY_WITHDRAWN:
        last_withdrawal_number = _update_by_withdrawal_event(
            account_statement, event)
    elif event_type == MONEY_TRANSFERED:
        last_withdrawal_number = _update_by_transfer_event(
            account, event, account_statement, last_withdrawal_number)
    return account_exists, last_withdrawal_number


def _update_by_transfer_event(account, event, account_statement, last_withdrawal_number):
    "Update account statement by a withdrawal event and return last withdrawal number"
    if account == event["account_withdrawn"]:
        account_statement.add_transaction(
            title="Transfer to another account",
            timestamp=event["timestamp"],
            balance_diff=-event["amount"]
        )
        last_withdrawal_number = event["withdrawal_number"]
    elif account == event["account_credited"]:
        account_statement.add_transaction(
            title="Transfer from another account",
            timestamp=event["timestamp"],
            balance_diff=event["amount"]
        )
    return last_withdrawal_number


def _update_by_withdrawal_event(account_statement, event):
    "Update account statement by a withdrawal event and return last withdrawal number"
    account_statement.add_transaction(
        title="Withdraw",
        timestamp=event["timestamp"],
        balance_diff=-event["amount"]
    )
    return event["withdrawal_number"]


def _update_by_deposit_event(account_statement, event):
    "Update account statement by a deposit event"
    account_statement.add_transaction(
        title="Deposit",
        timestamp=event["timestamp"],
        balance_diff=event["amount"]
    )
