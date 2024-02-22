from ..Utils import api
from .mapping import dataIndexName

def insertRecord(record, indexName=dataIndexName):
    api.insertRecord(indexName, record)

def bulkInsert(records, indexName=dataIndexName):
    api.bulkInsert(indexName, records)

