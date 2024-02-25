from ..Utils import api
from .mapping import featureIndex

def getHitsFromResult(res):
    if(res['hits']["total"] == 0):
        return []
    
    return res["hits"]["hits"]


def queryAll():
    dataQuery = {
        "query": {
            "match_all": {}
        }
        
    }
    
    res = api.client.search(index=featureIndex, body=dataQuery, ignore=400)
    res = getHitsFromResult(res)
    return [x["_source"] for x in res]