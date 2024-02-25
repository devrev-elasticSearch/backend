from AWS import sqs
from VectorDb.FeatureModel import insert as featureInsert

from dotenv import load_dotenv
import os

load_dotenv()

queueUrl = os.getenv("featureQueueUrl")

def callback(message):
    print(message)
    featureInsert.bulkInsert(message)
    print("Inserted")
    
def loop():
    sqs.loop(queueUrl, callback=callback, timeInMinutes=1,delete=True)