import messaging_events


class MessagesProjector(object):

    def __init__(self, event_store, messages_store):
        self.event_store = event_store
        self.messages_store = messages_store
        self.updaters = {
            messaging_events.MESSAGE_READ_BY_USER: self._on_msg_read,
            messaging_events.MESSAGE_SENT_TO_USER: self._on_msg_sent
        }

    def run_infinite_refresh_loop(self, seconds_to_sleep, max_num_events_to_process):
        import time, sys
        while True:
            if self.refresh(max_num_events_to_process):
                character = 'x'
            else:
                character = '.'
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(seconds_to_sleep)

    def refresh(self, max_num_events_to_process):
        cur_seq_num = self.messages_store.get_cur_seq_num()
        any_events_found = False
        events = self.event_store.get_events(
            limit=max_num_events_to_process, from_seq_num=cur_seq_num+1)
        for event in events:
            self.updaters[event["event_type"]].__call__(event)
            any_events_found = True
        return any_events_found

    def _update_by_event(self, event):
        event_type = event["event_type"]
        self.updaters[event_type].__call__(event)

    def _on_msg_read(self, event):
        self.messages_store.mark_msg_as_read(
            user_id=event["aggregate_id"],
            message_id=event["message_id"],
            new_seq_num=event["seq_num"])

    def _on_msg_sent(self, event):
        self.messages_store.add_msg_for_user(
            user_id=event["aggregate_id"],
            message_id=event["message_id"],
            new_seq_num=event["seq_num"])
