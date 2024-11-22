import json
import boto3
import uuid
from botocore.exceptions import ClientError

# DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EventsTable')

# Lambda client for invoking the SNS notification Lambda
lambda_client = boto3.client('lambda')

# Helper function to invoke the notification Lambda
def invoke_notification_lambda(operation, event_details):
    try:
        # Prepare the payload for the notification Lambda
        payload = {
            'operation': operation,
            'body': json.dumps(event_details)  # The SNS Lambda expects a "body" key
        }
        
        # Invoke the SNS notification Lambda function
        response = lambda_client.invoke(
            FunctionName='arn:aws:lambda:us-east-1:857752321006:function:SNSNotificationEM',  # Replace with the actual name or ARN of your SNS Lambda function
            InvocationType='RequestResponse',  # For debugging; switch to 'Event' in production
            Payload=json.dumps(payload)
        )
        
        # Log the response for debugging
        print("Notification Lambda response:", response)
        return response  # Return the response for further inspection if needed
    except Exception as e:
        print("Error invoking notification Lambda:", str(e))
        raise  # Rethrow the exception for visibility

# Main Lambda handler
def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))
        data = json.loads(event['body'])
        
        # Validate required fields
        if not all(key in data for key in ('name', 'date', 'location')):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing required fields (name, date, location)'}),
                'headers': {'Content-Type': 'application/json'}
            }

        # Generate unique event ID
        new_event_id = str(uuid.uuid4())
        
        # Add the event to DynamoDB
        table.put_item(
            Item={
                'event_id': new_event_id,
                'name': data['name'],
                'date': data['date'],
                'location': data['location']
            }
        )
        
        # Invoke the SNS notification Lambda
        invoke_notification_lambda("add", {
            'event_id': new_event_id,
            'name': data['name'],
            'date': data['date'],
            'location': data['location']
        })
        
        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'Event added successfully', 'event_id': new_event_id}),
            'headers': {'Content-Type': 'application/json'}
        }

    except ClientError as e:
        print("ClientError:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error', 'details': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }
    except Exception as e:
        print("Unexpected error:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error', 'details': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }
