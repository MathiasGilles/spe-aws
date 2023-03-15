import json
import boto3
import os
import uuid
import time

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['STORAGE_DATA_NAME']
table = dynamodb.Table(table_name)

def handler(event, context):
  time.sleep(60)
  event['id'] = str(uuid.uuid4())
  response = table.put_item(Item=event)
  
  return{
    'result': "200"
  }