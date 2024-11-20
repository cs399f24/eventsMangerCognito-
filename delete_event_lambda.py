import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EventsTable')  # Replace with your table name

def lambda_handler(event, context):
    try:
        event_id = event['pathParameters']['event_id']

        # Check if the event exists
        response = table.get_item(Key={'event_id': event_id})
        if 'Item' not in response:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Event not found"})
            }

        # Proceed with deletion
        table.delete_item(Key={'event_id': event_id})

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Event deleted successfully"})
        }

    except ClientError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
    except KeyError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid input"})
        }
