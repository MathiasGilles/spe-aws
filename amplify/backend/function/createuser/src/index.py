import json
import boto3
import uuid
import os
from boto3.dynamodb.conditions import Attr
import secret

dynamodb = boto3.resource('dynamodb')
secretmanager = boto3.client('secretsmanager')

def handler(event, context):
  response = {}

  table_user_name = os.environ['STORAGE_USER_NAME']
  table_user = dynamodb.Table(table_user_name)

  potential_user = json.loads(event['body'])
  check = check_if_user_exist(table_user, potential_user)

  if check == False:
    create_user(table_user, potential_user)
    user = get_user(table_user, potential_user)
    secret.create_secret(secret.SECRET_NAME, user['Items'][0]['id'])
    token = secret.get_secret(secret.SECRET_NAME, user['Items'][0]['id'])
  else:
    token = secret.get_secret(secret.SECRET_NAME,check['id'])

  response['statusCode'] = 200
  response['body'] = json.dumps({'token': token})

  return response

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

def get_user(table, object):
  response = table.scan(
         FilterExpression=Attr('lastName').eq(object['lastName']),
         ProjectionExpression="id",
  )

  return response