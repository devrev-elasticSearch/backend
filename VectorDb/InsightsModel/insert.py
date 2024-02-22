from ..Utils import api
from .mapping import insightsIndexName

def insertRecord(record, indexName=insightsIndexName):
    api.insertRecord(indexName, record)

def bulkInsert(records, indexName=insightsIndexName):
    api.bulkInsert(indexName, records)