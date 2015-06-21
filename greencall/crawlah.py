""" Crawlah.py 

Makes API requests in a timely manner then writes out the data

"""
import sys
import json
import codecs
import logging
from time import gmtime, strftime

from twisted.internet import reactor
from twisted.web.client import getPage
from twisted.web.error import Error
from twisted.internet.defer import DeferredList, DeferredSemaphore

maxRun = 10
# consider using an ordered dict for self.data; for now let's just
# bang on it & see if things break

def enable_log(log_name):
    """ Enable logs written to file """
    log_name = strftime("%d_%b_%Y_%H%M%S", gmtime()) + log_name
    logging.basicConfig(filename= log_name + ".log",
                        level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s' +\
                        ' %(message)s')

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
            print "Successful: {}".format(isSuccess)
            print "Output length: {}".format(len(result))

        for key in self.data.keys():
            print "key value: {}".format(key)
            print "data value len: {}".format(len(self.data[key]))

    def pageCallback(self, result, key):
        ########### I added this, to hold the data:
        self.data[key] = result
        logging.info("Data appended")
        return result

    def errorHandler(self,result, key):
        # Bad thingy!
        logging.error(result)
        self.data[key] = False
        logging.info("Appended False at %d" % len(self.data))

    def finish(self, ign):
        reactor.stop()

    def start(self):
        """ get each page """
        deferreds = []
        sem = DeferredSemaphore(maxRun)
        
        for key in self.book.keys():
            logging.info(key)
            
            d =  sem.run(getPage, self.book[key])
            d.addCallback(self.pageCallback, key)
            d.addErrback(self.errorHandler, key)
            deferreds.append(d)

        dl = DeferredList(deferreds)
        dl.addCallback(self.listCallback)
        dl.addCallback(self.finish)

            
        
    
    
enable_log('crawlah')
gp = getPages({'12345':'http://tbonza.github.io/',
               '45678':'https://twitter.com/'})
gp.start()
reactor.run()
