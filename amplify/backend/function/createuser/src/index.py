import json
import boto3
import uuid
import os
from boto3.dynamodb.conditions import Attr


dynamodb = boto3.resource('dynamodb')

def handler(event, context):
  table_user_name = os.environ['STORAGE_USER_NAME']
  table_token_name = os.environ['STORAGE_TOKEN_NAME']
  table_user = dynamodb.Table(table_user_name)
  table_token = dynamodb.Table(table_token_name)

  check = check_if_user_exist(table_user, event)

  if check == False:
    create_user(table_user, event)
    user = get_user(table_user, event)
    create_token(table_token, user['Items'][0]['id'])
    token = get_token(table_token, user['Items'][0]['id'])
  else:
    token = get_token(table_token, check['id'])

  return {
      'token': token
  }

def check_if_user_exist(user_table, object):
  response = get_user(user_table, object)

  if not response['Items']:
   return False
  else:
    return response['Items'][0]

def create_user(table, object):
  obj = {
    'id': str(uuid.uuid4()),
    'firstName': object['firstName'],
    'lastName': object['lastName'],
    'age': object['age'],
  }
  response = table.put_item(Item=obj)

def create_token(table, user_id):
  obj= {
    'id': str(uuid.uuid4()),
    'token': str(uuid.uuid4()),
    'user_id': user_id,
  }
  table.put_item(Item=obj)


def get_token(table, user_id):

  columns = {
    '#token': 'token',
  }

  response = table.scan(
         FilterExpression=Attr('user_id').eq(user_id),
         ProjectionExpression="#token",
         ExpressionAttributeNames=columns
  )

  return response['Items'][0]['token']

def get_user(table, object):
  response = table.scan(
         FilterExpression=Attr('lastName').eq(object['lastName']),
         ProjectionExpression="id",
  )

  return response