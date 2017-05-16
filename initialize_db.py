
from pymongo import MongoClient
CLIENT = MongoClient()

def clean_db():
    CLIENT.drop_database("cqrs")

def initialize_seqnum():
    CLIENT.cqrs.counters.insert({"seq_num": 0})

#def initialize_event_store():
    #print CLIENT.cqrs.events.count()
    
if __name__=="__main__":
    clean_db()
    initialize_seqnum()
    #initialize_event_store()
