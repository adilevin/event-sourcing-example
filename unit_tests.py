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
        events = self.event_store.get_events(from_seq_num=0)
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
        read_events = self.event_store.get_events(from_seq_num=0)
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

    def test_get_events_with_filter(self):
        "get events with filter should run correctly"
        self._insert_events(5)
        read_events = self.event_store.get_events(
            events_filter={"aggregate_id": {"$gt": 2}})
        self.assertEquals(2, len(read_events))
        for event in read_events:
            self.assertTrue(event["aggregate_id"] > 2)

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


from bank import Bank, AccountDoesNotExistException, NotEnoughMoneyForWithdrawalException


class TestBank(unittest.TestCase):
    "Tests for Bank class"

    def setUp(self):
        "Reset the event store"
        Bank.reset(host=TEST_HOST, port=TEST_PORT, db_name=TEST_DB)
        self.bank = Bank(host=TEST_HOST, port=TEST_PORT, db_name=TEST_DB)

    def test_empty_bank(self):
        "The empty event store should have no account"
        with self.assertRaises(AccountDoesNotExistException):
            self.bank.get_balance("captain america")

    def test_empty_account(self):
        "An empty account has zero balance"
        self.bank.create_account("captain america")
        self.assertEquals(0, self.bank.get_balance("captain america"))

    def test_deleted_account(self):
        "A deleted accont does not exist"
        self.bank.create_account("captain america")
        self.bank.delete_account("captain america")
        with self.assertRaises(AccountDoesNotExistException):
            self.bank.get_balance("captain america")

    def test_single_deposit(self):
        "An empty account has zero balance"
        self.bank.create_account("captain america")
        self.bank.deposit("captain america", 50)
        self.assertEquals(50, self.bank.get_balance("captain america"))

    def test_deposits_and_withdrawals(self):
        "Multiple deposits and withdrawals should sum up correctly"
        self.bank.create_account("captain america")
        self.bank.deposit("captain america", 50)
        self.bank.deposit("captain america", 70)
        self.bank.withdraw("captain america", 80)
        self.assertEquals(40, self.bank.get_balance("captain america"))

    def test_two_withdrawals(self):
        "Enable two withdrawals if there is enough money in the account"
        self.bank.create_account("captain america")
        self.bank.deposit("captain america", 50)
        self.bank.withdraw("captain america", 20)
        self.bank.withdraw("captain america", 10)
        self.assertEquals(20, self.bank.get_balance("captain america"))

    def test_forbidden_withdrawal(self):
        "Enable two withdrawals if there is enough money in the account"
        self.bank.create_account("captain america")
        self.bank.deposit("captain america", 50)
        self.bank.withdraw("captain america", 20)
        with self.assertRaises(NotEnoughMoneyForWithdrawalException):
            self.bank.withdraw("captain america", 60)

    def test_transfer_money(self):
        "Transfer money between two accounts with sufficient funds"
        self.bank.create_account("captain america")
        self.bank.create_account("iron man")
        self.bank.deposit("captain america", 1000)
        self.bank.deposit("iron man", 500)
        self.bank.transfer(from_account="iron man",
                           to_account="captain america",
                           amount=200)
        self.assertEquals(1200, self.bank.get_balance("captain america"))
        self.assertEquals(300, self.bank.get_balance("iron man"))


if __name__ == '__main__':
    # unittest.main(defaultTest="TestBank")
    unittest.main()
