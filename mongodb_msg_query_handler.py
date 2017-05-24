
class MongoDBMsgQueryHandler(object):

    def __init__(self, msg_projection):
        # The query handler gets the projection as a dependency, especially because
        # it can have a number of projections as input.
        self.msg_projection = msg_projection

    def get_msg_for_user(self, user_id):
        return self.msg_projection.get_msg_for_user(user_id)
