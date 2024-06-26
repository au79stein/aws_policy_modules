#!/usr/bin/env python3

# aws_policy_modules

import json, boto3, re
from pprint import pprint
from copy import deepcopy

class Statement(object):
  def __init__(self, statement, source_policy):
    self.__fields = ['Sid', 'Effect', 'Principal', 'Action', 'Resource', 'Condition']
    self.__ori_statement = deepcopy(statement)
    self.__changing_statement = statement
    self.source_policy = source_policy
    self.reload()
    self.validate()

  def validate(self):
    if type(self.content) is not dict:
      raise ValueError('Error parsing statement. Input is not a valid JSON object.')

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

  def show_statement(self):
    pprint(self.source_policy)


class PolicyBase(object):
  def __init__(self, **kwargs):
    ''' resourceIdentifier: CMK Id or Arn, S3 Bucket Name, etc...
        serviceModule: eg: boto3.client('s3'), session.client('s3'), etc
    '''
    self.__serviceModule      = kwargs['serviceModule']
    self.__resourceIdentifier = kwargs['resourceIdentifier']
    self.reload()
    self.validate()
    self.sids = [ statement.get('Sid', '') for statement in self.Statement ]

  def validate(self):
    if type(self.content) is not dict:
      raise ValueError('Error parsing policy. Input is not a valid JSON object.')

  def fill_up_sids(self):
    c = 0
    for statement in self.Statement:
      if not statement.get('Sid', None):
        statement['Sid'] = 'statement' + str(c)
      c += 1
    self.save()

  def __is_principal_valid(self, p):
    # Identify valid principals. Deleted principal will be something like AI###########
    if re.compile("[A-Z0-9]{21}").match(p):
      return False
    else:
      return True

  def clean_up_deleted_principal(self):
    for statement in self.Statement:
      principal = statement.get('Principal')
      if type(principal) is dict:
        aws_principals = principal.get('AWS')
        if type(aws_principals) is not list:
          aws_principals = [aws_principals]
        if aws_principals:
          valid_aws_principals = [ p for p in aws_principals if self.__is_principal_valid(p) ]
          if len(valid_aws_principals) == 0:
            raise ValueError(f"Statement {str(statement)} has no valid AWS principal")
          else:
            principal['AWS'] = valid_aws_principals

  def select_statement(self, sid):
    searching = [ statement for statement in self.Statement if statement.get('Sid', None) == sid ]
    if len(searching) == 0:
      return None
    else:
      return Statement(searching[0], self)

  def show_statement(self):
    for statement in self.Statement:
      pprint(statement)
    #pol = json.loads(resp['Policy'])
    #pprint(pol)

  def reload(self):
    self.content = self.get_policy()
    self.__fields = self.content.keys() 
    for field in self.__fields:
      setattr(self, field, self.content.get(field, None))

  def save(self, clean_deleted_principals=False):
    self.validate()
    if clean_deleted_principals:
      self.clean_up_deleted_principals()
    policy_string = json.dumps(self.content)
    resp = self.put_policy(policy_string)
    self.reload()
    return resp


class BucketPolicy(PolicyBase):
  def __init__(self, **kwargs):
    super(BucketPolicy,self).__init__(**kwargs)

  def get_policy(self):
    resp = self._PolicyBase__serviceModule.get_bucket_policy(Bucket=self._PolicyBase__resourceIdentifier)
    return json.loads(resp['Policy'])

  def put_policy(self, policy_string):
    resp = self._PolicyBase__serviceModule.put_bucket_policy(Bucket=self._PolicyBase__resourceIdentifier, Policy=policy_string)
    return resp

