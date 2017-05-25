
class SeqNumAlreadyUsedException(Exception):
    pass


class DuplicateKeyException(Exception):
    pass

class EventStore(object):

    def add_event(self, event):
        pass

    @staticmethod
    def reset():
        raise Exception("This is an abstract class")
