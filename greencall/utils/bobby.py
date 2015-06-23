# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 18:15:52 2015

@author: bmcdonnell
"""
def myfunk( inHole, outHole):
  """
  a = [];
  b = myfunk(google, a);

  Args:
      inHole: Nested dictionary containing either other dictionaries,
              lists, or strings. Originally set up to parse results from
              the Google Search API

      outHole: list

  Returns:
      List of dictionaries where each dict is mapped to a string
      or list.
  """
  for keys in inHole.keys():
    is_list = isinstance(inHole[keys],list);
    is_dict = isinstance(inHole[keys],dict);
    if is_list:
      element = inHole[keys];
      new_element = {keys:element};
      outHole.append(new_element);
  
    if is_dict:
      element = inHole[keys].keys();
      new_element = {keys:element};
      outHole.append(new_element);
      myfunk(inHole[keys], outHole);

    if not(is_list or is_dict):
      new_element = {keys:inHole[keys]};
      outHole.append(new_element);

  return outHole.sort();

