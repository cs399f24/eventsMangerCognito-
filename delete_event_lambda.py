import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EventsTable')

lambda_client = boto3.client('lambda')

def invoke_notification_lambda(operation, event_details):
    try:
        payload = {
            'operation': operation,
            'body': event_details
        }
        print(f"Invoking SNS Lambda with payload: {json.dumps(payload)}")
        
        response = lambda_client.invoke(
            FunctionName='arn:aws:lambda:us-east-1:857752321006:function:SNSNotificationEM',
            InvocationType='Event',
            Payload=json.dumps(payload)
        )

        # Log the response for debugging
        print(f"Notification Lambda response: {response}")
        return response
    except Exception as e:
        print(f"Error invoking notification Lambda: {str(e)}")
        raise


def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))
        event_id = event['pathParameters']['event_id']
        
        # Check if the event exists
        response = table.get_item(Key={'event_id': event_id})
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({"error": "Event not found"}),
                'headers': {'Content-Type': 'application/json'}
            }
        
        # Delete the event
        table.delete_item(Key={'event_id': event_id})
        
        # Invoke the SNS notification Lambda
        invoke_notification_lambda("delete", {'event_id': event_id})
        
        return {
            'statusCode': 200,
            'body': json.dumps({"message": f"Event {event_id} deleted successfully"}),
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
