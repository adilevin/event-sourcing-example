import unittest
import mongodb_utils
from mongodb_kv_store import MongoDBKVStore

TEST_DB = "test_kv"

class TestMongoDBKVStore(unittest.TestCase):

    def setUp(self):
        self.kv_store = MongoDBKVStore(
            host="localhost", port=27017, db_name=TEST_DB, reset=True)

    @classmethod
    def tearDownClass(cls):
        mongodb_utils.drop_db(host="localhost", port=27017, db_name=TEST_DB)

    def test_empty_kv_store(self):
        self.assertIsNone(self.kv_store.get("some key"))

    def test_set_get(self):
        value = {"data": [5, 6, 7]}
        self.kv_store.set("key1", value)
        self.assertDictEqual(value, self.kv_store.get("key1"))


if __name__ == '__main__':
    unittest.main()
