""" Crawlah.py 

Makes API requests in a timely manner then writes out the data

"""
import sys
import json
import codecs

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.defer import DeferredSemaphore
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent


class ResourcePrinter(Protocol):
    def __init__(self, finished, count):
        self.finished = finished
        self.count = count
        self.output = open('output/out' + \
                           str(self.count) +'_test.json', 'w')

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

        
class AgentMaker(object):

    def __init__(self, sites):
        self.ro = ResourceOutput()
        self.sites = sites

    def manageAgents(self):

        #sites = ["https://www.google.com/", "https://www.yahoo.com/",
         #        "https://www.google.com/", "https://www.yahoo.com/"]
                 #"http://www.cnn.com/"]#, "http://www.msnbc.com/"]

        count = 0
        #deferreds = []
        sem = DeferredSemaphore(10)
        while count < len(sites):
            agent = Agent(reactor)
            d = sem.run(agent.request('GET', sites[count]))
            d.addCallback(self.ro.printResource, count)
            d.addErrback(self.ro.printError)
            count += 1

            print "\n\nMischief count: %d" % count
            #print "\n\nData_managed: %d" % len(self.data)

        #print "muhData ", str(self.data.keys())
        #print "sanity check: ", self.ro.data[1]
        self.mischiefManaged(d)

    def mischiefManaged(self, d):
        d.addBoth(self.ro.stop)



if __name__ == "__main__":

    with open('greencall/example.json', 'r') as infile:
        wtf = json.load(infile)
    infile.close()

    sites = []
    for site in wtf:
        sites.append(codecs.encode(site))
        
    am = AgentMaker(sites)
    am.manageAgents()
    
    reactor.run()



