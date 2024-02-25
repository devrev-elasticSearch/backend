from ..Utils import api
from .mapping import appIndexName

def insertAppData(data):
    api.insertRecord(appIndexName, data)

def bulkInsertAppData(data):
    api.bulkInsert(appIndexName, data)
    
    
def deleteByAppName(appName):
    api.deleteByQuery(appIndexName, {"query": {"match": {"name": appName}}})