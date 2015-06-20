""" Crawlah.py 

Makes API requests in a timely manner then writes out the data

"""
import sys
import json
import codecs
import logging
from time import gmtime, strftime

from twisted.internet import reactor
from twisted.internet.defer import Deferred, DeferredSemaphore
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent

maxRun = 10

def enable_log(log_name):
    """ Enable logs written to file """
    log_name = strftime("%d_%b_%Y_%H%M%S", gmtime()) + log_name
    logging.basicConfig(filename= log_name + ".log",
                        level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s' +\
                        ' %(message)s')

class ResourcePrinter(Protocol):
    def __init__(self, finished, count):
        self.finished = finished
        self.count = count
        self.output = open('output/out' + str(self.count) +'_test.json', 'w')

    def dataReceived(self, data):

        if self.finished:
            self.output.write(data)
        
        return data

    def connectionLost(self, reason):
        self.finished.callback(None)

        
class ResourceOutput(object):
    
    def printResource(self, response, count):
        finished = Deferred()

        response.deliverBody(ResourcePrinter(finished, count))

        return finished

    def printError(self, failure):
        #logging.error(sys.stderr, failure)
        logging.error('some print error went wrong')
        print >>sys.stderr, failure

    def stop(self, result):
        logging.info('reactor stopped')
        reactor.stop()

        
class AgentMaker(object):

    def __init__(self, sites):
        self.ro = ResourceOutput()
        self.sites = sites

    def manageAgents(self):

        count = 0
        sem = DeferredSemaphore(maxRun)

        logging.info('manageAgents loop START')
        while count < len(self.sites):
            agent = Agent(reactor)
            d = sem.run(agent.request, 'GET', self.sites[count])
            d.addCallback(self.ro.printResource, count)
            d.addErrback(self.ro.printError)
            count += 1

        logging.info('manageAgents loop END')
        self.mischiefManaged(d)

    def mischiefManaged(self, d):
        d.addBoth(self.ro.stop)


enable_log('crawlah')

with open('examples/test.json','r') as infile:
    sites = json.load(infile)
    infile.close()

count = 0
ascii_sites = []
for site in sites:
    clean = codecs.encode(site, 'ascii')
    ascii_sites.append(clean)

am = AgentMaker(ascii_sites)
am.manageAgents()

reactor.run()



