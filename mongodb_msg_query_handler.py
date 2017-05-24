
class MongoDBMsgQueryHandler(object):

    def __init__(self, msg_projection):
        # The query handler gets the projection as a dependency, especially because
        # it can have a number of projections as input.
        self.msg_projection = msg_projection

    def get_msgs(self, user_id):
        return self.msg_projection.get_msgs(user_id)

    def get_num_unread(self, user_id):
        return self.msg_projection.get_num_read(user_id)
