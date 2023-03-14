import boto3
import json

secretmanager = boto3.client('secretsmanager')

SECRET_NAME = 'user_token'

def create_secret(key, id):

  all_secret = get_all_secret(key)
  all_secret[id] = str(uuid.uuid4())

  secretmanager.put_secret_value(
    SecretId=key,
    SecretString= json.dumps(all_secret)
  )
def get_secret (secret_name,secret_key):
  secret_object = secretmanager.get_secret_value(SecretId=secret_name)

  secret_values = secret_object.get('SecretString', None)

  if secret_values is None:
      raise ValueError('No keys detected')

  secret_json = json.loads(secret_values)
  secret_key_value = secret_json.get(secret_key, None)

  if secret_key_value is None:
      raise ValueError(f'No such key { secret_key }')

  return secret_key_value

def get_all_secret (secret_name):
   secret_object = secretmanager.get_secret_value(SecretId=secret_name)

   secret_values = secret_object.get('SecretString', None)

   if secret_values is None:
       raise ValueError('No keys detected')

   secret_json = json.loads(secret_values)

   return secret_json

def get_secret_name(secret_value):
    all_secret = get_all_secret(SECRET_NAME)
    for key in all_secret:
      if all_secret[key] == secret_value:
        return key

    raise ValueError('Unknown token')