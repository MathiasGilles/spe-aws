import json
import secret
import os
import boto3
from action import Action

def handler(event, context):
  headers = event.get('headers') or {}
  api_key = headers.get('x-api-key')

  if not api_key:
    raise ValueError('Input error: x-api-key')

  user_id = secret.get_secret_name(api_key)
  data = json.loads(event['body'])
  data['userId'] = user_id

  if data['action'] == Action.S3.value:
    response = trigger_lambda('createDataDynamo',data)
  elif data['action'] == Action.DYNAMO.value:
    #response = trigger_lambda('',data)
    response = "to do s3"
  else:
     raise ValueError('Unknown action')

  return {
      'statusCode': 200,
      'headers': {
          'Access-Control-Allow-Headers': '*',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
      },
      'body': json.dumps(response)
  }

def trigger_lambda(lambda_name, data):
 boto3.invoke(
      FunctionName=lambda_name+"-"+str(os.environ['ENV']),
      Payload= json.dumps(data)
    )