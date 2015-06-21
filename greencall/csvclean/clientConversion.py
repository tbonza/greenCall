""" Converts JSON file to client API format, retains unique id """

import json
import logging



class ClientConversion(object):
    """ Converts JSON file to Client API format """

    def __init__(self, clientclass, querystr):
        """
        Args:
          clientclass: class, Client API conversion class
          querystr: str, query string to be converted
        """
        self.client = clientclass
        self.q = querystr

    def convertString(self, domethod):
        """ Returns client API request format 
        
        Args:
          domethod: method from client class the converts query string

        Returns:
          str, client API request format
        """
        return self.client.domethod(self.q)


def runConversion(jsonpath, clientclass, domethod):
    """ Converts JSON file to client API format 

    Args:
      jsonpath: path to JSON file that's been converted from CSV input
      clientclass: class, Client API conversion clas
      domethod: method from client class the converts query string

    Returns:
      Python dictionary that is a valid param for use in crawlah.py
    """
    with open(jsonpath, 'r') as jsonin:
        obs = json.load(jsonin)
        jsonin.close()

    for key in obs.keys():
        cc = ClientConversion(clientclass, obs[key])
        
        obs[key] = cc.convertString(domethod)

    return obs
        
        

