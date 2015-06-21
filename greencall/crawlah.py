""" Crawlah.py 

Makes API requests in a timely manner then writes out the data

"""
import sys
import json
import codecs
import logging
from time import gmtime, strftime, sleep

from twisted.internet import reactor
from twisted.web.client import getPage
from twisted.web.error import Error
from twisted.internet.defer import DeferredList, DeferredSemaphore

MAX_RUN = 10 # number of requests 
RATE_LIMIT = 1 # requests per second

# consider using an ordered dict for self.data to match keys up with
# results from 'results'.
# There are several ways to make this go faster but for now we just
# want to play nice with the APIs we have available.


class getPages(object):
    """ Return contents from HTTP pages """

    def __init__(self, book, logger=False):
        self.book = book
        self.data = {}
        #util = Utility()
        #if logger:
        #    log = util.enable_log("crawler")

    def listCallback(self, results):
        for isSuccess, result in results:

            if not isSuccess:
                logging.error("Retrieval was unsuccessful")
            #print "Successful: {}".format(isSuccess)
            #print "Output length: {}".format(len(result))

        for value in self.data.values():
            if value == False:
                logging.debug("Found a dropped connection")
            elif len(value) == 0:
                logging.debug("Found a dropped connection; missing data")
            #print "key value: {}".format(key)
            #print "data value len: {}".format(len(self.data[key]))

        with open('results.json','w') as outfile:
            json.dump(self.data, outfile)
            outfile.close()

    def pageCallback(self, result, key):
        ########### I added this, to hold the data:
        self.data[key] = result
        #logging.info("Data appended")
        return result

    def errorHandler(self,result, key):
        # Bad thingy!
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
            #logging.info(key)
            
            d =  sem.run(getPage, self.book[key])
            sleep(RATE_LIMIT)
            d.addCallback(self.pageCallback, key)
            d.addErrback(self.errorHandler, key)
            deferreds.append(d)

        dl = DeferredList(deferreds)
        dl.addCallback(self.listCallback)
        dl.addCallback(self.finish)

