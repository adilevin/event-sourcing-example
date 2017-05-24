
class MongoDBMsgQueryHandler(object):

    def __init__(self, msgs_projection):
        # The query handler gets the projection as a dependency, especially because
        # it can have a number of projections as input.
        self.msgs_projection = msgs_projection

    def get_msgs_for_user(self, user_id):
        return self.msgs_projection.get_messages_for_user(user_id)
