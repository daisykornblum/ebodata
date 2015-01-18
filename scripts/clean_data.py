import DB_CONF from config
from db import get_dataframe, save_collection
import clean_regexes as regx




def clean_data(config, output_collection=None):
    rawdata = get_dataframe(config)
    data = []

    for row in rawdata.iterrows():
        data_row = {}
        data_row['id_str'] = row[1][1]
        data_row['text'] = row[1][2]

        ### Regular expression removal from text (email,usernames,RT,URLs,emos)
        data_row['text_no_email'] = email_addresses_regex.sub('', data_row['text'])
        data_row['text_no_username'] = username_regex.sub('', data_row['text_no_email'])
        data_row['text_no_rt'] = rt_regex.sub('', data_row['text_no_username'])
        data_row['text_no_url'] = embedded_url_regex.sub('', data_row['text_no_rt'])
        data_row['text_no_emo'] = RE_EMOJI.sub('', data_row['text_no_url'])
        data_row['text_no_emoz'] = RE_EMOTICONS.sub('', data_row['text_no_emo'])

        data_row['cleaned_text'] = data_row['text_no_emoz']

        data.append(data_row)

    if output_collection is not None:
        save_collection(config, output_collection, data)

    return data



def clean_data_batched(config, batch_size=1000, output_collection=None):
    count = 0
    data = []

    config['query_config']['limit_to'] = batch_size

    while (True):
        config['query_config']['skip'] = count * batch_size
        data.append(clean_data(config, output_collection))
        count += 1

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

data = clean_data(config)

print 'cleaned %s rows of data' % str(len(data))




# conn = MongoClient(host='localhost', port=27017)
# db = conn['ebodata']
# collection = db.cleaned_data_20141119

# collection.insert(cleaned_data)