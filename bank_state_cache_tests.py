"""
Unittests for BankStateCache
"""

import unittest

from bank_state_cache import BankStateCache

TEST_HOST = "localhost"
TEST_PORT = 27017
TEST_DB = "test_db"


class TestBankStateCache(unittest.TestCase):
    "Tests for EventStore class"

    def setUp(self):
        "Reset the cache"
        BankStateCache.reset(host=TEST_HOST, port=TEST_PORT, db_name=TEST_DB)
        self.bank_state_cache = BankStateCache(
            host=TEST_HOST, port=TEST_PORT, db_name=TEST_DB)

    def test_empty_cache(self):
        "The empty cache should return None for any account"
        self.assertIsNone(self.bank_state_cache.get_cached_state("acc"))

    def test_insertion(self):
        "An inserted state should be fetched"
        self.bank_state_cache.update("acc", {"data": 5})
        cached_state = self.bank_state_cache.get_cached_state("acc")
        self.assertDictEqual({"data": 5}, cached_state)


if __name__ == '__main__':
    unittest.main()
