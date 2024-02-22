from ..Utils import api
from .mapping import rawDataIndexName

def insertRecord(record, indexName=rawDataIndexName):
    api.insertRecord(indexName, record)

def bulkInsert(records, indexName=rawDataIndexName):
    api.bulkInsert(indexName, records)