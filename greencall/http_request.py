import asyncio
import aiohttp
import logging

from src.clients import googleSearch
from src.csvclean import goodData
from src.database import asyncMongo

@asyncio.coroutine
def get(*args, **kwargs):
    response = yield from aiohttp.request('GET', *args, **kwargs)
    return (yield from response.read_and_close(decode=True))

@asyncio.coroutine
def api_request(query, client):
    """ Make request to API and write results to Mongo 

    Args:
        query: query from csv file
        client: api client

    Returns:
        True if database write was successful; False otherwise.
    """
    uuid, api_query = query
    url = client(api_query)
    api_result = yield from get(url, compress=True)

    try:
        asyncMongo.write(api_result)
        return True

    except:
        logging.error("Mongo write failed: {0}".format(query))
        return False

def load_file(csv_file):
    """ Load queries 

    Args:
        csv_file: path to csv file with single column of queries

    Returns:
        list of tuples: (unique_id, query_term)

    """
    return goodData(csv_file)

@asyncio.coroutine
def mongo_go(api_result, query):
    try:
        asyncMongo(api_result, query)
        return True
    except:
        uuid, api_query = query
        logging.error("MongoDb write failed: {0} -- {1}".format(uuid, api_query)
        return False

@asyncio.coroutine
def handle_each_item(query, client):
    """ Handle each query asyncronously """
    if not api_request(query, client):
        uuid, api_query = query
        logging.warn("FETCH:: {0} ;;; {1}".format(uuid, api_query)
                          

def run_async_loop(csv_file, client):
    loop = asyncio.get_event_loop()
    f = asyncio.wait(handle_each_item(query, client) \
                     for query in load_file(csv_file))
    loop.run_until_complete(f)                  
    
                      
