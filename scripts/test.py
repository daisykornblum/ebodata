# -*- coding: utf-8 -*-
from config import DB_CONF
from db import get_dataframe, save_collection
import clean_regexes as regx




def test_db(config, output_collection=None):
    data = get_dataframe(config)
    print 'retrieved %s rows of data' % str(len(data))
    return data



def test_db_batched(config, output_collection=None, batch_size=1000):
    count = 0
    data = []

    config['query_config']['limit_to'] = batch_size

    while (True):
        config['query_config']['skip'] = count * batch_size
        new_data = test_db(config, output_collection)
        data.append(new_data)
        count += 1

    print '(batch) retrieved %s rows of data' % str(len(data))
    return data



config = {
    'db_config':    DB_CONF,
    'query_config': {
        'collection':   'rawdata_20141119',
        'query':        {
            'lang':     'en'
        },
        'fields':       {
            'text':     True,
            'id_str':   True
        },
        'limit_to':     None
    }
}

data = test_db(config, 'marcel_tmp_coll')
data = test_db_batched(config, 'marcel_tmp_batch_coll')






# conn = MongoClient(host='localhost', port=27017)
# db = conn['ebodata']
# collection = db.cleaned_data_20141119

# collection.insert(cleaned_data)