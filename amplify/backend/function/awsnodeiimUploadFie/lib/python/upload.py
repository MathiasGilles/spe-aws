import boto3

s3_client = boto3.client('s3')

def upload_file(file_name, bucket, key="data/data.json"):
    try:
        response = s3_client.put_object(Body=file_name, Bucket=bucket, Key=key)
    except:
        return False
    return True

def create_presigned_url(object_name, bucket_name, expiration=3600):
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except:
        return None

    return response

def read_file(object_key, bucket):
  try:
    response = s3_client.get_object(Bucket=bucket, Key=object_key)
  except Exception as error:
    print(error)
    return False
  return response['Body'].read()