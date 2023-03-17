import json
import os
import boto3
import upload
import requests

s3_client = boto3.client("s3")

def handler(event, context):
  bucket = "bucketjsondata92122-" + os.environ['ENV']

  file_key = event['Records'][0]['s3']['object']['key']

  file = json.loads(upload.read_file(file_key, bucket))
  data = {'data':json.dumps(file['data'])}

  send(file['webhook'], data)

  return {
      'statusCode': 200,
      'headers': {
          'Access-Control-Allow-Headers': '*',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
      },
      'body': json.dumps('Hello from your new Amplify Python lambda!')
  }

def send(url, data):
  try:
    requests.post(url, data)
  except Exception as error:
    print(error)
    return False

  return True