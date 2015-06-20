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

class ManageData(object):
    """ Manages data retrieved from the ResourcePrinter protocol """

    def __init__(self):
        self.request_data = {}
        self.myfile = open('myfile.json','w')

    def write_file(self, key, value):
        self.myfile.write(value)
        
    def write(self, key, value):
        self.request_data[key] = value

    def read(self):
        return self.request_data


class ResourcePrinter(Protocol, ManageData):
    
    def __init__(self, finished, key):
        self.finished = finished
        self.key = key
    
    def dataReceived(self, data):

        if self.finished:
            self.write_file(key = self.key,
                            value = data)
        
        return data

    def connectionLost(self, reason):
        self.finished.callback(None)

        
class ResourceOutput(ManageData):
    
    def printResource(self, response, key):
        finished = Deferred()

        response.deliverBody(ResourcePrinter(finished, key))

        return finished

    def printError(self, failure):
        print >>sys.stderr, failure

    def outputData(self, response):
        print self.read()
        
class AgentMaker(object):

    def __init__(self):
        self.data = {}
        self.ro = ResourceOutput()

    def manageAgents(self):

        sites = ["https://github.com/","https://twitter.com/"]

        count = 0
        sem = DeferredSemaphore(maxRun)
  
        while count < len(sites):
            agent = Agent(reactor)
            
            d = sem.run(agent.request, 'GET', sites[count])
            d.addCallback(self.ro.printResource, count)
            d.addErrback(self.ro.printError)
            #d.addCallback(self.ro.outputData)
                        
            count += 1

            print "Mischief count: %d" % count

        d.addBoth(self.mischiefManaged)
        
    def mischiefManaged(self, result):
        reactor.stop()



enable_log('crawlah')
logging.info('crawlah started')

am = AgentMaker()
am.manageAgents()
reactor.run()
