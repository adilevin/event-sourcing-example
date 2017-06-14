
class SeqNumAlreadyUsedException(Exception):
    pass


class DuplicateKeyException(Exception):
    pass

class EventStore(object):

    def add_event(self, event):
        pass
