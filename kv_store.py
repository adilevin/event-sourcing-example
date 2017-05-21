from pymongo import MongoClient


class KVStore(object):

    def __init__(self, host="localhost", port=27017, db_name="kv-store"):
        self.client = MongoClient(host=host, port=port)
        self.collection = self.client[db_name].kv

    def set(self, key, value):
        self.collection.update_one(
            filter={"_id": key},
            upsert=True,
            update={"$set": {
                "_id": key,
                "val": value
            }})

    def get(self, key):
        "Get the value at a key, or None if it doesn't exist"
        doc = self.collection.find_one(filter={"_id": key})
        return doc and doc["val"]

    @staticmethod
    def reset(host, port, db_name):
        client = MongoClient(host=host, port=port)
        client.drop_database(db_name)
