from ..Utils import api
from .mapping import rawDataIndexName

def getHitsFromResult(res):

    if(res["hits"]["total"] == 0):
        return []
    
    return res["hits"]["hits"]


def queryAllRecords(indexName=rawDataIndexName):
    res = api.getAllRecords(indexName)
    return getHitsFromResult(res)


def queryByDateRange(start, end, indexName=rawDataIndexName):
    dataQuery={
        "query": {
            "range": {
                "date": {
                    "gte": start,
                    "lte": end
                }
            }
        }
    }
    res = api.client.search(index=indexName, body=dataQuery)
    return getHitsFromResult(res)

def queryBySource(source, indexName=rawDataIndexName):
    dataQuery={
        "query": {
            "match": {
                "source": source
            }
        }
    }
    res = api.client.search(index=indexName, body=dataQuery)
    return getHitsFromResult(res)

def queryByKeywordsInText(keywords, indexName=rawDataIndexName):
    dataQuery={
        "query": {
            "match": {
                "text": " ".join(keywords)
            }
        }
    }
    res = api.client.search(index=indexName, body=dataQuery)
    return getHitsFromResult(res)
