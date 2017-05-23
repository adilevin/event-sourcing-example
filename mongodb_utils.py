from pymongo import MongoClient

def drop_db(host, port, db_name):
    client = MongoClient(host=host, port=port)
    client.drop_database(db_name)

def drop_dbs_by_prefix(host, port, db_name_prefix):
    client = MongoClient(host=host, port=port)
    db_names = client.database_names()
    for db_name in db_names:
        if db_name.startswith(db_name_prefix):
            client.drop_database(db_name)
            