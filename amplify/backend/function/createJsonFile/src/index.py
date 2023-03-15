import json
import os
import boto3
from botocore.exceptions import ClientError
import upload

s3_client = boto3.client('s3')
bucket = os.environ['STORAGE_BUCKETJSONDATA_BUCKETNAME']

def handler(event, context):
  del event['userId']
  del event['action']
  upld = upload.upload_file(json.dumps(event), bucket)

  if upld:
    response = upload.create_presigned_url('data/data.json', bucket)
  else:
    response = "Impossible d'upload le file"

  return response