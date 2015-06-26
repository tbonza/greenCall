""" Crawlah.py 

Makes API requests in a timely manner then writes out the data

"""
import sys
import json
import codecs
import logging
from time import gmtime, strftime, sleep, time

import requests
from twisted.internet import reactor
from twisted.web.client import getPage
from twisted.web.error import Error
from twisted.internet.defer import DeferredList, DeferredSemaphore

MAX_RUN = 20 # number of requests 
RATE_LIMIT = 1 # requests per second

class getPages(object):
    """ Return contents from HTTP pages """

    def __init__(self, book, logger=False):
        self.book = book
        self.data = {}

    def listCallback(self, results):
        for isSuccess, result in results:

            if not isSuccess:
                logging.error("Retrieval was unsuccessful")

        for value in self.data.values():
            if value == False:
                logging.debug("Found a dropped connection")
            elif len(value) == 0:
                logging.debug("Found a dropped connection; missing data")

        with open('results.json','w') as outfile:
            json.dump(self.data, outfile)
            outfile.close()

    def pageCallback(self, result, key):
        """ Holds the data while keeping unique_id 

        Args:
          result: body from API request
          key: unique id from input file

        Returns:
          Result; returned as deferred
          self.data; returned to class state
        """
        self.data[key] = result
        
        return result

    def errorHandler(self,result, key):
        "Handles errors during requests """
        logging.error(result)
        self.data[key] = False
        logging.info("Appended False at %d" % len(self.data))

    def finish(self, ign):
        logging.info("reactored stopped")
        reactor.stop()

    def start(self):
        """ get each page """
        deferreds = []
        sem = DeferredSemaphore(MAX_RUN)
        
        for key in self.book.keys():

            sleep(RATE_LIMIT)
            d =  sem.run(getPage, self.book[key])
            d.addCallback(self.pageCallback, key)
            d.addErrback(self.errorHandler, key)
            deferreds.append(d)

        dl = DeferredList(deferreds)
        dl.addCallback(self.listCallback)
        dl.addCallback(self.finish)

