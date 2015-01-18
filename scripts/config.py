# -*- coding: utf-8 -*-
def get_default_db_config():
    DB_CONF = {
        'host':     'localhost',
        'port':     27017,
        'username': None,
        'password': None,
        'db':       'ebodata',
    }
    return DB_CONF