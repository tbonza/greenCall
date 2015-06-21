"""
API client for Google Custom Search

Build your custom search engine using 'Custom Search' by Google. It 
allows you to specify which types of results should appear by only 
searching results from specific websites or all websites. Advanced 
features allow you to specific which types of entities (Person, Place,
etc.), relationships between entities and actions should be returned by
the search results.

Official Documentation:
https://developers.google.com/custom-search/docs/overview

Params (used):
  'v1'          : API version
  'cx'          : The custom search engine ID to scope this search query
  'lr'          : language in english
  'filter'      : removes duplicates if 1; 0 otherwise
  'exactTerms'  : result must contain term(s)
  'q'           : query
  'dateRestrict': Specifies all search results are from a time period

Params (helpful but not used):
  'gl'          : Geolocation of end user. (string)
   
"""
import logging

class GoogleCustomSearch(object):
    """ All params in __init__ are mandatory for now """

    def __init__(self,
                 version = False,
                 cx = False,
                 lr = False,
                 filtah = False,
                 exactTerms = False,
                 q = False,
                 dateRestrict = False,
                 secretKey = False,
                 uniqueId = False):

        
        self.version = version
        self.cx = cx
        self.lr = lr
        self.filtah = filtah
        self.exactTerms = exactTerms
        self.q = q
        self.dateRestrict = dateRestrict
        self.secretKey = secretKey
        self.uniqueId = uniqueId
        self.queryStem = "https://www.googleapis.com/customsearch/"    

    def checkParams(self):
        """ Check params to see what will be included in the request """

        required = set([self.version, self.cx, self.q, self.secretKey,
                        self.uniqueId, self.filtah])

        if False in required:
            raise NameError('Required parameter is missing')

        # custom search engine id 
        if ':' in self.cx:
            try:
                self.cx = self.cx.replace(':','%3A')
            except:
                raise NameError("Change colon to a '%3A' sign for cx")

        # query string
        if ' ' in self.q:
            self.q = self.q.replace(' ','+')

        return None
                
    def queryString(self):
        """ GET - configure string for search query """
        make_query = ""
        check_params = self.checkParams()

        try:

            ## Required Parameters

            # add query stem
            make_query += self.queryStem

            # add version
            make_query += 'v' + self.version + '?'

            # add filter for duplicates
            make_query += 'filter=' + self.filtah + '&'
            
            # add custom search engine id (yours)
            make_query += 'cx=' + self.cx + '&'

            # add langague specification
            make_query += 'lr=' + self.lr + '&'

            # add exact terms
            make_query += 'exactTerms=' + self.exactTerms + '&'

            # add actual query string
            make_query += 'q=' + self.q + '&'

            # add date restrictions
            make_query += 'dateRestrict=' + self.dateRestrict + '&'

            # add secret key (get it from Google Developer dashboard)
            make_query += 'key=' + self.secretKey

            logging.info('Google custom search api request set: {}'\
                         .format(self.uniqueId))

            return make_query

        except KeyError:
            logging.error("incorrect value given to optional parameter")
            logging.info("reconfigure query for uniqueId: {0}; q: {1}"\
                         .format(self.q, self.uniqueId))

            


