import json
import os
import upload

bucket = os.environ['STORAGE_BUCKETJSONDATA_BUCKETNAME']

def handler(event, context):

  file_key = event['Records'][0]['s3']['object']['key']
  print(file_key)
  file = upload.read_file(file_key, bucket)
  print(file)
  return {
      'statusCode': 200,
      'headers': {
          'Access-Control-Allow-Headers': '*',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
      },
      'body': json.dumps('Hello from your new Amplify Python lambda!')
  }

