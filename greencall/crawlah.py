""" Crawlah.py 

Makes API requests in a timely manner then writes out the data

"""
import sys
import json

from twisted.internet import reactor
from twisted.internet.defer import Deferred, DeferredSemaphore
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent

maxRun = 10


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
        print >>sys.stderr, failure

    def stop(self, result):
        reactor.stop()

        
class AgentMaker(PersistData):

    def __init__(self):
        self.data = {}
        self.ro = ResourceOutput()

    def manageAgents(self):

        sites = ["https://www.google.com/", "https://www.yahoo.com/",
                 "https://www.google.com/", "https://www.yahoo.com/"]
                 #"http://www.cnn.com/"]#, "http://www.msnbc.com/"]

        count = 0
        sem = DeferredSemaphore(maxRun)
        
        while count < len(sites):
            agent = Agent(reactor)
            d = sem.run(agent.request, 'GET', sites[count])
            d.addCallback(self.ro.printResource, count)
            d.addErrback(self.ro.printError)
            count += 1

            logging.info("Mischief count: %d" % count)

        self.mischiefManaged(d)

    def mischiefManaged(self, d):
        d.addBoth(self.ro.stop)


        
am = AgentMaker()
am.manageAgents()

reactor.run()



