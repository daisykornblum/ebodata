# -*- coding: utf-8 -*-
import pandas as pd
from pymongo import MongoClient

def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]


def _process_configs(configs):
    if not 'db_config' in configs:
        configs['db_config'] = {}
    if not 'query_config' in configs:
        configs['query_config'] = {}

    if not 'host' in configs['db_config']:
        configs['db_config']['host'] = 'localhost'
    if not 'port' in configs['db_config']:
        configs['db_config']['port'] = 27017
    if not 'username' in configs['db_config']:
        configs['db_config']['username'] = None
    if not 'password' in configs['db_config']:
        configs['db_config']['password'] = None
    if not 'db' in configs['db_config']:
        configs['db_config']['db'] = ''

    if not 'collection' in configs['query_config']:
        configs['query_config']['collection'] = None
    if not 'query' in configs['query_config']:
        configs['query_config']['query'] = {}
    if not 'fields' in configs['query_config']:
        configs['query_config']['fields'] = None
    if not 'skip' in configs['query_config']:
        configs['query_config']['skip'] = None
    if not 'limit_to' in configs['query_config']:
        configs['query_config']['limit_to'] = None

    return configs


def _get_cursor(config, all_fields=False):
    """ Helper method gets cursor related to config obj """

    configs = _process_configs(config)
    db_config = configs['db_config']
    query_config = configs['query_config']

    # Connect to MongoDB
    db = _connect_mongo(host=db_config['host'], port=db_config['port'], username=db_config['username'], password=db_config['password'], db=db_config['db'])

    if all_fields:
        cursor = db[query_config['collection']].find(query_config['query'])
    else:
        cursor = db[query_config['collection']].find(query_config['query'], query_config['fields'])

    if query_config['skip'] is not None:
        cursor = cursor.skip(query_config['skip'])

    if query_config['limit_to'] is not None:
        cursor = cursor.limit(query_config['limit_to'])

    return cursor




def get_iterable(config):
    """ Read from Mongo and return iterable cursor """

    return _get_cursor(config)



def save_collection(config, collection_name, data):
    """ Save data to (new ?) collection """

    configs = _process_configs(config)
    db_config = configs['db_config']

    # Connect to MongoDB
    db = _connect_mongo(host=db_config['host'], port=db_config['port'], username=db_config['username'], password=db_config['password'], db=db_config['db'])

    collection = db[collection_name]
    return collection.insert(data)



def update_collection(config, update_query):
    """ Update collection field """

    configs = _process_configs(config)
    db_config = configs['db_config']
    query_config = configs['query_config']

    # Connect to MongoDB
    db = _connect_mongo(host=db_config['host'], port=db_config['port'], username=db_config['username'], password=db_config['password'], db=db_config['db'])

    return db[query_config['collection']].update(query_config['query'], update_query)



def move_collection(config, collection_name):
    """ Move matching documents into new collection so they're not processed again """

    configs = _process_configs(config)
    db_config = configs['db_config']
    query_config = configs['query_config']

    # Connect to MongoDB
    db = _connect_mongo(host=db_config['host'], port=db_config['port'], username=db_config['username'], password=db_config['password'], db=db_config['db'])

    cursor = db[query_config['collection']].find(query_config['query'])

    save_collection(config, collection_name, list(cursor))
    db[query_config['collection']].remove(query_config['query'])



def get_dataframe(config):
    """ Read from Mongo and Store into DataFrame """

    cursor = _get_cursor(config)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    return df