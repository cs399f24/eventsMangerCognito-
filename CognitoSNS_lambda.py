import boto3

sns_client = boto3.client('sns')
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:857752321006:EventsManagerNotifications'  # Replace with your ARN

def lambda_handler(event, context):
    try:
        # Extract user's email from the event
        email = event['request']['userAttributes']['email']
        if not email:
            raise ValueError("No email found in user attributes")
        
        # Subscribe the user to the SNS topic
        response = sns_client.subscribe(
            TopicArn=SNS_TOPIC_ARN,
            Protocol='email',
            Endpoint=email
        )
        
        print("Subscription successful:", response)
        return event  # Cognito expects the event object to be returned
    
    except Exception as e:
        print("Error subscribing user to SNS:", str(e))
        raise  # Raising the error to ensure Cognito is notified of the failure
