import json
import secret
from action import Action

def handler(event, context):
  headers = event.get('headers') or {}
  api_key = headers.get('x-api-key')

  if not api_key:
    raise ValueError('Input error: x-api-key')

  user_id = secret.get_secret_name(api_key)
  data = json.loads(event['body'])

  if data['action'] == Action.S3.value:
    response = "s3"
  elif data['action'] == Action.DYNAMO.value:
    response = 'dynamo'
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