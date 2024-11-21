import json
import boto3
import uuid
import os
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EventsTable')

def lambda_handler(event, context):
    try:
        # Log incoming event for debugging purposes
        print("Received event:", json.dumps(event))  # This logs the entire event
        print("Received body:", event['body'])  # Log the body itself

        # Parse the event body to a dictionary
        data = json.loads(event['body'])

        # Validate required fields
        if not all(key in data for key in ('name', 'date', 'location')):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing required fields (name, date, location)'}),
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
            }

        # Generate unique event ID
        new_event_id = str(uuid.uuid4())
        
        # Log the event ID and data
        print(f"Generated new event ID: {new_event_id}")
        
        # Insert the new event into DynamoDB
        response = table.put_item(
            Item={
                'event_id': new_event_id,
                'name': data['name'],
                'date': data['date'],
                'location': data['location']
            }
        )
        
        # Log DynamoDB response for debugging
        print("DynamoDB response:", response)
        
        # Return success response
        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'Event added successfully', 'event_id': new_event_id}),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        }

    except ClientError as e:
        print(f"ClientError: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error', 'details': str(e)}),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        }
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error', 'details': str(e)}),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        }
