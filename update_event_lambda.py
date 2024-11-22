import json
import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EventsTable')

# Initialize Lambda client to invoke the SNS notification function
lambda_client = boto3.client('lambda')

# Method to invoke the SNS notification Lambda
def invoke_notification_lambda(operation, event_details):
    try:
        # Prepare the payload for the SNS notification Lambda
        payload = {
            'operation': operation,
            'body': json.dumps(event_details)
        }

        # Invoke the SNS notification Lambda function
        response = lambda_client.invoke(
            FunctionName='arn:aws:lambda:us-east-1:857752321006:function:SNSNotificationEM',  # Replace with the actual name or ARN
            InvocationType='Event',  # 'Event' is used for asynchronous invocation
            Payload=json.dumps(payload)
        )

        # Log the response for debugging
        print("Notification Lambda response:", response)
        return response
    except Exception as e:
        print("Error invoking notification Lambda:", str(e))
        raise

def lambda_handler(event, context):
    try:
        # Log the incoming event for debugging
        print("Received event:", json.dumps(event))
        
        # Extract the event ID and data from the request
        body = json.loads(event['body'])
        event_id = event['pathParameters']['event_id']  # Get the event_id from pathParameters

        # Extract updated details from the body
        name = body['name']
        date = body['date']
        location = body['location']

        # Update the event details in DynamoDB
        response = table.update_item(
            Key={'event_id': event_id},
            UpdateExpression="set #name = :name, #date = :date, #location = :location",
            ExpressionAttributeNames={
                '#name': 'name',
                '#date': 'date',
                '#location': 'location'
            },
            ExpressionAttributeValues={
                ':name': name,
                ':date': date,
                ':location': location
            },
            ReturnValues="UPDATED_NEW"
        )

        # Log the DynamoDB response for debugging
        print("DynamoDB Update Response:", response)

        # Prepare the event details for the notification Lambda
        event_details = {
            'event_id': event_id,
            'name': name,
            'date': date,
            'location': location
        }

        # Invoke the SNS notification Lambda for update operation
        invoke_notification_lambda("update", event_details)
        
        # Return success response with updated event details
        return {
            'statusCode': 200,
            'body': json.dumps({
                "message": "Event updated successfully",
                "updated": response
            }),
            'headers': {'Content-Type': 'application/json'}
        }

    except ClientError as e:
        # Log the error for debugging
        print("ClientError:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error', 'details': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }
    except Exception as e:
        # Log the error for debugging
        print("Unexpected error:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error', 'details': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }
