"""
The event store
"""

from pymongo import MongoClient, ReturnDocument, ASCENDING
import datetime


class EventStore(object):

    "The event store"

    def __init__(self, host="localhost", port=27017, db_name="event_store"):
        self.client = MongoClient(host=host, port=port)
        self.events = self.client[db_name].events
        self.counters = self.client[db_name].counters

    def add_event(self, payload):
        "add an event in the event store"
        self.add_event_with_given_seq_num(payload, self._get_next_seq_num())

    def get_events_for_aggregate(self, aggregate_id, limit=0, from_seq_num=0):
        "get all events beginning at a given sequence number"
        return self._get_filtered_events(
            filter_expression={"aggregate_id": aggregate_id},
            limit=limit,
            from_seq_num=from_seq_num)

    def get_events(self, limit=0, from_seq_num=0):
        "get all events beginning at a given sequence number"
        return self._get_filtered_events(
            filter_expression={},
            limit=limit,
            from_seq_num=from_seq_num)

    def _get_filtered_events(self, filter_expression, limit=0, from_seq_num=0):
        "get all events beginning at a given sequence number"
        the_filter_expression = dict(filter_expression)
        if from_seq_num > 0:
            the_filter_expression.update({"_id": {"$gte": from_seq_num}})
        cursor = self.events.find(
            filter=the_filter_expression,
            sort=[("_id", 1)],
            limit=limit)
        return [event for event in cursor]

    @staticmethod
    def reset(host="localhost", port=27017, db_name="event_store"):
        "clear the event store, and return the events collection"
        client = MongoClient(host=host, port=port)
        client.drop_database(db_name)
        client[db_name].counters.insert({"seq_num": 0})
        client[db_name].events.create_index(
            keys=[("aggregate_id", ASCENDING),
                  ("_id", ASCENDING)],
            name="index by aggreage id and seq_num")
        return client[db_name].events

    def add_event_with_given_seq_num(self, payload, seq_num):
        "add an event in the event store with a given seq_num. For test purposes"
        event_payload = dict(payload)
        event_payload.update({
            "_id": seq_num,
            "seq_num": seq_num,
            "timestamp": datetime.datetime.now().isoformat()
        })
        self.events.insert(event_payload)

    def _get_next_seq_num(self):
        "get next sequence number"
        ret = self.counters.find_one_and_update(
            filter={},
            update={"$inc": {"seq_num": 1}},
            return_document=ReturnDocument.BEFORE)
        return ret["seq_num"]


if __name__ == "__main__":
    EventStore.reset("localhost", 27017, "test")
