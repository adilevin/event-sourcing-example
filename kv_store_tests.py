import unittest

from kv_store import KVStore

TEST_HOST = "localhost"
TEST_PORT = 27017
TEST_DB = "test_db"


class TestKVStore(unittest.TestCase):

    def setUp(self):
        KVStore.reset(host=TEST_HOST, port=TEST_PORT, db_name=TEST_DB)
        self.kv_store = KVStore(
            host=TEST_HOST, port=TEST_PORT, db_name=TEST_DB)

    def test_empty_kv_store(self):
        self.assertIsNone(self.kv_store.get("some key"))

    def test_set_get(self):
        value = {"data": [5, 6, 7]}
        self.kv_store.set("key1", value)
        self.assertDictEqual(value, self.kv_store.get("key1"))


if __name__ == '__main__':
    unittest.main()
