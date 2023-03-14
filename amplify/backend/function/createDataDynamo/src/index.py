import json
import os
import uuid
import boto3
from botocore.config import Config

my_config = Config(
    region_name='eu-west-1',
)
dynamodb = boto3.resource('dynamodb', config=my_config)
table_data_name = os.environ['STORAGE_DATA_NAME']
table_data = dynamodb.Table(table_data_name)


def handler(event, context):
    obj = {
        'id': str(uuid.uuid4()),
        'userId': event['userId'],
        'data': event['data']
    }

    response = table_data.put_item(Item=obj)

    return {
        response
    }
