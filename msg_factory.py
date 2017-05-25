from msg_projector import MsgProjector
from msg_cmd_handler import MsgCmdHandler
from mongodb_msg_projection import MongoDBMsgProjection
from mongodb_event_store import MongoDBEventStore
from msg_query_handler import MsgQueryHandler

def create_msg_cqrs(prod_config=False, reset=False):
    db_name_prefix = prod_config and "msg" or "test_msg"
    return _create_msg_cqrs(host="localhost", port=27017, db_name_prefix=db_name_prefix, reset=reset)


def _create_msg_cqrs(host, port, db_name_prefix, reset):
    if reset:
        MongoDBMsgProjection.reset(
            host=host, port=port, db_name=db_name_prefix + "_projection")
        MongoDBEventStore.reset(
            host=host, port=port, db_name=db_name_prefix + "_event_store")
    msg_projection = MongoDBMsgProjection(
        host=host, port=port, db_name=db_name_prefix + "_projection")
    event_store = MongoDBEventStore(
        host=host, port=port, db_name=db_name_prefix + "_event_store")
    cmd_handler = MsgCmdHandler(event_store)
    msg_projector = MsgProjector(
        event_store=event_store, msg_projection=msg_projection)
    query_handler = MsgQueryHandler(msg_projection=msg_projection)
    return cmd_handler, msg_projector, msg_projection, query_handler
