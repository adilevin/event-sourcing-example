from pymongo import MongoClient, ASCENDING


class MongoDBMessagesStore(object):

    def __init__(self, host="localhost", port=27017, db_name="messages_store"):
        self.client = MongoClient(host=host, port=port)
        self.messages_per_user = self.client[db_name].messages_per_user
        self.messages_cur_seq_num = self.client[db_name].cur_seq_num

    def get_cur_seq_num(self):
        doc = self.messages_cur_seq_num.find_one()
        if doc:
            return doc["seq_num"]
        else:
            self._update_seq_num(-1)
            return -1

    def get_messages_for_user(self, user_id):
        cursor = self.messages_per_user.find(
            filter={"user_id": user_id}, projection={"_id":False, "message_id":True, "read":True})
        return [msg for msg in cursor]

    def mark_msg_as_read(self, user_id, message_id, new_seq_num):
        self.messages_per_user.update_one(
            filter={"user_id": user_id, "message_id": message_id},
            update={"$set":{"user_id": user_id, "message_id": message_id, "read": True}})
        self._update_seq_num(new_seq_num)

    def add_msg_for_user(self, user_id, message_id, new_seq_num):
        self.messages_per_user.insert({"user_id": user_id, "message_id": message_id})
        self._update_seq_num(new_seq_num)

    def _update_seq_num(self, new_seq_num):
        self.messages_cur_seq_num.update_one(
            filter={},
            update={"$set": {"seq_num": new_seq_num}}, upsert=True)

    @staticmethod
    def reset(host, port, db_name):
        client = MongoClient(host=host, port=port)
        client.drop_database(db_name)
        client[db_name].messages_per_user.create_index(
            keys=[("user_id", ASCENDING),
                  ("message_id", ASCENDING)],
            name="index by user_id and message_id")
