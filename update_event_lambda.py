import json
import boto3

def lambda_handler(event, context):
    # Parse the body of the request (which is passed as a string)
    try:
        body = json.loads(event['body'])  # Parse the stringified JSON body into a Python dictionary
        event_id = event['pathParameters']['event_id']  # Get the event_id from the path parameters

        # Extract the data from the request body
        name = body['name']
        date = body['date']
        location = body['location']

        # Initialize DynamoDB client
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('EventsTable')  # Replace with your DynamoDB table name

        # Update the item in DynamoDB using the event_id
        response = table.update_item(
            Key={'event_id': event_id},  # The primary key of the event to update
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
            ReturnValues="UPDATED_NEW"  # Returns the updated values
        )

        # Return a successful response
        return {
            'statusCode': 200,
            'body': json.dumps({"message": "Event updated successfully", "updated": response})
        }

    except Exception as e:
        # Return an error response in case of issues
        return {
            'statusCode': 500,
            'body': json.dumps({"error": "Internal Server Error", "details": str(e)})
        }
