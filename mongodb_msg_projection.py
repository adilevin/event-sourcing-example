from pymongo import MongoClient


class MongoDBMsgProjection(object):

    def __init__(self, host="localhost", port=27017, db_name="msg_projection"):
        self.client = MongoClient(host=host, port=port)
        self.msg_per_user = self.client[db_name].msg_per_user
        self.num_unread_msg_per_user = self.client[db_name].num_unread_msg_per_user
        self.msg_cur_seq_num = self.client[db_name].cur_seq_num

    def get_cur_seq_num(self):
        doc = self.msg_cur_seq_num.find_one()
        if doc:
            return doc["seq_num"]
        else:
            self._update_seq_num(-1)
            return -1

    def get_msg_for_user(self, user_id):
        cursor = self.msg_per_user.find(
            filter={"user_id": user_id}, projection={"_id": False, "user_id": False})
        return [msg for msg in cursor]

    def mark_msg_as_read(self, user_id, msg_id, new_seq_num):
        self.msg_per_user.update_one(
            filter={"user_id": user_id, "msg_id": msg_id},
            update={"$set": {"read": True}})
        self._update_num_unread_msg(user_id)
        self._update_seq_num(new_seq_num)

    def add_msg_for_user(self, user_id, msg_id, new_seq_num):
        self.msg_per_user.insert(
            {"user_id": user_id, "msg_id": msg_id, "read": False})
        self._update_num_unread_msg(user_id)
        self._update_seq_num(new_seq_num)

    def _update_seq_num(self, new_seq_num):
        self.msg_cur_seq_num.update_one(
            filter={},
            update={"$set": {"seq_num": new_seq_num}}, upsert=True)

    def _update_num_unread_msg(self, user_id):
        count = self.msg_per_user.find(
            {"user_id": user_id, "read": False}).count()
        self.num_unread_msg_per_user.update_one(
            filter={"user_id": user_id}, update={"$set": {"num_unread": count}}, upsert=True)

    @staticmethod
    def reset(host, port, db_name):
        client = MongoClient(host=host, port=port)
        client.drop_database(db_name)
