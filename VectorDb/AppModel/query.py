from .mapping import appIndexName
from ..Utils import api
import random

def getHitsFromResult(res):
    if(res['hits']["total"] == 0):
        return []
    
    return res["hits"]["hits"]

def isAppNamePresent(appName, indexName=appIndexName):
    dataQuery={
        "query": {
            "term": {
                "name": appName
            }
        }
    }
    res = api.client.search(index=indexName, body=dataQuery, ignore=400)
    return res['hits']["total"] > 0


def queryByAppName(appName, indexName=appIndexName):
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

def queryUniqueAppNames(indexName=appIndexName):
    dataQuery={
        "size": 0,
        "aggs": {
            "unique_app_names": {
                "terms": {
                    "field": "name"
                }
            }
        }
    }
    res = api.client.search(index=indexName, body=dataQuery, ignore=400)
    return res["aggregations"]["unique_app_names"]["buckets"]

def queryRandomFirstOrderLabel(appName="Google Pay",indexName=appIndexName):
    dataQuery={
        "query": {
            "term": {
                "name": appName
            }
        },
        "size": 50,
        "sort": [
            {
                "_script": {
                    "type": "number",
                    "script": {
                        "lang": "painless",
                        "source": "Math.random()"
                    },
                    "order": "asc"
                }
            }
        ]
    }
    res = api.client.search(index=indexName, body=dataQuery, ignore=400)
    temp = getHitsFromResult(res)[0]["_source"]["first_order_labels"]
    
    
    if temp == []:
        return queryRandomFirstOrderLabel(appName)
    
    random.shuffle(temp)
    return temp[0]['name']