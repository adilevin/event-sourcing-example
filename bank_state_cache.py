"""
A persistent cache for bank state
"""

from pymongo import MongoClient


class BankStateCache(object):

    """
        A cache of account states
    """

    def __init__(self, host="localhost", port=27017, db_name="bank_state_cache"):
        self.client = MongoClient(host=host, port=port)
        self.collection = self.client[db_name].bank_state_cache

    def update(self, account, state):
        "Update the cached state of an account"
        self.collection.update_one(
            filter={"_id": account},
            upsert=True,
            update={"$set": {
                "_id": account,
                "state": state
            }})

    def get_cached_state(self, account):
        "Get the cached state of an account"
        doc = self.collection.find_one(filter={"_id": account})
        return doc and doc["state"]

    @staticmethod
    def reset(host, port, db_name):
        "clear the cache"
        client = MongoClient(host=host, port=port)
        client.drop_database(db_name)
