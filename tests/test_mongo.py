"""
Tests for MongoDb functionality
"""
from twisted.trial import unittest

testing = ('12345',
           'hello world',
           {'news': ['everyone is saying',
                     'hello again',
                     'howdy'],
            'brews': 'hello beer'})

class TestMongo(unittest.TestCase):
    """ Placeholder until MongoDb is implemented """
    
    def test_mongo(self):
        """ Not needed right now """
        pass
