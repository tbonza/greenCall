""" runapi.py

Makes asyncronous calls to API and writes results to MongoDb

"""
import asyncio
import aiohttp
import logging
import signal

#from src.clients import googleSearch
from src.csvclean import goodData
from src.database import asyncMongo

class Runapi(object):
    """ Make async requests to one API """

    def __init__(self, maxtasks=100):
        self.client = client
        self.csvfile = csvfile
        self.loop = loop
        self.todo = set()
        self.busy = set()
        self.done = {}
        self.tasks = set()
        self.sem = asyncio.Semaphore(maxtasks)

        # connector stores cookies between requests and uses connection pool
        self.connector = aiohttp.TCPConnector(share_cookies=True, loop=loop)

    @asyncio.coroutine
    def run(self):
        asyncio.Task() # set initial work
        yield from asyncio.sleep(1)
        while self.busy:
            yield from asyncio.sleep(1)

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
        ammo = goodData(csv_file)
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
                # good spot to write to database
                pass

            resp.close()
            self.done[uuid] = True

        self.busy.remove(uuid)

def apiFetcher(client, csvfile, loglocation='runapi'):
    enable_log(loglocation)
    loop = asyncio.get_event_loop()

    c = Runapi(client, csvfile, loop)
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
        

                     
        
                

