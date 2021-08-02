# Helium-Analysis
This is the repo for python scripts to analyze and display the data coming in from helium hotspots. 

AWS services used : 
- Lambda (Created the back and front end)
- Cognito (User authentication)
- Dynamodb (Database)
- API Gatewaay (Created an REST API connected with the database)
- CloudWatch (Sceduled events)

Backend is powered by Dynamodb, AWS Lambda and the Helium API. The security layer and role based access is provided by AWS Cognito. Using the database, I use JavaScript, HTML and CSS to design a front end which is integrated with the AWS Lambda functions. 


