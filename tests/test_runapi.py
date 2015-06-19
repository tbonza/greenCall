""" Tests for runapi.py """
import asyncio
import unittest
import pytest

from greencall.runapi import Runapi

# https://www.google.com/#q=hello+world

class DemoClient(object):

    def __init__(self, query_term):
        self.query_term = query_term

    def demo_client(self):

        query_string = ""
        query_list = self.query_term.split(" ")
        
        count = 0
        while count < len(query_list):

            if count == (len(query_list) - 1):
                query_string += query_list[count]
                
            else:
                query_string += (query_list[count]  + '%20')

                google_stem = 'https://www.google.com/webhp?sourceid=' +\
                              'chrome-instant&ion=1&espv=2&ie=UTF-8#q='
            count += 1
            
        return google_stem + query_string

    
class TestRunapiExists(unittest.TestCase):

    def test_demo_client(self):
        dc = DemoClient("hello world")
        
        query_term = "hello world"
        google_stem = 'https://www.google.com/webhp?sourceid=chrome-' +\
                      'instant&ion=1&espv=2&ie=UTF-8#q='
        equals = google_stem + "hello%20world"
    

        self.assertEquals(dc.demo_client(), equals)
    

    @pytest.mark.asyncio
    def test_runapi_init(self):
        """ Can we init runapi successfully? """
        loop = asyncio.get_event_loop()
        ra = Runapi(client= DemoClient,
                    inputdict={'12345':'hello world'},
                    loop = loop)
        self.assertEquals(type(ra.done),dict)
        loop.stop()

    @pytest.mark.asyncio
    def test_runapi_inputQueries(self):
        """ Can we init runapi successfully? """
        loop = asyncio.get_event_loop()
        ra = Runapi(client= DemoClient,
                    inputdict={'12345':'hello world'},
                    loop = loop)
        self.assertEquals(ra.inputQueries(), {'12345':'hello world'})
        loop.stop()

class TestRunapiMethods(unittest.TestCase):

    def setUp(self):
        #self.loop = asyncio.get_event_loop()
        #ra = Runapi(client= DemoClient,
        #            inputdict={'12345':'hello world'},
        #            loop = self.loop)
        pass

    def tearDown(self):
        #self.loop.stop()
        pass

    def test_inputQueries(self):
        pass
        

        
        
    


