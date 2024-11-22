import json
import boto3
from botocore.exceptions import ClientError

sns_client = boto3.client('sns')

def lambda_handler(event, context):
    try:
        # Log the incoming event for debugging
        print("Received event:", json.dumps(event))
        
        # Ensure body is parsed correctly if it's a stringified JSON
        if isinstance(event['body'], str):
            event_details = json.loads(event['body'])
        else:
            event_details = event['body']

        # Extract operation type
        operation = event.get('operation')
        if not operation:
            raise ValueError("Operation type (add, update, delete) is missing")

        # Initialize the message and subject
        subject = f"Event {operation.capitalize()} Notification"
        message = ""

        if operation == "add":
            message = f"New event added:\nName: {event_details['name']}\nDate: {event_details['date']}\nLocation: {event_details['location']}"
        
        elif operation == "update":
            event_id = event_details.get('event_id')
            if not event_id:
                raise ValueError("Event ID is required for update operation")
            message = f"Event {event_id} updated:\nName: {event_details.get('name', 'Not updated')}\nDate: {event_details.get('date', 'Not updated')}\nLocation: {event_details.get('location', 'Not updated')}"
        
        elif operation == "delete":
            event_id = event_details.get('event_id')
            if not event_id:
                raise ValueError("Event ID is required for delete operation")
            message = f"Event {event_id} has been deleted."
        
        else:
            raise ValueError("Invalid operation type. Use add, update, or delete.")

        # Send SNS notification
        response = sns_client.publish(
            TopicArn='arn:aws:sns:us-east-1:857752321006:EventsManagerNotifications',  # Use the correct ARN
            Subject=subject,
            Message=message
        )

        # Log the SNS response for debugging
        print("SNS Notification Sent:", response)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': f"Notification sent for event {operation}."})
        }
    
    except ValueError as ve:
        # Handle specific value errors and log
        print("ValueError:", str(ve))
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(ve)})
        }
    
    except ClientError as e:
        # Log the error when SNS fails
        print("Error sending SNS notification:", e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error', 'details': str(e)})
        }
    
    except Exception as e:
        # Catch any unexpected errors
        print("Unexpected error:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error', 'details': str(e)})
        }
