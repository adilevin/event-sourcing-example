"""
Command handler (CQRS)
"""

from pymongo import MongoClient, ReturnDocument
import uuid

class CommandHandler(object):
    """
        Command handler for CQRS demo
    """

    def __init__(self):
        client = MongoClient()
        self.events_collection = client.cqrs.events
        self.counters_collection = client.cqrs.counters

    def start_new_cart(self, customer_name):
        "start a new cart for customer"
        cart_id = uuid.uuid4().hex
        self._add_event(event_type="new cart started",
                        payload={"customer_name": customer_name, "cart_id": cart_id})
        return cart_id

    def add_item_to_cart(self, cart_id, item_name, quantity):
        "add an item to a cart"
        self._add_event(event_type="add item to cart",
                        payload={"cart_id": cart_id, "item_name": item_name, "quantity": quantity})

    def _get_next_seq_num(self):
        "get next sequence number"
        ret = self.counters_collection.find_one_and_update(
            filter={},
            update={
                "$inc": {"seq_num": 1}},
            return_document=ReturnDocument.AFTER)
        return ret["seq_num"]

    def _add_event(self, event_type, payload):
        "add an event in the event store"
        event = {
            "event_type": event_type,
            "payload": payload,
            "seq_num": self._get_next_seq_num()
        }
        self.events_collection.insert(event)


if __name__ == "__main__":
    CMD_HANDLER = CommandHandler()
    CART_ID = CMD_HANDLER.start_new_cart("adi")
    CMD_HANDLER.add_item_to_cart(CART_ID, "banana", 2)
    CMD_HANDLER.add_item_to_cart(CART_ID, "orange", 1)
    CMD_HANDLER.add_item_to_cart(CART_ID, "orange", 3)
