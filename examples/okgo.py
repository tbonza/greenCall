import json
import codecs
import logging

from twisted.internet import reactor

#from greencall.csvclean import goodData
#from greencall.database import asyncMongo
#from greencall.clients import googleSearch
from greencall.crawlah import getPages
from greencall.utils.utilityBelt import enable_log


if __name__ == '__main__':
    
    enable_log('crawlah')

    with open('examples/testkitten.json', 'r') as infile:
        testkitten = json.load(infile)

    for key in testkitten.keys():
        testkitten[key] = codecs.encode(testkitten[key])
    

    logging.info("crawlah STARTED")
    gp = getPages(testkitten)
    gp.start()
    reactor.run()
