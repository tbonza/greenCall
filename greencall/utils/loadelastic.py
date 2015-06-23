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

def map_documents(results_dict, esformat):
    """ Maps the results dictionary to elasticsearch documents 

    This is currently only tested on results from the Google Custom
    Search API.

    NOTE: leaving out the parent-child relationships for now.

    Args:
        results_dict: Results returned from API, read from JSON
        esformat: document format template

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

    #while conversion:
        
        #doc = conversion.pop(conversion.keys()[count], None)

        #esformat["_id"] = es_id
        #esformat["_source"] = {conversion.keys()[count] : doc }

        #documents.append(esformat)

        #esformat["_id"] = None
        #esformat["_source"] = ""

        #count += 1

    return conversion

        
    

    
    

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


