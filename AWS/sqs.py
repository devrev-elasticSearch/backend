import boto3
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Create SQS client
accessKey = os.getenv("accessKey")
secretKey = os.getenv("secretKey")
region = os.getenv("region")

sqs = boto3.client('sqs', region_name=region, aws_access_key_id=accessKey, aws_secret_access_key=secretKey)

def publishToSqsQueue(queueUrl, messageBody={}):
    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queueUrl,
        DelaySeconds=10,
        MessageBody=json.dumps(messageBody)
    )

    return response

def pollSqsQueue(queueUrl,  maxMessages=1, waitTimeSeconds=20):
    # Create an SQS client with your credentials
    # Poll the SQS queue
    response = sqs.receive_message(
        QueueUrl=queueUrl,
        AttributeNames=[
            'All'
        ],
        MaxNumberOfMessages=maxMessages,
        MessageAttributeNames=[
            'All'
        ],
        WaitTimeSeconds=waitTimeSeconds
    )

    # Extract messages from the response
    messages = response.get('Messages', [])

    return messages

def loop(queueUrl,timeInMinutes=10,maxMessages=1,callback=print,delete=True):
    while True:
        messages = pollSqsQueue(queueUrl, maxMessages=maxMessages)
        totalMessages = []
        if messages:
            for message in messages:
                for msg in json.loads(message['Body']):
                    totalMessages.append(msg)

                # Delete the message from the queue after processing
                receiptHandle = message['ReceiptHandle']

                if(delete):
                    sqs.delete_message(
                        QueueUrl=queueUrl,
                        ReceiptHandle=receiptHandle
                    )

        callback(totalMessages)
        time.sleep(timeInMinutes*60)
