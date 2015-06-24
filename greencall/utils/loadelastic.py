""" Bulk loads Elasticsearch using their client for Python 

After running the example in 'okgo.py' your output will be 
'results.json'. The higher level utility functions provided here will
allow you to bulk load Elasticsearch.
"""
import json
import logging

from elasticsearch import Elasticsearch
from elasticsearch import helpers

from greencall.utils.bobby import ApiConversion
from greencall.csvclean.inputCsv import read_csv

def read_json(resultspath):

    with open(resultspath, 'r') as injson:
        results = json.load(injson)
        injson.close()

    return results

def convert_content(value):
    """ Convert dictionary values to json as well """
    return json.loads(value)

class ElasticsearchDocument(object):

    def __init__(self, es_id, source, account_number,
                 account_holder):
        
        self.es_id = es_id
        self.source = source
        self.account_number = account_number
        self.account_holder = account_holder

    def esFormatGetter(self, esformat):

        esformat["_id"] = self.es_id
        esformat["_source"] = self.source
        esformat["_source"]["account_number"] = self.account_number
        esformat["_source"]["account_holder"] = self.account_holder

        return esformat
        
        
def map_documents(results_dict, esformat, account, es_id):
    """ Maps the results dictionary to elasticsearch documents 

    This is currently only tested on results from the Google Custom
    Search API.

    NOTE: leaving out the parent-child relationships for now.

    Args:
        results_dict: Results returned from API, read from JSON
        esformat: document format template
        account: (int:account number, str:account holder)

    Returns:
        list of dictionaries in elasticsearch doc format ready for
        upload.

    """
    documents = []

    a = []
    ac = ApiConversion()
    ac.myfunk(results_dict)
    conversion = ac.documents

    while conversion:

        _esformat = esformat.copy()

        doc = conversion.pop()

        account_number, account_holder = account
        ed = ElasticsearchDocument(es_id = es_id,
                                   source = { doc.keys()[0] : \
                                              doc[doc.keys()[0]] },
                                   account_number = account_number,
                                   account_holder = account_holder)

        documents.append(ed.esFormatGetter(_esformat))

        es_id += 1

    return documents

#def merge_csv_input(filepath):
#    """ Merge csv input file to get account information, returns dict """
#    accountdict = read_csv(filepath)   

def prepare_all_documents(jsondict, esformat, accountdict):
    """ Prepare results returned for each account as bulk upload 

    Args:
        jsondict: results returned from API
        esformat: elasticsearch document format
        accountdict: read_csv(filepath) from csvclean utils
        
    Returns:
        List, ready for bulk upload into elasticsearch

    """
    actions = []
    es_id = 1 # assumes new index

    for key in jsondict.keys():

        if key not in accountdict:
            logging.error("Account {} missing from CSV input file."\
                          .format(key))
            logging.info("Documents associated with {} will not be " +\
                         "loaded into elasticsearch".format(key))

        else:
            actions += map_documents(results_dict = jsondict[key],
                                     esformat = esformat,
                                     account = (key,accountdict[key]),
                                     es_id = es_id)

        es_id += 1
    
    return actions


def load_elastic(resultspath, esformat, accountdict):
    """ Load elasticsearch with output from 'results.json' """
    
    es = Elasticsearch()
    
    results = read_json(resultspath)

    actions = prepare_all_documents(results, esformat, accountdict)

    # load elasticsearch in bulk
    helpers.bulk(es, actions)


