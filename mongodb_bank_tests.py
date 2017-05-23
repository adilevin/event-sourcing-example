from bank_tests import BankBaseTests
import bank_factory
import mongodb_utils

TEST_DB = "test_bank"


class TestMongoDBBank(BankBaseTests.TestBank):

    def setUp(self):
        bank = bank_factory.create_bank_with_mongodb_event_store(
            host="localhost", port=27017, db_name=TEST_DB, reset=True)
        setattr(self, "bank", bank)
        # The above statement is like self.bank=bank, but it's needed because
        # it is outside the constructor

    @classmethod
    def tearDownClass(cls):
        mongodb_utils.drop_db(host="localhost", port=27017, db_name=TEST_DB)
