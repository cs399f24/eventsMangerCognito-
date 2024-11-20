import boto3
import json
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EventsTable')

def lambda_handler(event, context):
    try:
        response = table.scan()
        events = {item['event_id']: item for item in response['Items']}
        return {
            'statusCode': 200,
            'body': json.dumps(events),
            'headers': {'Content-Type': 'application/json'}
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }
