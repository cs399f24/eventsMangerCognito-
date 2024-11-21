import boto3
import json
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EventsTable')

def lambda_handler(event, context):
    try:
        # Scan DynamoDB for all events
        response = table.scan()
        
        # Prepare events in a dictionary format where each event ID is the key
        events = {item['event_id']: item for item in response['Items']}
        
        # Return the response with the events as an actual JSON object (not stringified)
        return {
            'statusCode': 200,
            'body': json.dumps(events),  # JSON string that will be parsed by API Gateway
            'headers': {'Content-Type': 'application/json'}
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }
