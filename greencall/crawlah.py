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
#         sleep(RATE_LIMIT)

# consider using an ordered dict for self.data to match keys up with
# results from 'results'.
# There are several ways to make this go faster but for now we just
# want to play nice with the APIs we have available.

class RequestHandler(object):
    """ Sets rate limit and reschedules dropped requests """

    def __init__(self, rate, per):

        self.rate = rate # unit: messages
        self.per = per # unit: seconds
        self.allowance = rate # unit: messages
        self.last_check  = now()

    def rate_limit_timer(self, last_check, fire_at_will):
        """ This needs a test written """

        current = time()
        time_passed = current - last_check
        last_check = current

        self.allowance += time_passed * (self.rate/self.per)

        if (self.allowance > self.rate):
            self.allowance = self.rate

        if (self.allowance < 1.0):
            pass
        else:
            self.allowance -= 1.0
            return fire_at_will = True


    def rate_little_hammer(self, r):
        # also needs a test written
        """ Request throttle for Requests library

        Args:
            r: request result from requests.get()
        Returns:
            True when it's ok to make a new request
        """
        fire_at_will = False
        last_check = time()
        
        while not fire_at_will:

            if r.status_code == 200:
                self.rate_limit_timer(last_check, fire_at_will)
                
            elif r.status_code == 400:
                pass

            else:
                pass
                
        
        


class getPages(object):
    """ Return contents from HTTP pages """

    def __init__(self, book, logger=False):
        self.book = book
        self.data = {}
        #util = Utility()
        #if logger:
        #    log = util.enable_log("crawler")

    def littleHammer(self):
        """ Requests should equal 1 per second """

        for key in self.book.keys():
            pass

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

            sleep(RATE_LIMIT)
            d =  sem.run(getPage, self.book[key])
            d.addCallback(self.pageCallback, key)
            d.addErrback(self.errorHandler, key)
            deferreds.append(d)

        dl = DeferredList(deferreds)
        dl.addCallback(self.listCallback)
        dl.addCallback(self.finish)

