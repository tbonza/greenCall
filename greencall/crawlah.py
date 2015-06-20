""" Crawlah.py 

Makes API requests in a timely manner then writes out the data

"""
import json
import codecs
import logging
from time import gmtime, strftime

from twisted.internet import defer, reactor
from twisted.web.client import getPage

#from greencall.utils import utilityBelt

def enable_log(log_name):
    """ Enable logs written to file """
    log_name = strftime("%d_%b_%Y_%H%M%S", gmtime()) + log_name
    logging.basicConfig(filename= log_name + ".log",
                        level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s' +\
                        ' %(message)s')

 
maxRun = 10
 
#urls = [
#  'http://twistedmatrix.com',
#  'http://yahoo.com',
#  'http://www.google.com',
#  ]

with open('examples/testing.json', 'r') as infile:
    wtf = json.load(infile)
infile.close()

urls = []
for site in wtf:
    urls.append(codecs.encode(site))

 
def listCallback(results):
    with open('output.json','w') as outfile:
        count = 0
        ok = {}
        logging.info('results available')
        for isSuccess, result in results:
            ok[count] = result

        json.dump(ok, outfile)
            
def finish(ign):
    logging.info('process complete')
    reactor.stop()
 
def test():
  deferreds = []
  sem = defer.DeferredSemaphore(maxRun)
  count = 0
  for url in urls:
    d = sem.run(getPage, url)
    deferreds.append(d)
    print "Number queries: %d" % count
    count += 1
  dl = defer.DeferredList(deferreds)
  logging.info('deferreds added to list')
  dl.addCallback(listCallback)
  logging.info('list callback completed')
  dl.addCallback(finish)
  logging.info('finished callbacks')



enable_log('crawlah')
logging.info('crawlah started')
test()
reactor.run()

