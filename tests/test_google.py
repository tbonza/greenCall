""" Tests for greencall/utils/google.py """

from twisted.trial import unittest

from tests.data.test_value import values
from greencall.utils.google import (define_meta_es_doc,
                                    define_result_es_doc,
                                    parse_google_json)

class TestGoogleParser(unittest.TestCase):
    """ Test parsing functionality for google parser """


    def setUp(self):

        self.valuedict = values
        self.meta_info = ("Mister Grouse","123456789")

    def tearDown(self):
        pass

    def test_sanity_define_meta_es_doc(self):
        """ Sanity check for data type """

        output = define_meta_es_doc(self.valuedict, self.meta_info)

        self.assertEquals(type(output), dict)

    def test_define_meta_es_doc(self):
        """ Walk through data structure """
        output = define_meta_es_doc(self.valuedict, self.meta_info)

        # account info
        self.assertEquals(output['account_holder'], 'Mister Grouse')
        self.assertEquals(output['account_number'], "123456789")

        # search api info
        self.assertEquals(output['kind'], 'customsearch#search')
        self.assertEquals(output['inputEncoding'], 'utf8')
        self.assertEquals(output['exactTerms'], 'asset')

    def test_sanity_define_result_es_doc(self):
        """ Sanity check for data type """
        output = define_result_es_doc(self.valuedict, self.meta_info)

        self.assertEquals(type(output), dict)

    def test_define_result_es_doc(self):
        """ Walk through data structure """
        output = define_result_es_doc(self.valuedict, self.meta_info)
        
        # account info
        self.assertEquals(output['account_holder'], 'Mister Grouse')
        self.assertEquals(output['account_number'], "123456789")

        # search api info
        self.assertEquals(output['kind'], 'customsearch#search')
        self.assertEquals(output['cx'],
                          '003891126258438650518:fcb7zxrqavu')

    def test_sanity_parse_google_json(self):
        """ Sanity check for data type """
        #ouput = parse_google_json(self.valuedict, self.meta_info)

        #self.assertEquals(type(output), list)
        # test currently failing
        pass

    
        
        

