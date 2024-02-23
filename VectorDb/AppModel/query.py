from .mapping import appIndexName
from ..Utils import api

def getHitsFromResult(res):
    if(res['hits']["total"] == 0):
        return []
    
    return res["hits"]["hits"]


def queryAppName(appName, indexName=appIndexName):
    # print(api.getAllRecords(indexName))
    dataQuery={
        "query": {
            "term": {
                "name": appName
            }
        }
    }
    res = api.client.search(index=indexName, body=dataQuery, ignore=400)
    return getHitsFromResult(res)