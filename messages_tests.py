import unittest

import messages_factory

TEST_HOST = "localhost"
TEST_PORT = 27017

class TestMessaging(unittest.TestCase):

    def setUp(self):
        self.cmd_handler, self.messages_projector, self.messages_store = messages_factory.create_messages_cqrs(
            host="localhost", port=27017, db_name_prefix="test_msgs", reset=True)

    def test_empty_messages_store(self):
        self.assertEquals(-1, self.messages_store.get_cur_seq_num())
        msgs_for_user = self.messages_store.get_messages_for_user("user1")
        self.assertEquals([], msgs_for_user)

    def test_adding_message(self):
        self.cmd_handler.send_message_to_user(
            user_id="user1", message_id="msg1")
        self.messages_projector.refresh(100)
        msgs_for_user = self.messages_store.get_messages_for_user("user1")
        self.assertEquals([{"message_id":"msg1"}], msgs_for_user)

    def test_adding_multiple_messages(self):
        for i in range(3):
            self.cmd_handler.send_message_to_user(
                user_id="user%d" % i, message_id="msg%d" % i)
        self.cmd_handler.send_message_to_user(
            user_id="user0", message_id="another message")
        self.messages_projector.refresh(max_num_events_to_process=3)
        for i in range(3):
            self.assertEquals([{"message_id": "msg%d" % i}],
                              self.messages_store.get_messages_for_user("user%d" % i))
        self.messages_projector.refresh(1)
        self.assertEquals([{"message_id": "another message"}, {"message_id": "msg0"}],
                          self.messages_store.get_messages_for_user("user0"))

    def test_marking_message_as_read(self):
        self.cmd_handler.send_message_to_user(
            user_id="user1", message_id="msg1")
        self.cmd_handler.mark_message_as_read(
            user_id="user1", message_id="msg1")
        self.messages_projector.refresh(100)
        msgs_for_user = self.messages_store.get_messages_for_user("user1")
        self.assertEquals([{"message_id": "msg1", "read": True}], msgs_for_user)


if __name__ == '__main__':
    unittest.main()
