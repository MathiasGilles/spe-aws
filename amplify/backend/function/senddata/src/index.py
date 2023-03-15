import json
import secret
import os
import boto3
from action import Action

client = boto3.client('lambda')

def handler(event, context):
  headers = event.get('headers') or {}
  api_key = headers.get('x-api-key')

  if not api_key:
    raise ValueError('Input error: x-api-key')

  user_id = secret.get_secret_name(api_key)
  data = json.loads(event['body'])
  data['userId'] = user_id

  if data['action'] == Action.S3.value:
    response = trigger_lambda(os.environ['FUNCTION_CREATEJSONFILE_NAME'],data)
  elif data['action'] == Action.DYNAMO.value:
    response = trigger_lambda(os.environ['FUNCTION_CREATEDATADYNAMO_NAME'],data)
  else:
     response = 'Unknown action'

  return {
      'statusCode': 200,
      'body': json.dumps({'result':response})
  }

def trigger_lambda(lambda_name, data):
 response = client.invoke(
      FunctionName=lambda_name,
      Payload= json.dumps(data)
    )

 return response['Payload'].read().decode()