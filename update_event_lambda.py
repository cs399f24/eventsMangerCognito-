import boto3
import json
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EventsTable')

def lambda_handler(event, context):
    # Log the event for debugging
    print("Received event:", json.dumps(event))
    
    event_id = event['pathParameters']['event_id']
    data = json.loads(event['body'])

    # Check if required fields are in the body
    if 'name' in data and 'date' in data and 'location' in data:
        try:
            # Fetch the event to check if it exists
            response = table.get_item(
                Key={'event_id': event_id}
            )
            if 'Item' not in response:
                print(f"Event {event_id} not found in the database.")
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': 'Event not found'}),
                    'headers': {'Content-Type': 'application/json'}
                }

            # Update the event if it exists
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
                },
                ReturnValues="UPDATED_NEW"
            )
            print(f"Event {event_id} updated successfully.")
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Event updated successfully'}),
                'headers': {'Content-Type': 'application/json'}
            }

        except ClientError as e:
            print(f"Error updating event: {e}")
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
