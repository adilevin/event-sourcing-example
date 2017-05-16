"""
The event store
"""

from pymongo import MongoClient, ReturnDocument
import datetime


class EventStore(object):

    "The event store"

    def __init__(self):
        self.client = MongoClient()
        self.events = self.client.cqrs.events
        self.counters = self.client.cqrs.counters

    def add_event(self, payload):
        "add an event in the event store"
        event_payload = dict(payload)
        event_payload.update({
            "seq_num": self._get_next_seq_num(),
            "time_stamp": datetime.datetime.now().isoformat()
        })
        self.events.insert(event_payload)

    @staticmethod
    def reset():
        "clear the event store"
        client = MongoClient()
        client.drop_database("cqrs")
        client.cqrs.counters.insert({"seq_num": 0})

    def _get_next_seq_num(self):
        "get next sequence number"
        ret = self.counters.find_one_and_update(
            filter={},
            update={"$inc": {"seq_num": 1}},
            return_document=ReturnDocument.AFTER)
        return ret["seq_num"]
