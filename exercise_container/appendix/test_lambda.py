import json
import boto3

def lambda_handler(event, context):

    results = []
    for record in event['Records']:
        msg = record['body']
        event_src_arn = record['eventSourceARN']
        message_id = record['messageId']

        file_contents = json.loads(msg)

        results.append({
                    'message': file_contents, 
                    'event_source_arn': event_src_arn,
                    'message_id': message_id,
                })
    
    return {'results': results}