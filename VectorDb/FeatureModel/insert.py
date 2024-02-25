from ..Utils import api
from .mapping import featureIndex

def insertRecord(record, indexName=featureIndex):
    res = api.client.index(index=indexName, body=record)
    return res

def bulkInsert(records, indexName=featureIndex):
    res = api.bulkInsert(indexName, records)
    return res