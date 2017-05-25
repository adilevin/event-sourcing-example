"""
A class for representing the account balance and recent transactions
"""


class AccountStatement(object):

    "A statement of the balance and transactions in an account"

    def __init__(self, account_name):
        self.dictionary = {
            "account_name": account_name,
            "lines": [],
            "balance": 0
        }

    def reset(self):
        "Reset the account"
        self.dictionary["lines"] = []
        self.dictionary["balance"] = 0

    def add_transaction(self, title, timestamp, balance_diff):
        "Write down a transaction and update the balance"
        self.dictionary["balance"] += balance_diff
        self.dictionary["lines"] += [{
            "title": title,
            "balance_diff": balance_diff,
            "timestamp": timestamp,
            "balance_after": self.dictionary["balance"]
        }]

    def get_num_of_transactions(self):
        "Get number of transactions in the account"
        return len(self.dictionary["lines"])

    def get_balance(self):
        "Get current balance"
        return self.dictionary["balance"]

    def as_dict(self):
        "Get statement as a Python dictionary"
        return self.dictionary

    def __str__(self):
        return '\n'.join([_printline(l) for l in self.as_dict()["lines"]])

def _printline(line):
    return '%s %5d %6d %s' % (line["timestamp"], line["balance_after"], line["balance_diff"], line["title"])

if __name__ == "__main__":
    A = AccountStatement("adi")
    A.add_transaction(title="deposit", balance_diff=100, timestamp="4/5/32")
    import json
    print json.dumps(A.as_dict(), indent=2)
