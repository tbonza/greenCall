""" Tests for runapi.py """
import asyncio
import unittest
import pytest

# https://www.google.com/#q=hello+world


class TestRunapiMethods(unittest.TestCase):

    def demo_client(self, query_term):

        query_string = ""
        query_list = query_term.split(" ")
        
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

    def test_demo_client(self):
        query_term = "hello world"
        google_stem = 'https://www.google.com/webhp?sourceid=chrome-' +\
                      'instant&ion=1&espv=2&ie=UTF-8#q='
        equals = google_stem + "hello%20world"
    

        self.assertEquals(self.demo_client(query_term), equals)
    
    
    def test_runapi_init(self):
        """ Can we init runapi successfully? """
        pass


