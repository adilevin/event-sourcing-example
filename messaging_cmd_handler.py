
import messaging_events

class MessagingCmdHandler(object):

    def __init__(self, event_store):
        self.event_store = event_store

    def send_message_to_user(self, user_id, message_id):
        self.event_store.add_event({
            "aggregate_id": user_id,
            "message_id": message_id,
            "event_type": messaging_events.MESSAGE_SENT_TO_USER
        })

    def mark_message_as_read(self, user_id, message_id):
        self.event_store.add_event({
            "aggregate_id": user_id,
            "message_id": message_id,
            "event_type": messaging_events.MESSAGE_READ_BY_USER
        })
