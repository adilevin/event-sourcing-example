from messages_projector import MessagesProjector
from messaging_cmd_handler import MessagingCmdHandler
from mongodb_messages_store import MongoDBMessagesStore
from mongodb_event_store import MongoDBEventStore


def create_messages_cqrs(host, port, db_name_prefix, reset=False):
    if reset:
        MongoDBMessagesStore.reset(
            host=host, port=port, db_name=db_name_prefix + "_projected_msg_store")
        MongoDBEventStore.reset(
            host=host, port=port, db_name=db_name_prefix + "_event_store")
    messages_store = MongoDBMessagesStore(
        host=host, port=port, db_name=db_name_prefix + "_projected_msg_store")
    event_store = MongoDBEventStore(
        host=host, port=port, db_name=db_name_prefix + "_event_store")
    cmd_handler = MessagingCmdHandler(event_store)
    messages_projector = MessagesProjector(
        event_store=event_store, messages_store=messages_store)
    return cmd_handler, messages_projector, messages_store
