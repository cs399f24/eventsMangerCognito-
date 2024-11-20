import boto3
import json
import uuid
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EventsTable')

def lambda_handler(event, context):
    data = json.loads(event['body'])
    if 'name' in data and 'date' in data and 'location' in data:
        new_event_id = str(uuid.uuid4())
        try:
            table.put_item(
                Item={
                    'event_id': new_event_id,
                    'name': data['name'],
                    'date': data['date'],
                    'location': data['location']
                }
            )
            return {
                'statusCode': 201,
                'body': json.dumps({'message': 'Event added successfully'}),
                'headers': {'Content-Type': 'application/json'}
            }
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)}),
                'headers': {'Content-Type': 'application/json'}
            }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid event data'}),
            'headers': {'Content-Type': 'application/json'}
        }
