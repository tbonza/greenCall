""" Tests for Google Custom Search API """

from twisted.trial import unittest
from greencall.clients.googleSearch import GoogleCustomSearch

class TestGoogleCustomSearch(unittest.TestCase):
    """ Let's see if the API is put together correctly """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_class_instantiation(self):

        # http://stackoverflow.com/questions/647900
        # test runner will catch all exceptions not explictly caught
        
        gcs = GoogleCustomSearch(version = '1',
                filtah = '1',
                cx = '003891126258438650518:fcb7zxrqavu',
                lr = 'lang_en',
                exactTerms = 'asset',
                q='Taylor Swift',
                dateRestrict = "'2012'",
                secretKey = 'mcLovin_8_his_fake_id',
                uniqueId = 12345)

        self.assertTrue(True)

    def test_variables_converted_check_params(self):

        gcs = GoogleCustomSearch(version = '1',
                filtah = '1',
                cx = '003891126258438650518:fcb7zxrqavu',
                lr = 'lang_en',
                exactTerms = 'asset',
                q='Taylor Swift',
                dateRestrict = "'2012'",
                secretKey = 'mcLovin_8_his_fake_id',
                uniqueId = 12345)

        gcs.checkParams()
        
        self.assertTrue(':' not in gcs.cx)
        self.assertTrue(' ' not in gcs.q)

    def test_correct_request_configured(self):

        gcs = GoogleCustomSearch(version = '1',
                filtah = '1',
                cx = '003891126258438650518:fcb7zxrqavu',
                lr = 'lang_en',
                exactTerms = 'asset',
                q='Taylor Swift',
                dateRestrict = "'2012'",
                secretKey = 'mcLovin_8_his_fake_id',
                uniqueId = 12345)

        self.assertEquals(gcs.queryString(),
                          "https://www.googleapis.com/customsearch/" +\
                          "v1?filter=1&cx=003891126258438650518%3Af" +\
                          "cb7zxrqavu&lr=lang_en&exactTerms=asset&q" +\
                          "=Taylor+Swift&dateRestrict='2012'&key=mc" +\
                          "Lovin_8_his_fake_id")
        

        

        
    
    
