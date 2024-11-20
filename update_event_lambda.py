import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EventsTable')  # Replace with your table name

def lambda_handler(event, context):
    try:
        event_id = event['pathParameters']['event_id']
        data = json.loads(event['body'])

        # Check if the event exists
        response = table.get_item(Key={'event_id': event_id})
        if 'Item' not in response:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Event not found"})
            }

        # Proceed with the update
        table.update_item(
            Key={'event_id': event_id},
            UpdateExpression="SET #n = :name, #d = :date, #l = :location",
            ExpressionAttributeNames={
                '#n': 'name',
                '#d': 'date',
                '#l': 'location'
            },
            ExpressionAttributeValues={
                ':name': data['name'],
                ':date': data['date'],
                ':location': data['location']
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Event updated successfully"})
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
