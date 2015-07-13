""" Document parser for Google Custom Search API

I was hoping to have more general API to Elasticsearch document 
converter  but it looks like this will have to be API specific. Make
sure the hyperlinks are formatted as 'RAW'.

Given:

esformat = {
            "_index": "ipythonsearch",
            "_type": "website",
            "_id": None,
            "_source": ""
        }

Create:

<meta info>
{ 'account_holder' : 'Mister Grouse',
  'account_number' : '11111417',
  'kind': 'customsearch#search',
  'template' : 'some link about the custom search engine config',
  'title' : 'Google Custom Search - Mister Grouse',
  'totalResults' : '0',
  'searchTerms': 'Mister Grouse',
  'count': 10,
  'language': 'lang_en',
  'inputEncoding': 'utf8',
  'outputEncoding': 'utf8',
  'safe': 'off',
  'cx': '003891126258438650518:fcb7zxrqavu',
  'filter': '1',
  'exactTerms': 'asset',
  'dateRestrict': "'2012'",
  'searchTime': 0.161848,
  'formattedSearchTime': "0.16",
  'totalResults': '0',
  'formattedTotalResults': '0'
}
  
If at least 1 search result exists then a seperate ES document will
be created for each result. That ES document will be of the form:

<result info>
{ 'account_holder' : 'Mister Grouse',
  'account_number' : '11111417',
  'kind': 'customsearch#search',
  'cx': '003891126258438650518:fcb7zxrqavu',
  'title': 'Mister Grouse eats some cheese',
  'link': 'http://www.yellowpages.com/rio-rancho-nm/mister-grouse',
  'snippet': 'A snippet from the webpage about Mister Grouse'
}

Returns:
  List of dictionaries, containing es document formats with payloads
  of meta or search result information.

"""
import logging

from greencall.loadelastic import read_json


def define_meta_es_doc(pydict, meta_info):
    meta_es_doc = {}

    holder, number = meta_info
    
    meta_es_doc['account_holder'] = holder
    meta_es_doc['account_number'] = number
    meta_es_doc['kind'] = None
    meta_es_doc['template'] = None # mark as raw
    meta_es_doc['title'] = None
    meta_es_doc['totalResults'] = None
    meta_es_doc['searchTerms'] = None
    meta_es_doc['count'] = None
    meta_es_doc['language'] = None
    meta_es_doc['inputEncoding'] = None
    meta_es_doc['outputEncoding'] = None
    meta_es_doc['safe'] = None
    meta_es_doc['cx'] = None
    meta_es_doc['filter'] = None
    meta_es_doc['exactTerms'] = None
    meta_es_doc['dateRestrict'] = None
    meta_es_doc['searchTime'] = None
    meta_es_doc['formattedSearchTime'] = None
    meta_es_doc['totalResults'] = None
    meta_es_doc['formattedTotalResults'] = None

    return meta_es_doc

def define_result_es_doc(pydict, meta_info):
    res_es_doc = {}

    holder, number = meta_info

    res_es_doc['account_holder'] = holder
    res_es_doc['account_number'] = number
    res_es_doc['kind'] = None
    res_es_doc['cx'] = None
    res_es_doc['title'] = None
    res_es_doc['link'] = None
    res_es_doc['snippet'] = None

    return res_es_doc

def parse_google_json(pydict, meta_info):

    parsed = []

    if True:
        parsed.append(define_meta_es_doc(pydict, meta_info))

    elif False:
        for result in results:
            parsed.append(define_result_es_doc(pydict, meta_info))

    else:
        pass

    return parsed

    


def create_google_es_docs(resultsdict, accountdict):
    """
    Args:
        resultsdict: read_json(jsonpath)
        accountdict: read_csv(inputpath)
    """
    esdocs = []

    for key in resultsdict.keys():

        if key in accountdict:

            meta_info = accountdict[key]
            
            esdocs += parse_google_json(pydict, meta_info)

        
        else:
            logging.warning("key missing from parsed results: {}"\
                            .format(key))

    return esdocs

            
            

        

    

   


