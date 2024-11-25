# eventsManagerCognito-

![Blank diagram (2)](https://github.com/user-attachments/assets/d4e19019-ceb1-4aae-b1e9-864f70c1faac)


## Steps

## 1. Create the SNS_lambda function. 

### Replace the ARN in the function with the SNS topic you are using for the application.

## 2. Create the add/delete/get/update lambda functions. 

### In the add, delete, and update functions, replace the ARN with the ARN of your SNS_lambda function, allowing for notifications for when an event is added/updated/deleted. 

## 3. Create a REST API in API Gateway

## 4. Create the resources

### Create an /add_event resource
### Create a /events resource
### in the /events resource, create an /{event_id} resource

## 5. Create the GET method in the /events resource 

## Add the LabRole as the Execution Role in Integration Request

### Add these Response Headers under Method Respone

Access-Control-Allow-Headers
Access-Control-Allow-Methods
Access-Control-Allow-Origin

 ### Add this Header Mapping 

Access-Control-Allow-Origin '*'

## 6. Create the POST method in the /add_event resource 

## Add the LabRole as the Execution Role in Integration Request

## Add this application/json as the Mapping template in Integration Request

{
  "body": "$util.escapeJavaScript($input.body)"
}


### Add these Response Headers under Method Respone

Access-Control-Allow-Headers
Access-Control-Allow-Methods
Access-Control-Allow-Origin

 ### Add this Header Mapping 

Access-Control-Allow-Headers 'Content-Type'
Access-Control-Allow-Methods 'GET, POST, PUT, DELETE, OPTIONS'
Access-Control-Allow-Origin '*'

## 7. Create the DELETE method in the /events/{event_id} resource 

## Add the LabRole as the Execution Role in Integration Request

## Add this application/json as the Mapping template in Integration Request

{
    "pathParameters": {
        "event_id": "$input.params('event_id')"
    }
}


### Add these Response Headers under Method Respone

Access-Control-Allow-Headers
Access-Control-Allow-Methods
Access-Control-Allow-Origin

 ### Add this Header Mapping 

Access-Control-Allow-Headers 'Content-Type'
Access-Control-Allow-Methods 'GET, POST, PUT, DELETE, OPTIONS'
Access-Control-Allow-Origin '*'


## 8. Create the PUT method in the /events/{event_id} resource 

## Add the LabRole as the Execution Role in Integration Request

## Add this application/json as the Mapping template in Integration Request

{
  "body": "$util.escapeJavaScript($input.body).replaceAll("\\'", "'")",
  "pathParameters": {
    "event_id": "$input.params('event_id')"
  }
}


### Add these Response Headers under Method Respone

Access-Control-Allow-Headers
Access-Control-Allow-Methods
Access-Control-Allow-Origin

 ### Add this Header Mapping 
 
Access-Control-Allow-Headers 'Content-Type'
Access-Control-Allow-Methods 'GET, POST, PUT, DELETE, OPTIONS'
Access-Control-Allow-Origin '*'

## 9. Enable CORS in each resource

### Click each resource, click the Enable CORS button and check all the boxes in Gateway Responses and Access-Control-Allow-Methods

## 10. Deploy the API 

### Recommended to name the stage as 'dev', as that requires less adjustments to the index.html

## 11. Create a new S3 Bucket

### Enable all public access, enable static website hosting, and add the bucket policy

## 12. Upload the index.html to the S3 bucket

### Ensure the index.html as your API invoke URL as the server

## 13. Launch the application in Amplify

### 1. Deploy without Git
### 2. Use Amazon S3 as the Method, and select the new S3 bucket you made with the index.html
### 3. Save and deploy 

## Your app should now be up and running!






