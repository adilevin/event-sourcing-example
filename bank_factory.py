
from pymongo import ASCENDING
from mongodb_event_store import MongoDBEventStore
from bank import Bank

def create_bank_with_mongodb_event_store(host, port, db_name, reset=False):
    if reset:
        reset_bank_mongodb_event_store(host, port, db_name)
    event_store = MongoDBEventStore(host=host, port=port, db_name=db_name)
    return Bank(event_store)

def reset_bank_mongodb_event_store(host, port, db_name):
    events_collection = MongoDBEventStore.reset(
        host=host, port=port, db_name=db_name)
    events_collection.create_index(
        keys=[("account_withdrawn", ASCENDING), ("withdrawal_number", ASCENDING)],
        name="widthdrawal_compound_index", unique=True,
        partialFilterExpression={"account_withdrawn": {"$exists": True}})
