import json

def handler(event, context):
  headers = event.get('headers') or {}
  api_key = headers.get('x-api-key')

    if not api_key:
      raise ValueError('Input error: x-api-key')
  
  return {
      'statusCode': 200,
      'headers': {
          'Access-Control-Allow-Headers': '*',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
      },
      'body': json.dumps('Hello from your new Amplify Python lambda!')
  }