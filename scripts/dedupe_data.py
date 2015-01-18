# -*- coding: utf-8 -*-
from config import DB_CONF
from db import get_dataframe, save_collection



def _is_dupe(row, compdata_collection):
    if compdata_collection is None:
        tmp_conf = config
        tmp_conf['query_config']['collection'] = compdata_collection
        tmp_conf['query_config']['limit_to'] = None
        tmp_conf['query_config']['skip'] = None
        compdata = list(get_iterable(tmp_conf))

    compText = row[1][1][20:-20]
    if np.any([compText in s for s in compdata]):
        compdata.append(row[1][1])
        return True
    return False


def dedupe_data(config, compdata_collection=None, output_collection=None):
    data = get_dataframe(config)
    deduped_data = []

    for row in data.iterrows():
        if not _is_dupe(row, compdata_collection):
            deduped_data.append(row)

    if output_collection is not None:
        save_collection(config, output_collection, data)

    return data



def dedupe_data_batched(config, compdata_collection=None, output_collection=None, batch_size=1000):
    count = 0
    data = []

    config['query_config']['limit_to'] = batch_size

    while (True):
        config['query_config']['skip'] = count * batch_size
        batch_data = dedupe_data(config, compdata_collection, output_collection)
        count += 1

        if output_collection is None:
            data.append(batch_data)

    return data