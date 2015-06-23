""" Bulk loads Elasticsearch using their client for Python 

After running the example in 'okgo.py' your output will be 
'results.json'. The higher level utility functions provided here will
allow you to bulk load Elasticsearch.
"""
import json

from elasticsearch import Elasticsearch
from elasticsearch import helpers

def read_json(resultspath):

    with open(resultspath, 'r') as injson:
        results = json.load(injson)
        injson.close()

    return results

def convert_content(value):
    """ Convert dictionary values to json as well """
    return json.loads(value)

def map_documents(results_dict):
    """ Maps the results dictionary to elasticsearch documents """
    documents = []

    
    

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


