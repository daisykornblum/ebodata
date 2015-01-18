# -*- coding: utf-8 -*-
import datetime

from log import log
from config import DB_CONF
from db import get_dataframe, move_collection
import clean_regexes as regx
from clean_data import clean_data, clean_data_batched
from dedupe_data import dedupe_data, dedupe_data_batched


config = {
    'db_config':    get_default_db_config(),
    'query_config': {
        'collection':   'rawdata_20141119',
        'query':        {
            'lang':     'en'
        },
        'fields':       {
            'text':     True,
            'id_str':   True
        },
        'skip':         None
        'limit_to':     None
    }
}
date_str = str(datetime.date.today())
dupe_ref_collection = 'duplicate_strings_ref'

log('Starting processing')

# First let's move the matching documents to a new collection so we don't process them twice
new_raw_collection = 'rawdata_%s' % date_str
move_collection(config, new_raw_collection)
config['query_config']['collection'] = new_raw_collection
log('Moved matching rawdata from %s to %s' % ('rawdata_20141119', new_raw_collection))

# Now let's clean the data
cleaned_collection = 'cleaned_%s' % date_str
clean_data_batched(config, cleaned_collection)
config['query_config']['collection'] = cleaned_collection
log('Cleaned data and saved to %s' % cleaned_collection)

# Time to de-dupe
deduped_collection = 'cleaned_%s' % date_str
dedupe_data_batched(config, dupe_ref_collection, deduped_collection)
config['query_config']['collection'] = deduped_collection
log('Cleaned data and saved to %s' % deduped_collection)