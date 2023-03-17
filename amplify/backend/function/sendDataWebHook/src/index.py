import json
import boto3
import os
import uuid
import secret
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['STORAGE_WEBHOOK_NAME']
table = dynamodb.Table(table_name)
table_user_name = os.environ['STORAGE_USER_NAME']
table_user = dynamodb.Table(table_user_name)

sqs = boto3.client('sqs')
SQS_URL = "https://sqs.eu-west-1.amazonaws.com/355243151688/webhookSqs"

def handler(event, context):
  response = {}

  headers = event.get('headers') or {}
  api_key = headers.get('x-api-key')

  if not api_key:
    response['statusCode'] = 500
    response['body'] = 'Input error: x-api-key'
    return response

  user_id = secret.get_secret_name(api_key)

  if not user_id:
    response['statusCode'] = 500
    response['body'] = json.dumps({"result":'Unknown token'})
    return response

  data = json.loads(event['body'])

  insertion = insert_webhook_element(table, user_id, data)
  update = update_user(table_user, user_id, data)

  if insertion and update:
    response['statusCode'] = 200
    response['body'] = json.dumps({"result":'Insertion ok'})
  else:
    response['statusCode'] = 500
    response['body'] = json.dumps({"result":"Problème lors de l'insertion"})

  send_to_sqs(user_id)

  return response


def insert_webhook_element(table, user_id, data):
  obj = {
    'id': str(uuid.uuid4()),
    'userId': user_id,
    'data': data['data']
  }
  try:
    table.put_item(Item=obj)
    return True
  except:
    return False

def update_user(table, user_id, data):

  expression = "SET webhook = :webhook"
  values = {
    ':webhook' : data['webhook']
  }
  sk = get_user_sk(table,user_id)

  try:
    table.update_item(
      Key={'id': user_id, 'lastName': sk},
      UpdateExpression=expression,
      ExpressionAttributeValues=values,
    )
    return True
  except:
    return False

def get_user_sk(table, user_id):
  response = table.query(
    KeyConditionExpression=Key('id').eq(user_id),
    ProjectionExpression="lastName"
  )
  return response['Items'][0]['lastName']

def send_to_sqs(user_id):
  truc = sqs.send_message(
    QueueUrl=SQS_URL,
    MessageBody=json.dumps({'userId':user_id})
  )
  print(truc)