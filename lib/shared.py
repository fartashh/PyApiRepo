import threading
from lib import mongo

db_lock = threading.Lock()
settings = { 'identity': { 'id':100000}}
DBS = {}

DB = mongo.Mongo_DataProvider()
Collections=['logs']

shared_lock = threading.Lock()

def start(db_name = 'API_REPOSITORY'):
    global settings
    DB.connect(db_name, Collections,True );

def stop(db_name = 'pyNote'):
    DB.disconnect()

def attach(db_name, Collections):
    DBS.setdefault(db_name, mongo.Mongo_DataProvider()).connect(db_name, Collections)
    return DBS[db_name]
