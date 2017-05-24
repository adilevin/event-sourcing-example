from messages_projector import MessagesProjector
from messaging_cmd_handler import MessagingCmdHandler
from mongodb_messages_projection import MongoDBMessagesProjection
from mongodb_event_store import MongoDBEventStore


def create_messages_cqrs(prod_config=False, reset=False):
    db_name_prefix = prod_config and "messaging" or "test_messaging"
    return _create_messages_cqrs(host="localhost", port=27017, db_name_prefix=db_name_prefix, reset=reset)


def _create_messages_cqrs(host, port, db_name_prefix, reset):
    if reset:
        MongoDBMessagesProjection.reset(
            host=host, port=port, db_name=db_name_prefix + "_projected_msg_store")
        MongoDBEventStore.reset(
            host=host, port=port, db_name=db_name_prefix + "_event_store")
    messages_store = MongoDBMessagesProjection(
        host=host, port=port, db_name=db_name_prefix + "_projected_msg_store")
    event_store = MongoDBEventStore(
        host=host, port=port, db_name=db_name_prefix + "_event_store")
    cmd_handler = MessagingCmdHandler(event_store)
    messages_projector = MessagesProjector(
        event_store=event_store, messages_store=messages_store)
    return cmd_handler, messages_projector, messages_store
