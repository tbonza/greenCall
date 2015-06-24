# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 18:15:52 2015

@author: bmcdonnell
"""

# mock data structure
google = {"content": "foo", 
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

# correctly formatted documents for _source of elasticsearch entry
correct_documents = [
    {"content":"foo"},
    {"results": ["result_one", "result_two", "result_three"]},
    {"result_one": ["persona", "personb", "personc"]},
    {"persona": "phone"},
    {"personb": "phone"},
    {"personc": "phone"},
    {"result_two":["thing1","thing2","thing3"]},
    {"result_three": "none"},
    {"query": ["Taylor Swift", "Bob Dole", "Rocketman"]}
]

def recursive_dfs(graph, start, path=[]):
  '''recursive depth first search from start'''
  path=path+[start]
  for node in graph[start]:
    if not node in path:
      path=recursive_dfs(graph, node, path)
  return path

def branching(google):
    """ Get branches as a starting point for dfs"""
    branch = 0
    while branch < len(google):

        if google[google.keys()[branch]] is dict:

            #recursive_dfs(google, google[google.keys()[branch]])
            pass

        else:
            print("branch {}: result {}\n".format(branch,     google[google.keys()[branch]]))

        branch += 1

#branching(google)

class ApiConversion(object):

  def __init__(self):
    self.documents = []

  def myfunk( self, inHole ):
    for keys in inHole.keys():
        is_list = isinstance(inHole[keys],list)
        is_dict = isinstance(inHole[keys],dict)
        if is_list:
            element = inHole[keys]
            new_element = {keys:element}
            self.documents.append(new_element)

        if is_dict:
            element = inHole[keys].keys()
            new_element = {keys:element}
            self.documents.append(new_element)
            self.myfunk(inHole[keys])

        if not(is_list or is_dict):
            new_element = {keys:inHole[keys]}
            self.documents.append(new_element)

    return self.documents.sort()
  
#a = []
#b = myfunk(google, a)

ac = ApiConversion()

ac.myfunk(google)

print("data type: {}".format(ac.documents))


#for i in a:
#    print i, i in correct_documents
#print cmp(b,correct_documents)
