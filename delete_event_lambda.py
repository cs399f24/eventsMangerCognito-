import boto3
import json
from botocore.exceptions import ClientError

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EventsTable')

def lambda_handler(event, context):
    # Get event_id from pathParameters
    event_id = event['pathParameters']['event_id']
    
    try:
        # Check if the event exists by getting the item first
        response = table.get_item(
            Key={'event_id': event_id}
        )
        
        # If the event is not found
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Event not found'}),
                'headers': {'Content-Type': 'application/json'}
            }

        # If the event exists, proceed to delete it
        table.delete_item(
            Key={'event_id': event_id}
        )

        # Return success response if deletion is successful
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Event deleted successfully'}),
            'headers': {'Content-Type': 'application/json'}
        }

    except ClientError as e:
        # Handle DynamoDB errors
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }
