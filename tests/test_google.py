""" Tests for greencall/utils/google.py """

from twisted.trial import unittest

from tests.data.test_value import values
from greencall.utils.google import (define_meta_es_doc,
                                    define_result_es_doc)

class TestGoogleParser(unittest.TestCase):
    """ Test parsing functionality for google parser """


    def setUp(self):

        self.valuedict = values
        self.meta_info = ("Mister Grouse","123456789")

    def tearDown(self):
        pass

    def test_define_meta_es_doc(self):

        output = define_meta_es_doc(self.valuedict, self.meta_info)

        self.assertEquals(type(output), dict)
