import json
import boto3
import uuid
import os
from boto3.dynamodb.conditions import Attr


dynamodb = boto3.resource('dynamodb')
secretmanager = boto3.client('secretsmanager')

SECRET_NAME = 'user_token'

def handler(event, context):
  response = {}

  table_user_name = os.environ['STORAGE_USER_NAME']
  table_user = dynamodb.Table(table_user_name)

  potential_user = json.loads(event['body'])
  check = check_if_user_exist(table_user, potential_user)

  if check == False:
    create_user(table_user, potential_user)
    user = get_user(table_user, potential_user)
    create_secret(SECRET_NAME, user['Items'][0]['id'])
    token = get_secret(SECRET_NAME, user['Items'][0]['id'])
  else:
    token = get_secret(SECRET_NAME,check['id'])

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

def create_secret(key, id):

  all_secret = get_all_secret(key)
  all_secret[id] = str(uuid.uuid4())
  print(all_secret)
  response = secretmanager.put_secret_value(
    SecretId=key,
    SecretString= json.dumps(all_secret)
  )
  print(response)

def get_user(table, object):
  response = table.scan(
         FilterExpression=Attr('lastName').eq(object['lastName']),
         ProjectionExpression="id",
  )

  return response

def get_secret (secret_name,secret_key):
    secret_object = secretmanager.get_secret_value(SecretId=secret_name)

    secret_values = secret_object.get('SecretString', None)

    if secret_values is None:
        raise ValueError('No keys detected')

    secret_json = json.loads(secret_values)
    secret_key_value = secret_json.get(secret_key, None)

    if secret_key_value is None:
        raise ValueError(f'No such key { secret_key }')

    return secret_key_value

def get_all_secret (secret_name):
    secret_object = secretmanager.get_secret_value(SecretId=secret_name)

    secret_values = secret_object.get('SecretString', None)

    if secret_values is None:
        raise ValueError('No keys detected')

    secret_json = json.loads(secret_values)

    return secret_json