""" runapi.py

Makes asyncronous calls to an API client

"""
import asyncio
import aiohttp
import logging
import signal
import json

from greencall.utils.utilityBelt import enable_log

class Runapi(object):
    """ Make async requests to one API 
    
    Args:
        inputdict: { unique id : query term }
        loop: asyncio oject, from Python3 library
        client: function, API client
    """

    def __init__(self, client, inputdict, loop, maxtasks=100):
        self.client = client
        self.inputdict = inputdict
        self.loop = loop
   
        # connector stores cookies between requests using connection pool
        self.connector = aiohttp.TCPConnector(share_cookies=True,
                                              loop=loop)

    def inputQueries(self):
        """ Input for API crawler

        Args:
            inputdict: key   - str, unique id associated with each query
                       value - str, query term to be fed to API

        Returns:
            dict, will return inputdict if formatted correctly but raise
            error otherwise.
        """
        return self.inputdict

    def outputResult(self, unique_id, query_term, result):
        """ Outputs the result for one (1) query as a json object 

        Args:
            unique_id: str, unique id associated with the query
            query_term: str, the actual term that was queried
            result: dict, output from api request

        Returns:
            json list, 
               (unique id, query term, 
                output from API request as json dict)
        """
        return json.dumps((unique_id, query_term, result))
        

    @asyncio.coroutine
    def run(self):
        asyncio.Task(self.addRequests()) # set initial work
        self.connector.close()
        self.loop.stop()

    @asyncio.coroutine
    def addRequests(self):
        """ Load queries 

        Args:
            csv_file: path to csv file with single column of queries

        Returns:
            list of tuples: (unique_id, query_term)

        """
        ammo = self.inputQueries()
        for uuid in ammo.keys():
            if (uuid not in self.busy and
                uuid not in self.done and
                uuid not in self.todo):
                self.todo.add(uuid)
                yield from self.sem.acquire()
                logging.info("Processing UUID: {0}".format(uuid))
                task = asyncio.Task(self.process(uuid, ammo))
                task.add_done_callback(lambda t: self.sem.release())
                task.add_done_callback(self.tasks.remove)
                self.tasks.add(task)

    @asyncio.coroutine
    def process(self, uuid, ammo):
        """ Processes a specific query

        Args:
            ammo: dict of all terms; single term to be processed 
        """
        logging.info('processing query term: {0}'.format(query_term))

        self.todo.remove(uuid)
        self.busy.add(uuid)

        url = self.client(ammo[uuid])
        try:
            resp = yield from aiohttp.request(
                'GET', url, connector=self.connector)
        except Exception as exc:
            logging.error('UUID: {0} ;; error with API REQUEST: {1}'\
                          .format(uuid, url))
            self.done[uuid] = False
        else:
            if (resp.status == 200):
                self.outputResult(unique_id = uuid,
                                  query_term = ammo[uuid],
                                  result = resp) #should be a dict

            resp.close()
            self.done[uuid] = True

        self.busy.remove(uuid)

def apiFetcher(client, inputdict, loglocation='runapi'):
    enable_log(loglocation)
    loop = asyncio.get_event_loop()

    c = Runapi(client, inputdict, loop)
    asyncio.Task(c.run())

    try:
        loop.add_signal_handler(signal.SIGINT, loop.stop)
        
    except RuntimeError:
        logging.error("RuntimeError")

    loop.run_forever()
    logging.info('todo: {0}'.format(len(c.todo)))
    logging.info('busy: {0}'.format(len(c.busy)))
    logging.info('done: {0}'.format(len(c.done)))
    logging.info('tasks: {0}'.format(len(c.tasks)))
        

                     
        
                

