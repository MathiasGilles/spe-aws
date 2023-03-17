import json
import boto3
import os
import upload
from boto3.dynamodb.conditions import Key, Attr

sqs = boto3.client('sqs')
dynamo = boto3.resource('dynamodb')
s3_client = boto3.client('s3')

user_table = dynamo.Table(os.environ['STORAGE_USER_NAME'])
webhook_table = dynamo.Table(os.environ['STORAGE_WEBHOOK_NAME'])

SQS_URL = "https://sqs.eu-west-1.amazonaws.com/355243151688/webhookSqs"

bucket = os.environ['STORAGE_BUCKETJSONDATA_BUCKETNAME']

def handler(event, context):

  user_id = json.loads(event['Records'][0]['body'])['userId']
  webhook = get_webhook(user_id)
  data = get_data(user_id)
  
  response = {}
  response['userId'] = user_id
  response['webhook'] = webhook
  response['data'] = data

  upld = upload.upload_file(json.dumps(response), bucket, key="webhook/data.json")
  print(upld)
  return {
    'statusCode': 200,
    'body': json.dumps('Hello from your new Amplify Python lambda!')
  }

def get_webhook(user_id):
  try:
    response = user_table.scan(
      ProjectionExpression='webhook',
      FilterExpression=Attr('id').eq(user_id)
    )
    return response['Items'][0]['webhook']
  except:
   return False

def get_data(user_id):

  columns = {
    '#data': 'data'
  }
  try:
    response = webhook_table.query(
      IndexName="userId__",
      KeyConditionExpression=Key("userId").eq(user_id),
      ProjectionExpression="#data",
      ExpressionAttributeNames=columns,
    )
    return response['Items']
  except:
    return False