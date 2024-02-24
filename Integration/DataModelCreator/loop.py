from AWS import sqs
from dotenv import load_dotenv
from AI.utils import run_phase1
from VectorDb.AppModel import query as appQuery
from VectorDb.DataModel import insert as dataInsert
import os

load_dotenv()

rawDataQueueUrl = os.getenv("rawDataQueueUrl")
dataQueueUrl  = os.getenv("dataQueueUrl")

def callback(messages,appName="Google Pay"):
    appData = appQuery.queryByAppName(appName)[0]["_source"]
    print(appData)
    returnData,_ = run_phase1(messages,appData)

    if(len(returnData) == 0):
        print("Not publishing today")
        return
    
    sqs.publishToSqsQueue(dataQueueUrl, returnData)
    dataInsert.bulkInsert(returnData)
    print(returnData)

def loop(timeInMinutes=1,numMessages=1):
    sqs.loop(rawDataQueueUrl,timeInMinutes,numMessages,callback)
