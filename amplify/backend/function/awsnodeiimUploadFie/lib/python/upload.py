import boto3

s3_client = boto3.client('s3')

def upload_file(file_name, bucket, key="data/data.json"):
    try:
        response = s3_client.put_object(Body=file_name, Bucket=bucket, Key=key)
    except ClientError as e:
        return False
    return True

def create_presigned_url(object_name, bucket_name, expiration=3600):
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        return None

    return response