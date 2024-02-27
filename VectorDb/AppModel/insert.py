from ..Utils import api
from .mapping import appIndexName

def insertAppData(data):
    api.insertRecord(appIndexName, data)

def bulkInsertAppData(data):
    api.bulkInsert(appIndexName, data)
    

def updateByAppName(appName, data):
    api.updateRecordByField(appIndexName, "name", appName, data)
    return

def updateById(id, data):
    api.updateRecord(appIndexName, id, data)
    return
    
    
def deleteByAppName(appName):
    api.deleteByQuery(appIndexName, {"query": {"match": {"name": appName}}})