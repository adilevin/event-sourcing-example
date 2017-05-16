"""
Command handler (CQRS)
"""

from event_store import EventStore
import uuid


class CommandHandler(object):
    """
        Command handler for CQRS demo
    """

    def __init__(self):
        self.event_store = EventStore()

    def start_new_cart(self, customer_name):
        "start a new cart for customer"
        cart_id = uuid.uuid4().hex
        self.event_store.add_event({
            "event_type": "new cart started",
            "customer_name": customer_name,
            "cart_id": cart_id})
        return cart_id

    def add_item_to_cart(self, cart_id, item_name, quantity):
        "add an item to a cart"
        self.event_store.add_event({
            "event_type": "add item to cart",
            "cart_id": cart_id,
            "item_name": item_name,
            "quantity": quantity})


if __name__ == "__main__":
    EventStore.reset()
    CMD_HANDLER = CommandHandler()
    CART_ID = CMD_HANDLER.start_new_cart("adi")
    print CART_ID
    CMD_HANDLER.add_item_to_cart(CART_ID, "banana", 2)
    CMD_HANDLER.add_item_to_cart(CART_ID, "orange", 1)
    CMD_HANDLER.add_item_to_cart(CART_ID, "orange", 3)
