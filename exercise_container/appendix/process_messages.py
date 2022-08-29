import json
import boto3
import os

def lambda_handler(event, context):

    session = boto3.Session(
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name=os.environ.get('REGION_NAME')
    )

    s3 = session.resource(
        's3', 
        endpoint_url=os.environ.get('ENDPOINT_URL')
    )
    bucket_name = os.environ.get('BUCKET_NAME')

    results = []
    for record in event['Records']:
        msg = record['body']
        event_src_arn = record['eventSourceARN']
        message_id = record['messageId']

        file_contents = json.loads(msg)
        file_contents['sentence'] = f'{file_contents["name"]} said, "{file_contents["word"]}"'
        key = "".join(["queue_output_msg_", message_id, ".json"])
        bucket = s3.Object(bucket_name, key)
        res = bucket.put(Body=json.dumps(file_contents))

        results.append(
            {
                'queue': {
                    'message': file_contents, 
                    'event_source_arn': event_src_arn,
                    'message_id': message_id,
                },
                's3': {
                    'file_name': key,
                    'responce': res,
                }
            }
        )
    
    return {'results': results}