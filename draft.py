"""
Test pymong
"""

from pymongo import MongoClient, ReturnDocument

client = MongoClient()
db = client.test

def get_balance(customer_name):
    entries = db.events.find({"customer":customer_name},{"_id":0,"amount":1})
    return sum([item["amount"] for item in entries])

def get_next_seq_num():
   ret = db.counters.find_one_and_update(filter={},update={ "$inc": {"seq_num": 1 }},return_document=ReturnDocument.AFTER)
   return ret["seq_num"]

print get_balance("adi")
print get_balance("bella")

for i in range(10):
    print get_next_seq_num()
