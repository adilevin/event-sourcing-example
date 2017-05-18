"""
The event store
"""

from pymongo import MongoClient, ReturnDocument
import datetime


class EventStore(object):

    "The event store"

    def __init__(self, host="localhost", port=27017, db_name="event_store"):
        self.client = MongoClient(host=host, port=port)
        self.events = self.client[db_name].events
        self.counters = self.client[db_name].counters

    def add_event(self, payload):
        "add an event in the event store"
        event_payload = dict(payload)
        event_payload.update({
            "seq_num": self._get_next_seq_num(),
            "time_stamp": datetime.datetime.now().isoformat()
        })
        self.events.insert(event_payload)

    def get_events(self, events_filter=None, from_seq_num=0):
        "get all events beginning at a given sequence number"
        filter_expression = {"seq_num": {"$gte": from_seq_num}}
        filter_expression.update(events_filter or {})
        cursor = self.events.find(filter_expression)
        return [event for event in cursor]

    @staticmethod
    def reset(host="localhost", port=27017, db_name="event_store"):
        "clear the event store"
        client = MongoClient(host=host, port=port)
        client.drop_database(db_name)
        client[db_name].counters.insert({"seq_num": 0})

    def _get_next_seq_num(self):
        "get next sequence number"
        ret = self.counters.find_one_and_update(
            filter={},
            update={"$inc": {"seq_num": 1}},
            return_document=ReturnDocument.BEFORE)
        return ret["seq_num"]


if __name__ == "__main__":
    EventStore.reset("localhost", 27017, "test")
