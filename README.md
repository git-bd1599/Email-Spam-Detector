# Spam Detection

In this assignment we implemented a machine learning model to predict whether a message is spam or not. Furthermore, we created a system that upon receipt of an email message, it will automatically flag it as spam or not, based on the prediction obtained from the machine learning model.

### Outline: 
1. Completed tutorial for using Amazon SageMaker on AWS.
2. Implemented a Machine Learning model for predicting whether an SMS message is spam or not.
    - Deployed the resulting model to an endpoint (E1)
3. Implement an automatic spam tagging system.
    - Created an S3 bucket (S1) that will store email files.
    - Using SES, we set up an email address, that upon receipt of an email it stores it in S3.
    - For any new email file that is stored in S3, trigger a Lambda function (LF1) that extracts the body of the email and uses the prediction endpoint (E1) to predict if the           email is spam or not.
    - Reply to the sender of the email with a message as follows:
      
      “We received your email sent at [EMAIL_RECEIVE_DATE] with the subject [EMAIL_SUBJECT].
       
       Here is a 240 character sample of the email body: [EMAIL_BODY]
       
       The email was categorized as [CLASSIFICATION] with a [CLASSIFICATION_CONFIDENCE_SCORE]% confidence.”
       
       
4. Create an AWS CloudFormation template for the automatic spam tagging system.
    - Create a CloudFormation template (T1) to represent all the infrastructure resources (ex. Lambda, SES configuration, etc.) and permissions (IAM policies, roles, etc.).


![image](https://user-images.githubusercontent.com/61260957/120050130-de1e3300-bfe1-11eb-84f8-2db13d76bac5.png)



