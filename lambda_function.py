import json
import email
import boto3
import numpy as np
import os
from sms_spam_classifier_utilities import one_hot_encode
from sms_spam_classifier_utilities import vectorize_sequences

def lambda_handler(event, context):
    
    s3 = boto3.client("s3")
    vocabulary_length = 9013
    ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
    runtime = boto3.client('runtime.sagemaker')
    ses = boto3.client('ses')
    test_messages = []

    if event: 

        print("My Event is : ", event)
        file_obj = event["Records"][0]
        filename = str(file_obj["s3"]['object']['key'])
        print("filename: ", filename)
        fileObj = s3.get_object(Bucket = "filtered-mail-box", Key=filename)
        print("file has been gotten!")
        msg = email.message_from_bytes(fileObj['Body'].read())
        subject = msg["Subject"]
        return_path = msg["Return-Path"]
        date = msg["Date"]
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if "plain" in content_type:
                    payload = part.get_payload().rstrip("\n")
                    #print(payload)
        
        newpayload = ""
        for line in payload:
            newpayload = newpayload + line.rstrip('\n')
        print(newpayload)

        test_messages.append(newpayload)
        one_hot_test_messages = one_hot_encode(test_messages, vocabulary_length)
        encoded_test_messages = vectorize_sequences(one_hot_test_messages, vocabulary_length)
        

        data = np.array(encoded_test_messages)
        #print(data)
        
        data = encoded_test_messages
        payload_to_endpoint = json.dumps(data.tolist())

        response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                   ContentType='application/json',
                                   Body=payload_to_endpoint)

        result = json.loads(response['Body'].read().decode())

        print(result)
        
        predicted_probability = result['predicted_probability'][0][0]
        predicted_label = result['predicted_label'][0][0]

        classification_confidence_score = predicted_probability*100
        
        #print(predicted_label)

        if predicted_label == 1.0:
            classification = 'SPAM'
        else:
            classification = 'HAM'

        print("The email was categorized as {} with a {}% confidence.".format(classification, classification_confidence_score))
        print(subject, return_path, date)
        
        SENDER = "Karan Mankar <kmm1110@nyu.edu>"
        RECIPIENT = return_path
        
        BODY_TEXT = ("We received your email sent at {} with the subject {}.\n\n"
                     "Here is a 240 character sample of the email body:{} \n\n"
                     "The email was categorized as {} with a {}% confidence.".format(date, subject, payload, classification, classification_confidence_score)
                     )
        
        CHARSET = "UTF-8"
        
        
        response = ses.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': "Spam Classification",
                },
            },
            Source=SENDER,
        )
        
        print(response)
        
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
