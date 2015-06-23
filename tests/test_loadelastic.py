""" Tests for greencall/utils/loadelastic.py """

from twisted.trial import unittest

from greencall.utils.loadelastic import (read_json, convert_content,
                                         load_elastic, map_documents)

class TestElasticBulkLoad(unittest.TestCase):
    """ Test bulk load for elasticsearch python client """


    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_read_json(self):
        """ not really necessary """
        pass

    def test_convert_content(self):
        """ Ensure that a conversion was run smoothly """
        pass

    def test_load_elastic(self):
        """ make sure schema is interpreted correctly, etc. """
        pass

    def test_map_documents(self):
        esformat = {
            "_index": "customsearch",
            "_type": "website",
            "_id": None,
            "_source": ""
        }

        results_dict = {"content": "foo", 
          "results": {"result_one": {"persona": "phone",
                                     "personb":  "phone",
                                     "personc":  "phone"
                                    },
                      "result_two": ["thing1",
                                     "thing2",
                                     "thing3"
                                    ],
                      "result_three": "none"
                     },
          "query": ["Taylor Swift", "Bob Dole", "Rocketman"]
        }

        temp = map_documents(results_dict, esformat)

        self.assertEquals(len(temp), 9)

        

        
