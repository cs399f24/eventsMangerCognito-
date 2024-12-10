# eventsManagerCognito-


![Blank diagram (4)](https://github.com/user-attachments/assets/4dca78d3-f829-4782-ae79-d9ecf2d319a3)



## Steps

## 1. Create the DynamoDB database

Have it be called the EventsTable, with the primary key event_id.

## 2. Create the SNS_lambda function. 

Replace the ARN in the function with the SNS topic you are using for the application.

## 3. Create the add/delete/get/update lambda functions. 

In the add, delete, and update functions, replace the ARN with the ARN of your SNS_lambda function, allowing for notifications for when an event is added/updated/deleted. 

## 4. Create a REST API in API Gateway

## 5. Create the resources

Create an /add_event resource

Create a /events resource

in the /events resource, create an /{event_id} resource

## 6. Create the GET method in the /events resource 

Add the LabRole as the Execution Role in Integration Request

Add these Response Headers under Method Respone

Access-Control-Allow-Headers

Access-Control-Allow-Methods

Access-Control-Allow-Origin

Add this Header Mapping 

Access-Control-Allow-Origin '*'

## 7. Create the POST method in the /add_event resource 

Add the LabRole as the Execution Role in Integration Request

Add this application/json as the Mapping template in Integration Request

<img width="335" alt="Screenshot 2024-12-10 at 12 25 27 AM" src="https://github.com/user-attachments/assets/ff6d2511-2f37-41b4-9ec7-5cc3e9081f01">


Add these Response Headers under Method Respone

Access-Control-Allow-Headers

Access-Control-Allow-Methods

Access-Control-Allow-Origin

Add this Header Mapping 

Access-Control-Allow-Headers 'Content-Type'

Access-Control-Allow-Methods 'GET, POST, PUT, DELETE, OPTIONS'

Access-Control-Allow-Origin '*'

## 8. Create the DELETE method in the /events/{event_id} resource 

Add the LabRole as the Execution Role in Integration Request

Add this application/json as the Mapping template in Integration Request


<img width="319" alt="Screenshot 2024-12-10 at 12 26 11 AM" src="https://github.com/user-attachments/assets/bc1a9c85-c2c8-46d8-8b62-49ba00a2176e">




Add these Response Headers under Method Respone

Access-Control-Allow-Headers

Access-Control-Allow-Methods

Access-Control-Allow-Origin

Add this Header Mapping 

Access-Control-Allow-Headers 'Content-Type'

Access-Control-Allow-Methods 'GET, POST, PUT, DELETE, OPTIONS'

Access-Control-Allow-Origin '*'


## 9. Create the PUT method in the /events/{event_id} resource 

Add the LabRole as the Execution Role in Integration Request

Add this application/json as the Mapping template in Integration Request


<img width="462" alt="Screenshot 2024-12-10 at 12 26 26 AM" src="https://github.com/user-attachments/assets/354143e9-3430-4bb3-ab5b-5c0f1f6ee1fd">



Add these Response Headers under Method Respone

Access-Control-Allow-Headers

Access-Control-Allow-Methods

Access-Control-Allow-Origin

Add this Header Mapping 
 
Access-Control-Allow-Headers 'Content-Type'

Access-Control-Allow-Methods 'GET, POST, PUT, DELETE, OPTIONS'

Access-Control-Allow-Origin '*'

## 10. Enable CORS in each resource

Click each resource, click the Enable CORS button and check all the boxes in Gateway Responses and Access-Control-Allow-Methods

## 11. Create the Cognito User Pool to require users to use Email to log in 

Ensure that the OAuth 2.0 grant type is Implicit Grant.

## 12. Add a lambda trigger to automatically add users to the SNS subscription when they sign up. 

## 13. Add the Cognito User Pool as an authorizer in the API 

## 14. Deploy the API 

Recommended to name the stage as 'dev', as that requires less adjustments to the index.html
 
## 15. Create a new S3 Bucket

Enable all public access, enable static website hosting, and add the bucket policy

## 16. Upload the index.html to the S3 bucket

Ensure the index.html as your API invoke URL as the server 

## 17. Launch the application in Amplify

1. Deploy without Git
2. Use Amazon S3 as the Method, and select the new S3 bucket you made with the index.html
3. Save and deploy 

## Your app should now be up and running!






