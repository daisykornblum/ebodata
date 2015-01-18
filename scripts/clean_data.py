# -*- coding: utf-8 -*-
from config import DB_CONF
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



def clean_data_batched(config, output_collection=None, batch_size=1000):
    count = 0
    data = []

    config['query_config']['limit_to'] = batch_size

    while (True):
        config['query_config']['skip'] = count * batch_size
        batch_data = clean_data(config, output_collection)
        count += 1

        if output_collection is None:
            data.append(batch_data)

    return data