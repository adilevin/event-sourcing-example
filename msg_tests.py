import unittest
import msg_factory
import mongodb_utils

TEST_HOST = "localhost"
TEST_PORT = 27017
TEST_DB_NAME_PREFIX = "test_"


class TestMsg(unittest.TestCase):

    def setUp(self):
        self.cmd_handler, self.msg_projector, self.msg_store, self.query_handler = \
            msg_factory.create_msg_cqrs(
                prod_config=False, reset=True)

    @classmethod
    def tearDownClass(cls):
        mongodb_utils.drop_dbs_by_prefix(
            host=TEST_HOST, port=TEST_PORT, db_name_prefix=TEST_DB_NAME_PREFIX)

    def test_empty_msg_store(self):
        self.assertEquals(-1, self.msg_store.get_cur_seq_num())
        msg_for_user = self.msg_store.get_msgs("user1")
        self.assertEquals([], msg_for_user)

    def test_adding_msg(self):
        self.cmd_handler.send_msg_to_user(
            user_id="user1", msg_id="msg1")
        self.msg_projector.refresh(100)
        msg_for_user = self.query_handler.get_msgs("user1")
        self.assertEquals(
            [{"msg_id": "msg1", "read": False}], msg_for_user)

    def test_adding_multiple_msg(self):
        for i in range(3):
            self.cmd_handler.send_msg_to_user(
                user_id="user%d" % i, msg_id="msg%d" % i)
        self.cmd_handler.send_msg_to_user(
            user_id="user0", msg_id="another msg")
        self.msg_projector.refresh(max_num_events_to_process=3)
        for i in range(3):
            self.assertEquals([{"msg_id": "msg%d" % i, "read": False}],
                              self.query_handler.get_msgs("user%d" % i))
        self.msg_projector.refresh(1)
        self.assertEquals([{"msg_id": "msg0", "read": False},
                           {"msg_id": "another msg", "read": False}],
                          self.query_handler.get_msgs("user0"))

    def test_marking_msg_as_read(self):
        self.cmd_handler.send_msg_to_user(
            user_id="user1", msg_id="msg1")
        self.msg_projector.refresh(100)
        self.assertEqual(1, self.query_handler.get_num_unread("user1"))
        self.cmd_handler.mark_msg_as_read(
            user_id="user1", msg_id="msg1")
        self.msg_projector.refresh(100)
        self.assertEqual(0, self.query_handler.get_num_unread("user1"))
        msg_for_user = self.query_handler.get_msgs("user1")
        self.assertEquals(
            [{"msg_id": "msg1", "read": True}], msg_for_user)


if __name__ == '__main__':
    unittest.main()
