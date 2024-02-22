from AWS import sqs
from dotenv import load_dotenv
from .denoise import spam_check
import os

load_dotenv()

snapInQueueUrl = os.getenv("snapInQueueUrl")
rawDataQueueUrl = os.getenv("rawDataQueueUrl")

def callback(message):
    publishList = []
    for msg in message:
        if spam_check(msg['text']) is not None:
            publishList.append(msg)
    
    if(len(publishList) == 0):
        print("Not publishing today")
        return
    sqs.publishToSqsQueue(rawDataQueueUrl, message)
    print(publishList)


def loop(timeInMinutes=10,numMessages=1):
    sqs.loop(snapInQueueUrl,timeInMinutes,numMessages,callback)