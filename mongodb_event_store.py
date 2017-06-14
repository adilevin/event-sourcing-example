from pymongo import MongoClient, ASCENDING, errors
from event_store import EventStore, SeqNumAlreadyUsedException, DuplicateKeyException
import datetime

class MongoDBEventStore(EventStore):

    def __init__(self, host="localhost", port=27017, db_name="event_store"):
        self.client = MongoClient(host=host, port=port)
        self.events = self.client[db_name].events

    def add_event(self, payload):
        while True:
            # Optimistic locking mechanism for making sure that an event with seq_num N is
            # inserted before an event with seq_num N+1.
            try:
                unused_seq_num = self._get_unused_seq_num()
                self.add_event_with_given_seq_num(payload, unused_seq_num)
                break
            except SeqNumAlreadyUsedException:
                pass

    def _get_unused_seq_num(self):
        cursor = self.events.find(
            projection={"_id": 1},
            sort=[("_id", -1)], limit=1)
        last_seq_num = -1
        for event in cursor:
            last_seq_num = event["_id"]
        return last_seq_num + 1

    def get_events_for_aggregate(self, aggregate_id, limit=0, from_seq_num=0):
        return self._get_filtered_events(
            filter_expression={"aggregate_id": aggregate_id},
            limit=limit,
            from_seq_num=from_seq_num)

    def get_events(self, limit=0, from_seq_num=0):
        return self._get_filtered_events(
            filter_expression={},
            limit=limit,
            from_seq_num=from_seq_num)

    def _get_filtered_events(self, filter_expression, limit=0, from_seq_num=0):
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
        client[db_name].events.create_index(
            keys=[("aggregate_id", ASCENDING),
                  ("_id", ASCENDING)],
            name="index by aggreage id and seq_num")
        return client[db_name].events

    def add_event_with_given_seq_num(self, payload, seq_num):
        "add an event in the event store with a given seq_num. For test purposes"
        try:
            event_payload = dict(payload)
            event_payload.update({
                "_id": seq_num,
                "timestamp": datetime.datetime.now().isoformat()
            })
            self.events.insert(event_payload)
        except errors.DuplicateKeyError as err:
            if err.details["errmsg"].find("index: _id_") > 0:
                raise SeqNumAlreadyUsedException
            else:
                raise DuplicateKeyException
