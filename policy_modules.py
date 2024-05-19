#!/usr/bin/env python3

# aws_policy_modules

import json, boto3, re
from copy import deepcopy

class Statuement(object):
  def __init__(self, statement, source_policy):
    self.__fields = ['Sid', 'Effect', 'Principal', 'Action', 'Resource', 'Condition']
    self.__ori_statement = deepcopy(statement)
    self.__changing_statement = statement
    self.source_policy = source_policy
    self.reload()
    self.validate()

  def validate(self):
    if type(self.content) is not dict:
      raise ValueError('Error parsing statement.  Input is not a valid JSON object.')

  def save(self):
    for field in self.content.keys():
      if getattr(self, field) is not None:
        self.__changing_statement[field] = getattr(self, field)
      else:
        del self.__changing_statement[field]
    self.__ori_statement = deepcopy(self.__changing_statement)
    self.reload()
    return True

  def reload(self):
    self.content = deepcopy(self.__ori_statement)
    for field in self.__fields:
      setattr(self, field, self.content.get(field, None))




