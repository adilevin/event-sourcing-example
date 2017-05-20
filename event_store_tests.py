"""
Unittests for Event Sourcing example code
"""

import unittest

from event_store import EventStore

TEST_HOST = "localhost"
TEST_PORT = 27017
TEST_DB = "test_db"


class TestEventStore(unittest.TestCase):
    "Tests for EventStore class"

    def setUp(self):
        "Reset the event store"
        self.events_collection = EventStore.reset(
            host=TEST_HOST, port=TEST_PORT, db_name=TEST_DB)
        self.event_store = EventStore(
            host=TEST_HOST, port=TEST_PORT, db_name=TEST_DB)

    def test_empty_event_store(self):
        "The empty event store should have no events"
        events = self.event_store.get_events()
        self.assertEquals(0, len(events))

    def test_insertion_of_single_event(self):
        "A single event should be inserted correctly"
        self._test_insertion_of_events(1)

    def test_insertion_of_three_events(self):
        "Three events should be inserted correctly"
        self._test_insertion_of_events(3)

    def _test_insertion_of_events(self, num_events):
        "N events should be inserted correctly"
        inserted_events = self._insert_events(num_events)
        read_events = self.event_store.get_events()
        self.assertEquals(num_events, len(read_events))
        for i in range(num_events):
            self._assert_event(inserted_events[i], i, read_events[i])

    def test_get_events_with_offset(self):
        "get events with offset should run correctly"
        inserted_events = self._insert_events(5)
        read_events = self.event_store.get_events(from_seq_num=2)
        self.assertEquals(3, len(read_events))
        for i in range(3):
            self._assert_event(
                expected_payload=inserted_events[i + 2],
                expected_seqnum=i + 2,
                event=read_events[i])

    def test_get_events_with_limit(self):
        "get events with offset should run correctly"
        inserted_events = self._insert_events(5)
        read_events = self.event_store.get_events(from_seq_num=1, limit=2)
        self.assertEquals(2, len(read_events))
        self._assert_event(
            expected_payload=inserted_events[2],
            expected_seqnum=2,
            event=read_events[1])

    def test_events_by_aggregate_sorted(self):
        "get events for an aggregate should return events sorted by seq_num"
        for seq_num in [1, 4, 2, 3]:
            self.event_store._add_event_with_given_seq_num(
                payload={"aggregate_id": "x"}, seq_num=seq_num)
        read_events = self.event_store.get_events_for_aggregate(aggregate_id="x")
        for i in range(3):
            self.assertGreater(
                read_events[i + 1]["seq_num"], read_events[i]["seq_num"])

    def test_all_events_sorted(self):
        "get all should return events sorted by seq_num"
        for seq_num in [1, 4, 2, 3]:
            self.event_store._add_event_with_given_seq_num(
                payload={"aggregate_id": seq_num}, seq_num=seq_num)
        read_events = self.event_store.get_events()
        for i in range(3):
            self.assertGreater(
                read_events[i + 1]["seq_num"], read_events[i]["seq_num"])

    def test_get_events_for_aggregate(self):
        "get events with filter should run correctly"
        for _ in range(4):
            self.event_store.add_event(payload={"aggregate_id": "x"})
            self.event_store.add_event(payload={"aggregate_id": "y"})
        read_events = self.event_store.get_events_for_aggregate(
            aggregate_id="x")
        self.assertEquals(4, len(read_events))
        for event in read_events:
            self.assertEquals(0, event["seq_num"] % 2)

    def _insert_events(self, num_of_events_to_insert):
        "Insert N events"
        inserted_events = []
        for i in range(num_of_events_to_insert):
            event = {
                "aggregate_id": i,
                "data": i * 10
            }
            self.event_store.add_event(event)
            inserted_events.append(event)
        return inserted_events

    def _assert_event(self, expected_payload, expected_seqnum, event):
        "Asset that an event is as expected"
        self.assertEqual(
            expected_payload["aggregate_id"], event["aggregate_id"])
        self.assertEqual(expected_payload["data"], event["data"])
        self.assertEqual(expected_seqnum, event["seq_num"])
        self.assertIsNotNone(event["time_stamp"])


if __name__ == '__main__':
    unittest.main()
