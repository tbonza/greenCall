""" Bulk loads Elasticsearch using their client for Python 

After running the example in 'okgo.py' your output will be 
'results.json'. The higher level utility functions provided here will
allow you to bulk load Elasticsearch.
"""
import json

from elasticsearch import Elasticsearch
from elasticsearch import helpers

from greencall.utils.bobby import ApiConversion

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
        
        
def map_documents(results_dict, esformat):
    """ Maps the results dictionary to elasticsearch documents 

    This is currently only tested on results from the Google Custom
    Search API.

    NOTE: leaving out the parent-child relationships for now.

    Args:
        results_dict: Results returned from API, read from JSON
        esformat: document format template
        account_no: (int:account number, str:account holder)

    Returns:
        list of dictionaries in elasticsearch doc format ready for
        upload.

    """
    documents = []
    es_id = 1 # assumes a new index is being created
    count = 0

    a = []
    ac = ApiConversion()
    ac.myfunk(results_dict)
    conversion = ac.documents

    while conversion:

        doc = conversion.pop()
        
        esformat["_id"] = es_id
        esformat["_source"] = { doc.keys()[0] : doc[doc.keys()[0]] }


        documents.append(esformat)

        esformat["_id"] = None
        esformat["_source"] = ""

        es_id += 1
        count += 1

    return documents

        
    

    
    

def load_elastic(resultspath):
    """ Load elasticsearch with output from 'results.json' """
    
    es = Elasticsearch()
    
    results = read_json(resultspath)

    actions = []

    for key in results.keys():

        #results[key] = convert_content(results[key])

        if results[key] == False:
            results[key] = ""

        action = {
            "_index": "google-custom-search",
            "_type": 'search',
            "_id": key,
            "_source": results[key]
            }
        
        actions.append(action)

    # load elasticsearch in bulk
    helpers.bulk(es, actions)


