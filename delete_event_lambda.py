import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table_name = "EventsTable"  # Replace with your table name
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    print("Event received:", json.dumps(event))
    
    try:
        # Retrieve event_id from pathParameters
        event_id = event['pathParameters']['event_id']
        print(f"Attempting to delete event with ID: {event_id}")
        
        # Check if the event exists
        response = table.get_item(Key={'event_id': event_id})
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({"error": "Event not found"})
            }
        
        # If it exists, delete the item
        table.delete_item(Key={'event_id': event_id})
        return {
            'statusCode': 200,
            'body': json.dumps({"message": f"Event {event_id} deleted successfully"})
        }
    
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"error": "Missing or invalid path parameter", "details": str(e)})
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({"error": "Internal server error", "details": str(e)})
        }
