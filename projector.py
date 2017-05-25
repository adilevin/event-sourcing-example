
class Projector(object):

    def __init__(self, event_store, projection_store, updaters):
        self.event_store = event_store
        self.projection_store = projection_store
        self.updaters = updaters

    def run_infinite_refresh_loop(self, seconds_to_sleep, max_num_events_to_process):
        import time
        import sys
        while True:
            num_new_events = self.refresh(max_num_events_to_process)
            if num_new_events == 0:
                sys.stdout.write('.')
            else:
                sys.stdout.write(' ' + str(num_new_events) + ' ')
            sys.stdout.flush()
            time.sleep(seconds_to_sleep)

    def refresh(self, max_num_events_to_process):
        cur_seq_num = self.projection_store.get_cur_seq_num()
        events = self.event_store.get_events(
            limit=max_num_events_to_process, from_seq_num=cur_seq_num + 1)
        for event in events:
            self._update_by_event(event)
        return len(events)

    def _update_by_event(self, event):
        event_type = event["event_type"]
        self.updaters[event_type].__call__(event)
