import messaging_events
from projector import Projector


class MessagesProjector(Projector):

    def __init__(self, event_store, messages_store):
        super(self.__class__, self).__init__(
            event_store=event_store,
            projection_store=messages_store,
            updaters={
                messaging_events.MESSAGE_READ_BY_USER: self._on_msg_read,
                messaging_events.MESSAGE_SENT_TO_USER: self._on_msg_sent
            })

    def _on_msg_read(self, event):
        self.projection_store.mark_msg_as_read(
            user_id=event["aggregate_id"],
            message_id=event["message_id"],
            new_seq_num=event["seq_num"])

    def _on_msg_sent(self, event):
        self.projection_store.add_msg_for_user(
            user_id=event["aggregate_id"],
            message_id=event["message_id"],
            new_seq_num=event["seq_num"])
