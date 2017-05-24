
import msg_events

class MsgCmdHandler(object):

    def __init__(self, event_store):
        self.event_store = event_store

    def send_msg_to_user(self, user_id, msg_id):
        self.event_store.add_event({
            "aggregate_id": user_id,
            "msg_id": msg_id,
            "event_type": msg_events.MESSAGE_SENT_TO_USER
        })

    def mark_msg_as_read(self, user_id, msg_id):
        self.event_store.add_event({
            "aggregate_id": user_id,
            "msg_id": msg_id,
            "event_type": msg_events.MESSAGE_READ_BY_USER
        })
